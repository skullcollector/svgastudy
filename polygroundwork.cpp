//  g++ polygroundwork.cpp -o test $(sdl-config --libs --cflags)
//  Refresher course for how C++/C works
//
#include <stdlib.h>
#if defined(_MSC_VER)
#include "SDL.h"
#else
#include "SDL/SDL.h"
#endif
#include <stdio.h>
#include <math.h>
#define PI (3.14159265)

SDL_Surface *screen;


void printarray(unsigned int array[], int array_length){
  //for (int i = 0; i < arraylength, i++)
  for (int i =0; i < array_length; i++, array++){
    printf("array elem[%d]\n",*array);    
    
  }
  return ;
}

void printarray2(unsigned int *array, int array_length){
  //for (int i = 0; i < arraylength, i++)
  for (int i =0; i < array_length; i++, array++){
    printf("array elem[%d]\n",*array);    
    
  }
  return ;
}


void printptr(unsigned int *ptr) {
  printf("ptr elem = 0x%x, %d\n",ptr,*ptr);
}

typedef struct Coord {
  int x; 
  int y;
  int bla;
} ;

typedef Coord* CoordPtr;

void printCoord(Coord &ptr) {
  printf("ptr elem = 0x%x, x=%d, y=%d\n",&ptr,ptr.x,ptr.y);  
  ptr.x = 151;
}

/*
  recap on C peculiarities. Pointers, passing by value/reference, passing arrays.
  classes
  */
int main(int argc, char *argv[]){
  unsigned int array1[] = {1,2,3,4,5};
  printarray(array1,sizeof(array1)/sizeof(unsigned int));
  printptr(array1+2);
  array1[2] = 12;
  printptr(array1+2);
  printarray(array1,sizeof(array1)/sizeof(unsigned int));
  Coord xxx = {
    101,  // should be x
    2320, // should be y
    -1};  // should be bla
  printf("bla = %d\n",xxx.bla);
  printf("x = %d\n",xxx.x);
  printf("y = %d\n",xxx.y);
  printCoord(xxx);
  printCoord(xxx);
  printarray2(array1,sizeof(array1)/sizeof(unsigned int));
}

