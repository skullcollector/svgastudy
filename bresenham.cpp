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

typedef struct Coord{
  int x;
  int y;
};



void putpixel(int x,int y, int color)
{
  unsigned int *ptr = (unsigned int*)screen->pixels;
  int lineoffset = y * (screen->pitch / 4);
  ptr[lineoffset + x] = color;
}

void putpixel(Coord *pt, int color)
{
  if (!pt)
    return;
  int x = pt->x;
  int y = pt->y;
  unsigned int *ptr = (unsigned int*)screen->pixels;
  int lineoffset = y * (screen->pitch / 4);
  ptr[lineoffset + x] = color;
}

bool practically_nothing(int value) {
  const float some_value = 0.1;
  value = value < 0 ? -value : value;
  if (value < some_value) {
    return true;
  }
  return false;
};

void oct_x_dom_imp(Coord *ptA, Coord *ptB,int colour=0xff0000) {
  int deltax = ptB->x - ptA->x;
  int deltay = ptB->y - ptA->y;
  
  int startx = 0, starty =0, stopx =0, stopy=0;
  startx = ptA->x; starty = ptA->y;
  stopx = ptB->x;  stopy = ptB->y;
  if (deltax < 0) {
    startx = ptB->x; starty = ptB->y;
    stopx = ptA->x; stopy = ptA->y;
    deltax = -deltax;
    deltay = -deltay;
  }
  int y_increment = 1;
  if (deltay < 0) {
    deltay = -deltay;
    y_increment = -1;
  }

  int DX=deltax, DY=deltay;
  // error error+DY and error+DY-DX
  //     x = startx
  //     y = starty
  //     current_error = 0
  int x = startx, y = starty, error=0;
  while(deltax > 0) {
    putpixel(x,y,colour);
    deltax -= 1;
    x += 1;
    error += DY; // error+DY
    if ((error << 1) < DX) {
      // doo nothing...      
    } else {
      y += y_increment;
      error -= DX; // error+DY-DX
    }
  }
//     while dx > 0:
//         dx -= 1      
//         x += 1
//         a_error =new_error['skipping y'](current_error)
//         if 2*a_error < DX:
//             current_error = a_error #new_error['skipping y'](current_error)
//         else:
//             y = y + yincr
//             current_error = new_error['adding to y'](current_error)

//         yield x,y
  return;
}


void oct_y_dom_imp(Coord *ptA, Coord *ptB,int colour=0xff0000) {
  int deltax = ptB->x - ptA->x;
  int deltay = ptB->y - ptA->y;
  
  int startx = 0, starty =0, stopx =0, stopy=0;
  startx = ptA->x; starty = ptA->y;
  stopx = ptB->x;  stopy = ptB->y;
  if (deltay < 0) {
    startx = ptB->x; starty = ptB->y;
    stopx = ptA->x; stopy = ptA->y;
    deltax = -deltax;
    deltay = -deltay;
  }
  int x_increment = 1;
  if (deltax < 0) {
    deltax = -deltax;
    x_increment = -1;
  }

  int DX=deltax, DY=deltay;
  // error error+DY and error+DY-DX
  //     x = startx
  //     y = starty
  //     current_error = 0
  int x = startx, y = starty, error=0;
  while(deltay > 0) {
    putpixel(x,y,colour);
    deltay -= 1;
    y += 1;
    error += DX; // error+DX
    if ((error << 1) < DY) {   /// ERROR ?
      // doo nothing...      
    } else {
      x += x_increment;
      error -= DY; // error+DX-DY
    }
  }
//     while dx > 0:
//         dx -= 1      
//         x += 1
//         a_error =new_error['skipping y'](current_error)
//         if 2*a_error < DX:
//             current_error = a_error #new_error['skipping y'](current_error)
//         else:
//             y = y + yincr
//             current_error = new_error['adding to y'](current_error)

//         yield x,y
  return;
}

// def oct_x_dom_imp(ptA,ptB):
//     '''
//     Redefinition:
//     current_error = DY*current_error (from float implementation)
//     '''

//     dx, dy = dxdy(ptA,ptB)

//     startx,starty = ptA.x,ptA.y
//     stopx,stopy = ptB.x,ptB.y

//     if dx < 0:
//         startx,starty = ptB.x,ptB.y
//         stopx,stopy = ptA.x,ptA.y
//         dx, dy = dxdy(ptB,ptA)

//     yincr = 1
//     if dy < 0:
//         dy = -dy
//         yincr = -1

//     #M = 1.0*dy/dx       
//     DX,DY = dx, dy

//     # new_error = { 'skipping y': lambda current_error : current_error + M,
//     #               'adding to y': lambda current_error : current_error + M - 1}

//     new_error = { 'skipping y': lambda current_error : current_error + DY,
//                   'adding to y': lambda current_error : current_error + DY - DX}

//     x = startx
//     y = starty
//     current_error = 0
//     while dx > 0:
//         dx -= 1      
//         x += 1
//         a_error =new_error['skipping y'](current_error)
//         if 2*a_error < DX:
//             current_error = a_error #new_error['skipping y'](current_error)
//         else:
//             y = y + yincr
//             current_error = new_error['adding to y'](current_error)

//         yield x,y



void line(Coord *ptA, Coord *ptB, int colour);
void line (int startx, int starty, int stopx, int stopy, int colour);

void line (int startx, int starty, int stopx, int stopy, int colour=0xff0000) {
  Coord ptA,ptB;
  ptA.x = startx;  ptA.y = starty;
  ptB.x = stopx;  ptB.y = stopy;
  return;
}


void line(Coord *ptA, Coord *ptB, int colour=0xff0000) {
  int deltax = ptB->x - ptA->x;
  int deltay = ptB->y - ptA->y;
  
  // if practically_nothing(dx):
  //     y = starty
  //     while dy > 0:
  //         dy -= 1
  //         yield (startx, y)
  //         y += 1
  //     while dy < 0:
  //         dy += 1
  //         yield (startx, y)
  //         y -= 1

  int startx = ptA->x;
  int starty = ptA->y;
  if (practically_nothing(deltax)) {
    if (deltay < 0) {
      deltay = -deltay;
      startx = ptB->x;
      starty = ptB->y;
      // stopx = ptA->x;
      // stopy = ptA->y;
    }

    int y = starty;
    while(deltay > 0) {
      deltay -= 1;
      putpixel(startx, y,colour);
      y += 1;
    }
    return;
  }

    // if practically_nothing(dy):
    //     x = startx
    //     while dx > 0:
    //         dx -= 1
    //         yield (x, starty)
    //         x += 1
            
    //     while dx < 0:
    //         dx += 1
    //         yield (x, starty)
    //         x -= 1

  if (practically_nothing(deltay)) {
    if (deltax < 0) {
      deltax = -deltax;
      startx = ptB->x;
      starty = ptB->y;
    }

    int x = startx;
    while(deltax > 0) {
      deltax -= 1;
      putpixel(x, starty,colour);
      x += 1;
    }    
    return;
  }
        

    //     if abs(dx) >= abs(dy):
    //         if not oct_x_dom:
    //             raise Exception("X dominant Line octants not implemented")

    //         for pt in oct_x_dom(ptA,ptB):
    //             yield pt
    //     else:
    //         if not oct_y_dom:
    //             raise Exception("Y dominant Line octants not implemented")
                
    //         for pt in oct_y_dom(ptA,ptB):
    //             yield pt

  int dx = deltax, dy= deltay;
  dx = dx < 0 ? -dx : dx;
  dy = dy < 0 ? -dy : dy;
  if (dx > dy) {
    oct_x_dom_imp(ptA,ptB,colour);
  } else {
    oct_y_dom_imp(ptA,ptB,colour);
  }

    // if not practically_nothing(dy) and not practically_nothing(dx):
    //     dx,dy = dxdy(ptA,ptB)
        
    //     startx, starty = ptA.x,ptA.y
    //     stopx, stopy = ptB.x,ptB.y

    //     points = []
    //     if abs(dx) >= abs(dy):
    //         if not oct_x_dom:
    //             raise Exception("X dominant Line octants not implemented")

    //         for pt in oct_x_dom(ptA,ptB):
    //             yield pt
    //     else:
    //         if not oct_y_dom:
    //             raise Exception("Y dominant Line octants not implemented")
                
    //         for pt in oct_y_dom(ptA,ptB):
    //             yield pt
  
  return;
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



def line_skeleton(ptA,ptB,oct_x_dom=None,oct_y_dom=None):
    '''
    assumptions:
    x is only increasing.
    '''
    dx,dy = dxdy(ptA,ptB)

    startx, starty = ptA.x,ptA.y
    stopx, stopy = ptB.x,ptB.y

    if practically_nothing(dx):
        y = starty
        while dy > 0:
            dy -= 1
            yield (startx, y)
            y += 1
            
        while dy < 0:
            dy += 1
            yield (startx, y)
            y -= 1
        
            
    if practically_nothing(dy):
        x = startx
        while dx > 0:
            dx -= 1
            yield (x, starty)
            x += 1
            
        while dx < 0:
            dx += 1
            yield (x, starty)
            x -= 1

    if not practically_nothing(dy) and not practically_nothing(dx):

        #import pdb; pdb.set_trace()
        dx,dy = dxdy(ptA,ptB)
        
        startx, starty = ptA.x,ptA.y
        stopx, stopy = ptB.x,ptB.y

        points = []
        if abs(dx) >= abs(dy):
            if not oct_x_dom:
                raise Exception("X dominant Line octants not implemented")

            for pt in oct_x_dom(ptA,ptB):
                yield pt
        else:
            if not oct_y_dom:
                raise Exception("Y dominant Line octants not implemented")
                
            for pt in oct_y_dom(ptA,ptB):
                yield pt
 */





static Coord coordlist[] = { 
  {10,10},
  {200, 10}, 
  {200,200},
  {105,300},
  {10,200}
};

// static Coord coordlist[] = { 
//   {10,10},
//   {200, 100}, 
//   {400,10},
//   {500,200}
// };

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
    //line(coordlist[i0].x, coordlist[i0].y, coordlist[i1].x, coordlist[i1].y);
    line(&coordlist[i0], &coordlist[i1]);
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
