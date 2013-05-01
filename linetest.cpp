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

static Coord* output=NULL;
static Coord* output2=NULL;
static Coord coordlist[] = {  // upside down house
  {10,10},
  {200, 10}, 
  {200,200},
  {105,300},
  {10,200}
};


void render()
{   
  // Lock surface if needed
  if (SDL_MUSTLOCK(screen)) 
    if (SDL_LockSurface(screen) < 0) 
      return;

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

  int N = 5;
  if (!output2) { // render gets called a lot, let's not eat all the memory
    output2 = (Coord*)malloc(N*sizeof(Coord));;
    create_npoly(N,&output2,&startpoint);
  }

  regupoly(output2,N);
  // Unlock if needed
  if (SDL_MUSTLOCK(screen)) 
    SDL_UnlockSurface(screen);

  // Tell SDL to update the whole screen
  SDL_UpdateRect(screen, 0, 0, 640, 480);    
}


// Entry point
int main(int argc, char *argv[])
{
  // Initialize SDL's subsystems - in this case, only video.
  if ( SDL_Init(SDL_INIT_VIDEO) < 0 ) 
  {
    fprintf(stderr, "Unable to init SDL: %s\n", SDL_GetError());
    exit(1);
  }
  printf(" size %d ", sizeof(coordlist)/sizeof(Coord));
  // Register SDL_Quit to be called at exit; makes sure things are
  // cleaned up when we quit.
  atexit(SDL_Quit);
    
  // Attempt to create a 640x480 window with 32bit pixels.
  screen = SDL_SetVideoMode(800, 600, 32, SDL_SWSURFACE);
  
  // If we fail, return error.
  if ( screen == NULL ) 
  {
    fprintf(stderr, "Unable to set 640x480 video: %s\n", SDL_GetError());
    exit(1);
  }

  // Main loop: loop forever.
  while (1)
  {
    // Render stuff
    render();

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
