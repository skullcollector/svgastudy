// From  http://sol.gfxile.net/gp/ch02.html
//
// Call with  g++ test.c -o test $(sdl-config --libs --cflags)
// For SDL2 use sdl2-config... below wont work with it though, UpdateRect and SetVideoMode are shunned in SDL 2.0 land
//
#include <stdlib.h>
#if defined(_MSC_VER)
#include "SDL.h"
#else
#include "SDL/SDL.h"
#endif
#include <stdio.h>
#include <math.h>

SDL_Surface *screen;

void putpixel(int x, int y, int color)
{
  unsigned int *ptr = (unsigned int*)screen->pixels;
  int lineoffset = y * (screen->pitch / 4);
  ptr[lineoffset + x] = color;
}
/*

function line(x0, x1, y0, y1)
     int deltax := x1 - x0
     int deltay := y1 - y0
     real error := 0
     real deltaerr := abs (deltay / deltax)    // Assume deltax != 0 (line is not vertical),
           // note that this division needs to be done in a way that preserves the fractional part
     int y := y0
     for x from x0 to x1
         plot(x,y)
         error := error + deltaerr
         if error ≥ 0.5 then
             y := y + 1
             error := error - 1.0
*/

void line(int x0, int y0, int x1, int y1) {
  float deltax = (float)(x1-x0);
  float deltay = (float)(y1-y0);
  
  float d = fabs(deltay/deltax);
  float err = 0;

  int y = y0;
  int x = x0;
  
  if (true) { //( d > 0 ) {
    for (x = x0; x <= x1; x+=1) {
      putpixel(x,y, 0xff0000);
      err = err+d;    
      if (err >= 0.5) {
	y += 1;
	err -= 1.0;
      }
    }
  }
  // else if ( d < 0 ) {
  //   for (x = x0; x <= x1; x+=1) {
  //     putpixel(x,y, 0xff0000);
  //     err = err+d;    
  //     if (err <= 0.5) {
  // 	y -= 1;
  // 	err -= 1.0;
  //     }
  //   }    
  // }
}


void line2(int x0, int y0, int x1, int y1) {
  float deltax = (float)(x1-x0);
  float deltay = (float)(y1-y0);
  
  float d = deltay/deltax;
  float err = 0;

  int y = y0;
  int x = x0;
  
  if ( d > 0 ) {
    for (x = x0; x <= x1; x+=1) {
      putpixel(x,y, 0xff0000);
      err = err+d;    
      if (err >= 0.5) {
	y += 1;
	err -= 1.0;
      }
    }
  }
  else if ( d < 0 ) {
    for (x = x0; x <= x1; x+=1) {
      putpixel(x,y, 0xff0000);
      err = err+d;    
      if (err <= -0.5) {
  	y -= 1;
  	err += 1.0;
      }
    }    
  }
}



typedef struct Coord{
  int x;
  int y;
};

static Coord coordlist[] = { {10,10},
			     {200, 100}, {400,10}};

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
  for (int i = 0; i  <  listlen; i++){
    i0 = i % listlen;
    i1 = (i+1)%listlen;
    line2(coordlist[i0].x, coordlist[i0].y, coordlist[i1].x, coordlist[i1].y);
    putpixel(coordlist[i0].x, coordlist[i0].y, 0xffff00);
    putpixel(coordlist[i1].x, coordlist[i1].y, colourstart);
    //printf("%d, %d,:: %d %d",coordlist[i0].x, coordlist[i0].y, coordlist[i1].x, coordlist[i1].y);
  }
  
  
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
