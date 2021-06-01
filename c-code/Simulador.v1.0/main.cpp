
#include <GL/glut.h>
#include <GL/glu.h>
#include <GL/gl.h>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include "CellularAutomata.hpp"
#include "App.h"

using namespace std;

Stopwatch         stopwatch;
CellularAutomata *cellularAutomata;
double elapsedTime = 0.0f;
float FPS = 0.0;
int width = 800,
    height = 600;
bool start = false;
// Função de visualização
void render(void)
{
    glClear(GL_COLOR_BUFFER_BIT);

    float dX = 0.0f,
          dY = 0.0f;

    int type = GL_LINE_LOOP;

    float delta  = 0.0f;
    glColor3f(0.0f, 0.0f, 1.0f);

    float scaleX = 1.0f/static_cast<float>(cellularAutomata->getWidth());
    float scaleY = 1.0f/static_cast<float>(cellularAutomata->getHeight());
//Each cells
    for (int j = 0; j < cellularAutomata->getHeight(); j++){
        for (int i = 0; i < cellularAutomata->getWidth(); i++){
            int state = cellularAutomata->getState(i, j);
            glPushMatrix();
            glColor3f(1.0f, 0.0f, 0.0f);
            glTranslatef(dX, dY, 0.0f);
            if (state == CellularAutomata::EMPTY){
                type = GL_LINE_LOOP;
                glColor3f(1.0f, 0.0f, 0.0f);
            }else if (state == CellularAutomata::OCCUPIED){
                type = GL_QUADS;
                glColor3f(1.0f, 1.0f, 0.0f);
            }else if (state == CellularAutomata::LAKE){
                type = GL_QUADS;
                glColor3f(0.0f, 1.0f, 0.0f);
            }

            glBegin(type); //GL_QUADS);GL_LINE_LOOP

            glVertex3f(0.0f, 0.0f, 0.0f);
            glVertex3f(0.0f, -scaleY, 0.0f);
            glVertex3f(scaleX, -scaleY, 0.0f);
            glVertex3f(scaleX, 0.0f, 0.0f);


            glEnd();
            glPopMatrix();
            dX += scaleX;

        }
        dY -= scaleY;
        dX = 0.0f;
    }
//--- Lattice
    delta  = 0.0f;
    glColor3f(0.0f, 0.0f, 1.0f);
    for (int j = 0; j <= cellularAutomata->getHeight(); j++){
        glBegin(GL_LINES); //GL_QUADS);GL_LINE_LOOP
        glVertex3f(0.0f, -delta, 0.0f);
        glVertex3f(1.0f, -delta, 0.0f);
        glEnd();
        delta += scaleY;
    }

    delta = 0.0f;
    for (int j = 0; j <= cellularAutomata->getWidth(); j++){
        glBegin(GL_LINES); //GL_QUADS);GL_LINE_LOOP
        glVertex3f(delta, 0.0f, 0.0f);
        glVertex3f(delta, -1.0f, 0.0f);
        glEnd();
        delta += scaleX;
    }


    glutSwapBuffers();


}

// Função de inicialização de parâmetros (OpenGL e outros)
void init (void){ glClearColor(0.0f, 0.0f, 0.0f, 1.0f); }

// Função de evento do teclado
void keyboardEvent(unsigned char key, int x, int y)
{
     //    glutPostRedisplay();
    switch (key) {
        case 'a':
        case 'A': cellularAutomata->printEmptyArea();
           break;
        case 'b':
        case 'B':
            start = true;
            break;
        case 'u':
        case 'U':
            cout << "Update" << endl;
            cout.flush();
          break;
        case 'e':
        case 'E':
             start = false;
            break;

        case 'q':
        case 'Q':
        case 27:
            exit (EXIT_SUCCESS);
            break;

        default:
            break;
   }
}


//Viewport
void viewPort(int w, int h)
{

    if(h == 0) h = 1;


    width = w;
    height = h;
    glViewport(0, 0, w, h);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho (-0.01f, 1.01f, -1.01f, 0.01f, -1.0f, 1.0f);
    glutPostRedisplay();
}

//Loop principal da visualização
void mainloop(void)
{
    glutPostRedisplay();
    STOP_STOPWATCH(stopwatch);
    elapsedTime += stopwatch.mElapsedTime;

    FPS++;
    if (FPS >= 100.0f){
        float realfps = 1.0f / (elapsedTime / 100.0f);
        char msg[1024];
//        sprintf(msg, "CA - Game of life \t \t Alive: %.2f \t Dead: %.2f \t FPS: %5.2f", cellularAutomata->getAlive(), cellularAutomata->getDead(), realfps);
        sprintf(msg, "CA - Chico Mendes - FPS %5.2lf", realfps);
        glutSetWindowTitle(msg);
        FPS = 0.0;
        elapsedTime = 0.0f;
    }
    START_STOPWATCH(stopwatch);

}


int main(int argc, char**argv)
{
    cellularAutomata = new CellularAutomata();
    cellularAutomata->loadConfigFile("config.bin");
    cellularAutomata->setDiscritization(50.0, 50.0);
    START_STOPWATCH(stopwatch);

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(width, height);
    glutCreateWindow("CA - Chico Mendes");
    glutDisplayFunc(render);
    glutReshapeFunc(viewPort);
    glutKeyboardFunc(keyboardEvent);
    glutIdleFunc(mainloop);
    init();
    glutMainLoop();
    delete cellularAutomata;
    return EXIT_SUCCESS;
}
