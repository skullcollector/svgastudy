// From  http://sol.gfxile.net/gp/ch02.html
//
// Call with  g++ test.c -o test $(sdl-config --libs --cflags)
// Compilation now a little different
//
// g++ linetest.cpp line.cpp -o test $(sdl-config --libs) -g
//
// For SDL2 use sdl2-config... below wont work with it though, UpdateRect and SetVideoMode are shunned in SDL 2.0 land
//
// Have a few versions of the line code in here. Unused line methods are marked line0, line1 etc.
// When running you shoudl see an upside house, a regular polygon and a few lines or various gradients.
//
//
#include <stdlib.h>
#if defined(_MSC_VER)
#include "SDL.h"
#else
#include "SDL/SDL.h"
#endif
#include <stdio.h>
#include <math.h>
#include "line.h"

//SDL_Surface *screen;

//The surfaces that will be used
SDL_Surface *background = NULL;


const int C_WIDTH = 800;
const int C_HEIGHT = 600;
const int C_BPP = 32;

static Coord* output=NULL;
static Coord* output2=NULL;
static Coord* output3=NULL;
static Coord* output4=NULL;
static Coord coordlist[] = {  // upside down house
  {10,10},
  {200, 10}, 
  {200,200},
  {105,300},
  {10,200}
};


void render(unsigned int counter)
{   
  // Lock surface if needed
  if (SDL_MUSTLOCK(screen)) 
    if (SDL_LockSurface(screen) < 0) 
      return;

  SDL_FillRect(screen, NULL, 0x000000);

  // Ask SDL for the time in milliseconds
  int tick = SDL_GetTicks();

  int xstart=0, ystart=0, xend=0, yend=0;
  int colour=0x00ff00;
  int colourstart = 0x00ffff;

  // Declare a couple of variables  
  int i0=0, i1=0;
  int listlen = sizeof(coordlist)/sizeof(Coord);

  regupoly(coordlist, listlen);

  float data[] = {1,0.75,0.5,0.3,0.25,0.15,0.05,0,-1};
  Coord startpoint = {300,300};
  int float_length = sizeof(data)/sizeof(float);
  if (!output) { // render gets called a lot, let's not eat all the memory
    output = (Coord*)malloc(float_length*sizeof(Coord));;
  }

  testcases(data,float_length,&output, &startpoint);
  for(int i = 0; i < float_length; i++){
    line(&startpoint, &output[i]);
  }

  int N = 6;
  if (!output2) { // render gets called a lot, let's not eat all the memory
    output2 = (Coord*)malloc(N*sizeof(Coord));;
  }
  create_npoly(N,&output2,&startpoint,200,PI/100*counter);
  regupoly(output2,N);

  int N2 = 5;
  if (!output3) { // render gets called a lot, let's not eat all the memory
    output3 = (Coord*)malloc(N2*sizeof(Coord));;
  }
  create_npoly(N2,&output3,&startpoint,100,-PI/100*counter);
  regupoly(output3,N2);

  int N3 = 7;
  if (!output4) { // render gets called a lot, let's not eat all the memory
    output4 = (Coord*)malloc(N3*sizeof(Coord));;
  }
  create_npoly(N3,&output4,&startpoint,250,-PI/100*counter);
  regupoly(output4,N3);

  // Unlock if needed
  if (SDL_MUSTLOCK(screen)) 
    SDL_UnlockSurface(screen);

  // Tell SDL to update the whole screen
  SDL_UpdateRect(screen, 0, 0, C_WIDTH, C_HEIGHT);    
}

static unsigned int counter = 0;

// Entry point
int main(int argc, char *argv[])
{
  // Initialize SDL's subsystems - in this case, only video.
  if ( SDL_Init(SDL_INIT_VIDEO) < 0 ) 
  {
    fprintf(stderr, "Unable to init SDL: %s\n", SDL_GetError());
    exit(1);
  }

  // Register SDL_Quit to be called at exit; makes sure things are
  // cleaned up when we quit.
  atexit(SDL_Quit);
    
  // Attempt to create a 640x480 window with 32bit pixels.
  screen = SDL_SetVideoMode(C_WIDTH, C_HEIGHT, C_BPP, SDL_SWSURFACE);
  
  // If we fail, return error.
  if ( screen == NULL ) 
  {
    fprintf(stderr, "Unable to set 640x480 video: %s\n", SDL_GetError());
    exit(1);
  }

  // Main loop: loop forever.
  while (1)
  {
    counter = (counter+1);
    // Render stuff
    render(counter);

    // Poll for events, and handle the ones we care about.
    SDL_Event event;
    while (SDL_PollEvent(&event)) 
    {
      switch (event.type) 
      {
      case SDL_KEYDOWN:
        break;
      case SDL_KEYUP:
        // If escape is pressed, return (and thus, quit)
        if (event.key.keysym.sym == SDLK_ESCAPE)
          return 0;
        break;
      case SDL_QUIT:
        return(0);
      }
    }
  }
  return 0;
}
