#include "CellularAutomata.hpp"
#include <cassert>
#include <fstream>
#include <cstddef>
#include <cmath>
using namespace std;
//---- Functions
double  getDistance(stCell A, stCell B){
  double x = A.d_lat - B.d_lat;
  double y = A.d_long - B.d_long;
  return sqrt((x * x) + (y * y));
}


//------------------------------------------------------------------------------
CellularAutomata::CellularAutomata():
mCellX(0),
mCellY(0),
mEmptySize(0),
mDeltaX(0.0),
mDeltaY(0.0),
mCellList(NULL),
mCellListEmpty(NULL),
mLattice0(NULL),
mLattice1(NULL),
mWeight(NULL),
mRadius(1)
{};

CellularAutomata::~CellularAutomata(){
  clear();
};


void CellularAutomata::setLattice(int _x, int _y){
  clear();
  mCellX = _x; mCellY = _y;

  assert(posix_memalign((void**) &mCellList, ALIGN, mCellX * mCellY *  sizeof(stCell)) == 0);
  assert(mCellList != NULL);

  assert(posix_memalign((void**) &mLattice0, ALIGN, mCellX * mCellY *  sizeof(int)) == 0);
  assert(mLattice0 != NULL);

  assert(posix_memalign((void**) &mLattice1, ALIGN, mCellX * mCellY *  sizeof(int)) == 0);
  assert(mLattice1 != NULL);

  assert(posix_memalign((void**) &mWeight, ALIGN, mCellX * mCellY *  sizeof(stWeight)) == 0);
  assert(mWeight != NULL);


  memset(mCellList, 0x00, mCellX * mCellY *  sizeof(stCell));
  memset(mLattice0, 0x00, mCellX * mCellY *  sizeof(int));
  memset(mLattice1, 0x00, mCellX * mCellY *  sizeof(int));
  memset(mWeight,   0x00, mCellX * mCellY *  sizeof(stWeight));


};

void CellularAutomata::setData(int _x, int _y,
                               int _id,
                               int _bus,
                               int _health,
                               int _school,
                               double _lat, double _long,
                               int _state,
                               bool _change){

   int  p = _y * mCellX + _x;
   assert((_x < mCellX) && (_y < mCellY));

   mCellList[p].id = _id;
   mCellList[p].bus = _bus;
   mCellList[p].health = _health;
   mCellList[p].school = _school;
   mCellList[p].d_lat = _lat;
   mCellList[p].d_long = _long;
   //mCellList[p].state = _state;
   mCellList[p].change = _change;
   mLattice0[p] = _state;
   /*if (mCellList[p].state == 2){
     cerr << "Error" << endl;
     exit(-1);
   }*/
   /*
   if (p == 10444){
     cout << _x << endl;
     cout << _y << endl;
     cout << _id << endl;
     cout << _bus << endl;
     cout << _health << endl;
     cout << _school << endl;
     cout << _lat << endl;
     cout << _long << endl;
     cout << _state << " <<<< " << endl;
     cout << _change << endl;
   }
*/
};

void CellularAutomata::setDiscritization(double dx, double dy){
  mDeltaX = dx;
  mDeltaY = dy;
};

void CellularAutomata::clear(void){
  if (mCellList != NULL)
     free(mCellList);
  if (mCellListEmpty != NULL)
    free(mCellListEmpty);
  if (mCellListEmpty != NULL)
    free(mCellListEmpty);
  if (mLattice0 != NULL)
    free(mLattice0);
  if (mLattice1 != NULL)
    free(mLattice1);
  if (mWeight != NULL)
      free(mWeight);

  mCellListEmpty = NULL;
  mCellList = NULL;
  mLattice0 = NULL;
  mLattice1 = NULL;
  mWeight = NULL;
  mCellX = mCellY = 0;
};



void CellularAutomata::loadConfigFile(const string& configFile){

        string fileName = "";
        fstream input;
        fileName = configFile;
        assert(configFile.compare("") != 0);
        input.open(fileName, ios::in|ios::binary);
        assert(input.is_open());
        input.read(reinterpret_cast<char*> (&mCellX), sizeof(int));
        input.read(reinterpret_cast<char*> (&mCellY), sizeof(int));

        setLattice(mCellX, mCellY);
      /*
        assert(posix_memalign((void**) &mCellList, ALIGN, mCellX * mCellY *  sizeof(stCell)) == 0);
        assert(mCellList != NULL);
        memset(mCellList, 0x00, mCellX * mCellY *  sizeof(stCell));
*/
        input.read(reinterpret_cast<char*> (mCellList), mCellX * mCellY * sizeof(stCell));
        input.read(reinterpret_cast<char*> (mLattice0), mCellX * mCellY * sizeof(int));
        input.close();
        cout << "File loaded [" << fileName << "]" << endl;
        for (int i = 0; i < mCellX * mCellY; i++)
          mLattice1[i] = mLattice0[i];

/*
        assert(posix_memalign((void**) &mLattice0, ALIGN, mCellX * mCellY *  sizeof(int)) == 0);
        assert(mLattice0 != NULL);

        assert(posix_memalign((void**) &mLattice1, ALIGN, mCellX * mCellY *  sizeof(int)) == 0);
        assert(mLattice1 != NULL);

        memset(mLattice0, 0x00, mCellX * mCellY *  sizeof(int));
        memset(mLattice1, 0x00, mCellX * mCellY *  sizeof(int));

        assert(posix_memalign((void**) &mWeight, ALIGN, mCellX * mCellY *  sizeof(stWeight)) == 0);
        assert(stWeight != NULL);
*/
        buildList();
        setWeightSuitability();


};
void CellularAutomata::saveConfigFile(const string& configFile){
    string fileName = configFile;
    fstream output;
    assert(fileName.compare("") != 0);
    output.open(fileName, ios::out|ios::binary|ios::trunc);
    assert(output.is_open());
    output.write(reinterpret_cast<const char*> (&mCellX), sizeof(int));
    output.write(reinterpret_cast<const char*> (&mCellY), sizeof(int));
    output.write(reinterpret_cast<const char*> (mCellList), mCellX * mCellY * sizeof(stCell));
    output.write(reinterpret_cast<const char*> (mLattice0), mCellX * mCellY * sizeof(int));

    output.close();
    cout << "File saved [" << fileName << "]" << endl;
/*

      cout << mCellList[10444].id << endl;
      cout << mCellList[10444].bus << endl;
      cout << mCellList[10444].health << endl;
      cout << mCellList[10444].school << endl;
      cout << mCellList[10444].d_lat << endl;
      cout << mCellList[10444].d_long << endl;
      cout << mCellList[10444].state << " <<<< " << endl;
      cout << mCellList[10444].change << endl;
*/
};

stCell CellularAutomata::getCell(int _x, int _y){
  int p = _y * mCellX + _x;
  assert(p < mCellX * mCellY);
  return mCellList[p];

};


int CellularAutomata::getState(int _x, int _y){
  int p = _y * mCellX + _x;
  assert(p < mCellX * mCellY);
  return mLattice0[p];

};

void CellularAutomata::buildList(void){

  int count = 0;


    for (int i = 0; i < mCellX * mCellY; i++){

      if (mLattice0[i] == CellularAutomata::EMPTY)
       count++;


    }
    cout << "Count:" << count << endl;

    assert(posix_memalign((void**) &mCellListEmpty, ALIGN, count *  sizeof(int)) == 0);
    assert(mCellListEmpty != NULL);
    mEmptySize = count;
    int j = 0;
    for (int i = 0; i < mCellX * mCellY; i++){
      if (mLattice0[i] == CellularAutomata::EMPTY){
       mCellListEmpty[j] = i;
       j++;
      }
    }//end-for (int i = 0; i < mCellX * mCellY; i++){

};

void CellularAutomata::printEmptyArea(void){
    double area =  mDeltaX * mDeltaY;
    double count = 0.0;
    for (int i = 0; i < mCellX * mCellY; i++){
       if (mLattice0[i] == CellularAutomata::EMPTY){
         count++;
       }else if (mLattice0[i] == CellularAutomata::LAKE){
         count++;
       }

    }
    area *= count;
    cout << "Area:" << area << " meters "<< endl;


};

/*
* add atributes for each cell, usualy it comes from file
*/
void CellularAutomata::addAttrib(int i, int j, int t, int v, double w){
  assert((i < mCellX) && (i>= 0) && (j < mCellY) && (j > 0));
  int k = j * mCellX + i;
  switch (t){
    case CellularAutomata::INHERITED:
      mCellList[k].inherited = v;
      mWeight[k].inherited = w;
    break;
    case CellularAutomata::ECOLOGICAL:
      mCellList[k].ecological = v;
      mWeight[k].ecological = w;

    break;
    case CellularAutomata::PLANNING:
      mCellList[k].planning = v;
      mWeight[k].planning = w;

    break;
  }//switch (t){
};

void CellularAutomata::setWeightSuitability(void){
  //Get sum in order to normalize the values

  double b_max = 0.0,
         s_max = 0.0,
         h_max = 0.0;
  for (int i = 0; i < mCellX * mCellY; i++){
    stCell src = mCellList[i];
    b_max += static_cast<double>(src.bus);
    s_max += static_cast<double>(src.health);
    h_max += static_cast<double>(src.school);

  }//end-for (int i = 0; i < mCellX * mCellY; i++){


  for (int i = 0; i < mCellX * mCellY; i++){
    double w_b = 0.0,
           w_s = 0.0,
           w_h = 0.0;
    stCell src = mCellList[i];

    for (int j = 0; j < mCellX * mCellY; j++){
      if (i != j){
        stCell dest =  mCellList[j];
        double d = getDistance(src, dest);

        w_b += ( (static_cast<double>(dest.bus) / b_max) * d);
        w_s += ( (static_cast<double>(dest.health) / s_max) * d);
        w_h += ( (static_cast<double>(dest.school) / h_max) * d);

      }//end-if (i != j){
    }//end-for (int i = 0; i < mCellX * mCellY; i++){

    mWeight[i].bus    = w_b;
    mWeight[i].school = w_s;
    mWeight[i].health = w_h;
    assert(!isinf(w_b) && !isnan(w_b));
    assert(!isinf(w_s) && !isnan(w_s));
    assert(!isinf(w_h) && !isnan(w_h));

  }//end-for (int i = 0; i < mCellX * mCellY; i++){
};


void CellularAutomata::update(void){
    cout << "Updated..." << endl;
    int r = mRadius;

    for (int k = 0; k < mEmptySize; k++){
       int    ix =  mCellListEmpty[k] % mCellX;
       int    iy =  mCellListEmpty[k] / mCellX;
       int    ip = (iy * mCellX) + ix;
       //double N = 0.0;
       double sum = 0.0f;
       double elements = 0.0f;

       for (int rj = -r; rj <= r; rj++){
         int pj = iy - rj;
         for (int ri = -r; ri <= r; ri++){
           int pi = ix + ri;
           int p = (pj * mCellX) + pi;
           if (!((rj == 0) && (ri == 0))){
             /*
             double b = static_cast<double>(mCellList[p].bus)    * mWeight[p].bus;
             double h = static_cast<double>(mCellList[p].health) * mWeight[p].health;
             double s = static_cast<double>(mCellList[p].school) * mWeight[p].school;
             */

             double b = mWeight[p].bus;
             double h = mWeight[p].health;
             double s = mWeight[p].school;
             double W = 0.0f;
             if (mLattice0[p] == CellularAutomata::OCCUPIED){
               W = 1.0f;
             }
             sum +=  (W * (b + h + s));
             elements++;
           }//if (!((rj == 0) && (ri == 0))){


         }//end-for (int ri = -r; ri <= r; ri++){
       }//end-for (int rj = -r; rj <= r; rj++){
       sum /= elements;
       int aIm = mLattice0[ip];
       double prob = random();
       if ((prob < sum)  && (aIm == CellularAutomata::EMPTY)){
         mLattice1[ip] = CellularAutomata::OCCUPIED;
         cout << "Ocupou!!!" << endl;
         cout.flush();
       }else{
         mLattice1[ip] = mLattice0[ip];
         cout << "NÃO Ocupou!!!" << endl;
         cout.flush();
       }

       //cout <<  mCellListEmpty[k] << "\t" << sum << "\t" << endl;
       //cout <<  mCellListEmpty[i] << " -> (" << x << "," << y << ")" << "\t " << mCellX <<  endl;
    }//end-for (int i = 0; i < mCellX * mCellY; i++){
    int *swap = mLattice1;
    mLattice1 = mLattice0;
    mLattice0 = swap;

};;

double CellularAutomata::random(void){ return static_cast <double> (rand() % 65535 + 1) / 65535.0f; };
