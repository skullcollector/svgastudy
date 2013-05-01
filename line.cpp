// From  http://sol.gfxile.net/gp/ch02.html
//
// Call with  g++ test.c -o test $(sdl-config --libs --cflags)
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

#define PI 3.14159265


typedef struct Coord{
  int x;
  int y;
};

void gen_pt_with_gradient(float gradient, Coord *output, Coord *start_coord     ,  int radius   );
void putpixel(int x,int y, int color);
void putpixel(Coord *pt, int color);
bool practically_nothing(int value);
void oct_x_dom_imp(Coord *ptA, Coord *ptB,int colour);
void oct_y_dom_imp(Coord *ptA, Coord *ptB,int colour);
void line(Coord *ptA, Coord *ptB, int colour);
void line (int startx, int starty, int stopx, int stopy, int colour);
void testcases(float *gradient_list,int list_length,Coord **output, Coord *start_coord, int radius );
void create_npoly(int num_corners, Coord **output, Coord *start_coord,int radius,float theta);
void regupoly(Coord *points, int number_of_points);

SDL_Surface *screen;

static Coord* output=NULL;
static Coord* output2=NULL;
static Coord coordlist[] = {  // upside down house
  {10,10},
  {200, 10}, 
  {200,200},
  {105,300},
  {10,200}
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
  return (value < some_value);
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
  int x = startx, y = starty, error=0;
  while(deltay > 0) {
    putpixel(x,y,colour);
    deltay -= 1;
    y += 1;
    error += DX; // error+DX
    if ((error << 1) < DY) {   /// MISTAKE? DX Rather?
      // doo nothing...      
    } else {
      x += x_increment;
      error -= DY; // error+DX-DY
    }
  }
  return;
}





void line (int startx, int starty, int stopx, int stopy, int colour=0xff0000) {
  Coord ptA,ptB;
  ptA.x = startx;  ptA.y = starty;
  ptB.x = stopx;  ptB.y = stopy;
  return;
}

void line0(Coord *ptA, Coord *ptB, int colour=0xff0000) {
  int deltax = ptB->x - ptA->x;
  int deltay = ptB->y - ptA->y;
  
  int startx = ptA->x;
  int starty = ptA->y;

  // Vertical lines..
  if (practically_nothing(deltax)) {
    if (deltay < 0) {
      deltay = -deltay;
      startx = ptB->x;
      starty = ptB->y;
    }

    int y = starty;
    while(deltay > 0) {
      deltay -= 1;
      putpixel(startx, y,colour);
      y += 1;
    }
    return;
  }
  
  // Horizontal lines..
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
  // NO EDIT
  int dx = deltax, dy= deltay;
  dx = dx < 0 ? -dx : dx;
  dy = dy < 0 ? -dy : dy;
  if (dx > dy) {
    oct_x_dom_imp(ptA,ptB,colour);
  } else {
    oct_y_dom_imp(ptA,ptB,colour);
  }
  
  return;
}

void line1(Coord *ptA, Coord *ptB, int colour=0xff0000) {
  int deltax = ptB->x - ptA->x;
  int deltay = ptB->y - ptA->y;
  
  int startx = ptA->x;
  int starty = ptA->y;
  int stopx = ptB->x;
  int stopy = ptB->y;

  
  if (abs(deltax) >= abs(deltay)) {
    #if 0
    oct_x_dom_imp(ptA,ptB,0x00ffff);
    #else

    startx = ptA->x; starty = ptA->y;
    stopx = ptB->x;  stopy = ptB->y;

    if (deltax < 0 ) {
      deltax = -deltax;
      deltay = -deltay;
      startx = ptB->x; starty = ptB->y;
      stopx = ptA->x; stopy = ptA->y;    
    }
    
    int y_increment = 1;
    if (deltay < 0) {
      y_increment = -1;
      deltay = -deltay;
    }

    int DX = deltax, DY = deltay;
    int x = startx, y = starty, error =0;
    while(deltax > 0) {
      putpixel(x,y,colour);
      deltax -= 1;
      x += 1;
      error += DY; // error+DY
      if (!((error << 1) < DX)) {
    	y += y_increment;
    	error -= DX; // error+DY-DX
      }
    }
    #endif
  } else {
    #if 0
    oct_y_dom_imp(ptA,ptB,colour);
    #else
    startx = ptA->x; starty = ptA->y;
    stopx = ptB->x;  stopy = ptB->y;

    if (deltay < 0 ) {
      deltax = -deltax;
      deltay = -deltay;
      startx = ptB->x; starty = ptB->y;
      stopx = ptA->x; stopy = ptA->y;    
    }
    
    int x_increment = 1;
    if (deltax < 0) {
      x_increment = -1;
      deltax = -deltax;
    }

    int DX = deltax, DY = deltay;
    int x = startx, y = starty, error =0;
    while(deltay > 0) {
      putpixel(x,y,colour);
      deltay -= 1;
      y += 1;
      error += DX; // error+DY
      if (!((error << 1) < DY)) {
    	x += x_increment;
    	error -= DY; // error+DY-DX
      }
    }
  #endif
  }

  return;
}
/**
 *
 * Optimized based on above code and M Abrash's book's methods
 * DOes not use float division OR abs value calls.
 *
 */
void line(Coord *ptA, Coord *ptB, int colour=0xff0000) {  

  int deltax = 0; 
  int deltay = 0;  
  int startx = 0; 
  int starty = 0; 
  int stopx = 0;
  int stopy = 0;
  
  // Make sure one delta is > 0, pick deltaY
  if (ptA->y < ptB->y) {
    startx = ptA->x; starty = ptA->y;
    stopx = ptB->x; stopy = ptB->y;
  }
  else {
    startx = ptB->x; starty = ptB->y;
    stopx = ptA->x; stopy = ptA->y;
  }

  // will be > 0 !
  deltax = stopx - startx;
  deltay = stopy - starty; 

  // This means xincr will be the direction indicator.
  bool x_dominant = false;
  bool y_dominant = false;
  int xincr = 1;

  if (deltax > 0) {
    if(deltax > deltay) {
      x_dominant = true;
    } else {
      y_dominant = true;
    }
  } else {
    deltax = -deltax;
    xincr = -1;
    if(deltax > deltay) {
      x_dominant = true;
    } else {
      y_dominant = true;
    }
  }

  int x=startx, y = starty, error =0;
  int DX = deltax, DY = deltay;

  // I dont want to make extra func calls if I can help it. 
  // Using flags instead.
  if (x_dominant) {  // for octants where abs(deltaX) > abs(deltaY); gradients < 1
    while(deltax > 0) {
      putpixel(x,y,colour);
      deltax -= 1;
      x += xincr;
      error += DY; // error+DY
      if (!((error << 1) < DX)) {
    	y += 1;
    	error -= DX; // error+DY-DX
      }
    }
    return;
  }

  if (y_dominant) { // for octants where abs(deltaX) <= abs(deltaY); gradients >= 1
    while(deltay > 0) {
      putpixel(x,y,colour);
      deltay -= 1;
      y += 1;
      error += DX; // error+DY
      if (!((error << 1) < DY)) {
    	x += xincr;
    	error -= DY; // error+DY-DX
      }
    } 
    return;
  }
  return;
}


void gen_pt_with_gradient(float gradient, Coord *output, Coord *start_coord=NULL,  int radius=100) {
  float angle = atan(gradient);
  int x=0, y=0, startx=0, starty=0;
  if (start_coord) {
    startx = start_coord->x; starty = start_coord->y;
  }
  x = startx + radius*cos(angle);
  y = starty + radius*sin(angle);
  if (output) {
    output->x = x;
    output->y = y;
  }
}

void testcases(float *gradient_list,int list_length,Coord **output, Coord *start_coord=NULL, int radius = 10) {
  
  if (!gradient_list||list_length <= 0||!output) {
    return;
  } else if (!*output) {
    return;
  }

  int x=0, y=0, startx=0, starty=0;
  if (start_coord) {
    startx = start_coord->x; starty = start_coord->y;
  }
  
  printf("list length = %d",list_length);
  

  Coord* start = *output;
  for (int i = 0; i < list_length;i++) {
    gen_pt_with_gradient(gradient_list[i],start++, start_coord);
    printf("\n\nCoord x %d, y %d",start[i].x,start[i].y);
  }
}

void regupoly(Coord *points, int number_of_points) {

    // def regupoly(self,points,marks=None):
    //     number_of_pnts = len(points)
    //     for i in range(0,number_of_pnts):
    //         self.charline(points[i], points[(i+1)%number_of_pnts],marks=marks)
  for (int i =0 ; i < number_of_points; i++) {
    line(&points[i],&points[(i+1)%number_of_points]);
  }
}

void create_npoly(int num_corners, Coord **output, Coord *start_coord=NULL,int radius=100,float theta=0) {
  float angle = 0;
  int xn=0, yn=0;

  int x=0, y=0;
  if (start_coord) {
    x = start_coord->x; y = start_coord->y;
  }
  
  Coord *start = *output;
  for (int corner_number = 0; corner_number < num_corners; corner_number++) {
    angle = corner_number * 2 * PI/num_corners+theta;
    start->x = int(x+radius*cos(angle));
    start->y = int(y+radius*sin(angle));
    start++;
  }
}

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
