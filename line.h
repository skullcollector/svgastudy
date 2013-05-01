#ifndef _LINE_H
#define _LINE_SVE
#include <stdio.h>
#include <math.h>

#define PI 3.14159265
typedef struct Coord{
  int x;
  int y;
};
extern SDL_Surface *screen;

#if 0
void gen_pt_with_gradient(float gradient, Coord *output, Coord *start_coord,  int radius);
void putpixel(int x,int y, int color);
void putpixel(Coord *pt, int color);
bool practically_nothing(int value);
void oct_x_dom_imp(Coord *ptA, Coord *ptB,int colour);
void oct_y_dom_imp(Coord *ptA, Coord *ptB,int colour);
void line(Coord *ptA, Coord *ptB, int colour);
void line (int startx, int starty, int stopx, int stopy, int colour);
void testcases(float *gradient_list,int list_length,Coord **output, Coord *start_coord, int radius);
void create_npoly(int num_corners, Coord **output, Coord *start_coord,int radius,float theta);
void regupoly(Coord *points, int number_of_points);
#else

void gen_pt_with_gradient(float gradient, Coord *output, Coord *start_coord=NULL,  int radius=100);
void putpixel(int x,int y, int color);
void putpixel(Coord *pt, int color);
bool practically_nothing(int value);
void oct_x_dom_imp(Coord *ptA, Coord *ptB,int colour);
void oct_y_dom_imp(Coord *ptA, Coord *ptB,int colour);
void line(Coord *ptA, Coord *ptB, int colour=0xff0000);
void line (int startx, int starty, int stopx, int stopy, int colour=0xff0000);
void testcases(float *gradient_list,int list_length,Coord **output, Coord *start_coord=NULL, int radius =10 );
void create_npoly(int num_corners, Coord **output, Coord *start_coord=NULL,int radius=100,float theta=0);
void regupoly(Coord *points, int number_of_points);
#endif
#endif
