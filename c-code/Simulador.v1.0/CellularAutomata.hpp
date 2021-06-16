#ifndef _CELLULAR_AUTOMATA_HPP_
#define _CELLULAR_AUTOMATA_HPP_
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <iomanip>
using namespace std;

/*
 *  configure.hpp
 *
 *  Created by Marcelo Zamith on 3/15/11.
 *  Copyright 2011 __MyCompanyName__. All rights reserved.
 *  This class has the basic structure as well as transition rules
 *
 */

using namespace std;
struct stCell
{   //bus, health and school are SUITABILITY
    int id;
		int bus;
		int health;
		int school;
    //another features as well as their weight
    int inherited;
    int ecological;
    int planning;
    //position of cell in world
		double d_lat, d_long;
		//int state; //Two states
		bool change; //Allow the cell to change its state, several cells is only to give data support
};

struct stWeight{
  double bus,
         health,
         school,
         inherited,
         ecological,
         planning;
};

class CellularAutomata
{

public:
    const static int EMPTY            = 0;
    const static int OCCUPIED         = 1;
    const static int LAKE             = 2;

    const static int SUITABILITY      = 3;
    const static int INHERITED        = 4;
    const static int ECOLOGICAL       = 5;
    const static int PLANNING         = 6;
    CellularAutomata();
    ~CellularAutomata();
		void setLattice(int, int);
		void setData(int, int, int, int, int, int, double, double, int, bool);
		void setDiscritization(double, double);
		void clear(void);
		void loadConfigFile(const string& configFile);
		void saveConfigFile(const string& configFile);
    int getWidth(void)  { return mCellX; }
    int getHeight(void) { return mCellY; }
    stCell getCell(int, int);
    int getState(int, int);
    int getState(int);
    int getCellSimulated(int);
    int getCellSimulatedSize(void);
    void buildList(void);
    void addAttrib(int, int, int, int, double);
    void setWeightSuitability(void);
    void printEmptyArea(void);
    void update(void);
    double random(void);
protected:
		int mCellX;   //Space in X
    int mCellY;   //Space in Y --> number of the roads
    int mSimulatedSize;
    double mDeltaX;
    double mDeltaY; //in meters !!!!
		stCell *mCellList;
    int mRadius;
    
    int *mLattice0,
        *mLattice1,
        *mCellSimulatedList;


    stWeight *mWeight;

};
#endif
