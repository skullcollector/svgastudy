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

#include <stdio.h>
#include <math.h>

#define PI (3.14159265)

SDL_Surface *screen;


/* Strategy time!

Since I would like to learn GFX in SDL 
and NOT how to make my own classes, I'll user STL.. for now.

*/
#include <vector>
#include <iostream>
//
// Python Code I am emulating...
//
// add_after_last_point = lambda lst,x,y: lst.append(lst[-1].add(x,y))
// poly4 = [Coord(20,0)]
// add_after_last_point(poly4,-4,2)
// add_after_last_point(poly4,-6,10)
// add_after_last_point(poly4,-1,5)
// add_after_last_point(poly4,5,8)
// add_after_last_point(poly4,5,3)
// add_after_last_point(poly4,4,-4) # 4, -5???
// add_after_last_point(poly4,6,-9)
// add_after_last_point(poly4,-3,-9)

/* 
   quick n dirty Coord class 
   ALL PUBLIC! OH NOES!
*/
class Coord{
public:
  Coord(int x, int y) {
    this->x = x;
    this->y = y;
  }
  Coord(const Coord* other){
    this->x = other->x;
    this->y = other->y;
  }
  ~Coord() {
  }
  
  int x;
  int y;

  Coord & add(const Coord &rhs) {        
    Coord *newCoord = new Coord(this->x + rhs.x, 
				this->y + rhs.y);
    return *newCoord;
  }
};

/*
  List class for convenience...OPTIMIZE !
 */
class List {
public:

  List(Coord *coords=NULL){
    if(!coords){
      this->list_data = new std::vector<Coord>();
      return;
    } else {
      int size = sizeof(coords)/sizeof(Coord);
      this->list_data = new std::vector<Coord>(coords, coords+size);      
    }
    //   int myints[] = {16,2,77,29};
    // std::vector<int> fifth (myints, myints + sizeof(myints) / sizeof(int) );
  }

  Coord get(int index) {
    if (index >= 0) {
      return this->list_data->at(index);
    } else {
      std::cerr<<"Negative indexing bad" << std::endl;
      return NULL;
    }    
  }

  void append(Coord &rhs) {
    this->list_data->push_back(new Coord(rhs));
  }

  int length(){
    return this->list_data->size();  // because it's X LONG not X BIG. 
  }
  
  Coord last(){
    return this->list_data->back();
  }

  /* Not generic, but generic isnt the point */
  /* move the cursor based on last coord. */
  void add_after_last_point(int diffx, int diffy) {
    Coord last_elem = this->list_data->back();
    this->list_data->push_back(new Coord(last_elem.x+diffx, 
					 last_elem.y+diffy));
  }

private:
  // Wrap the STL for now.
  std::vector<Coord> *list_data;
};


void putpixel(int x,int y, int color);
void putpixel(Coord *pt, int color);
bool practically_nothing(int value);

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
  for (int i = 0; i < 500; i++)
    putpixel(i,i%30,0xff0000);

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
  
  // printf(" size %d ", sizeof(coordlist)/sizeof(Coord));
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

  List *list = new List();
  Coord* crd1 = new Coord(12,123);
  Coord* crd2 = new Coord(300,100);
  list->append(*crd1);
  list->append(*crd2);
  list->add_after_last_point(-10,20);
  // list->get(0).x=10; this is bad I guess... -fpermissive?
  printf("0--> %d %d\n",list->get(0).x,list->get(0).y);
  printf("1--> %d %d\n",list->get(1).x,list->get(1).y);
  printf("2--> %d %d\n",list->get(2).x,list->get(2).y);


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




void putpixel(int x,int y, int color)
{
  if(!screen)
    return;
  unsigned int *ptr = (unsigned int*)screen->pixels;
  int lineoffset = y * (screen->pitch / 4);
  ptr[lineoffset + x] = color;
}

void putpixel(Coord *pt, int color)
{
  if (!pt||!screen)
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
