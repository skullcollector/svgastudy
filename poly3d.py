'''
example borrowing heavily from M Abrash's Game Programming Black Book CHapter 50.

Z increases into the screen.

Uses convex poly drawing code only

SLow! needs to be a lot faster.
Investigate:
- numpy (tried some, seems not not help)
- python C api
- ctypes

The idea is to make a fast python SOFTWARE engine.
So opengl is for later...

'''
import pygame
from pygame.locals import *
from gfxutil import *
from math import pi, cos,sin
import numpy

PROJECTION_RATIO =-5.0
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

class PygamePlotter(Plotter):
    def __init__(self, surface, *args, **kwargs):
        self.surface = surface
        super(PygamePlotter,self).__init__(oct_x_dom = oct_x_dom_implementation,
                                           oct_y_dom = oct_y_dom_implementation, *args, **kwargs)

    def put_pixel(self, x,y,colour):
        self.surface.set_at((x,y),colour)

    def create_npoly(self, **kwargs):
        x = kwargs.get('x',20)
        y = kwargs.get('y',20)
        theta = kwargs.get('theta',0)
        corners = kwargs.get('num_of_corners',4)        
        radius =  kwargs.get('radius', 10)
        angle = lambda num : num*2*pi/(1.0*corners)
        output = []
        for corner in range(corners,0,-1):
            a = angle(corner)+theta
            xn,yn = int(round(x+radius*cos(a))), int(round(y+radius*sin(a)))
            self.put_pixel(xn,yn,0xff0000);
            output += [Coord(xn,yn)]
        return output

def test_plotter(surface):
    plt = PygamePlotter(surface,default_colour=0xff0000)

    pt1,pt2 = Coord(10,10), Coord(100,200)
    plt.put_line(pt1,pt2,0xff0000)

    output = plt.create_npoly(num_of_corners=9,radius=100,x=200,y=200);
    plt.regupoly(output,0x00ff00)
   
def convexpoly_algo(surface,rotation=0):
    plt = PygamePlotter(surface,default_colour=0xff0000)
    output = plt.create_npoly(num_of_corners=9,radius=100,x=200,y=200,theta=rotation);
    fill_convex_poly(output,drawer=plt,colour=0x0000ff)

def xformvec(xform4X4, source4X1):
    return xform4X4*source4X1

def concat_x_forms(source4X4_first, source4X4_second):   
    return source4X4_first * source4X4_second

from functools import partial
def gen_proj_pt(pt,xform4X4):
    txpolypt = xformvec(xform4X4,pt)
    xval,yval,zval,wval = txpolypt
    
    '''
    so far theory is:
    we start at center point x,y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
    if the 3d point goes to the left or right it moves by by xval/zval (zval larger, perceived xposition further away)
    if the 3d point goes to up or down it moves by by yval/zval.
    '''
    new_x = int(round((1.0*xval/zval * 1.0  * PROJECTION_RATIO*(SCREEN_WIDTH/2.0)+0.5) + SCREEN_WIDTH/2)) if zval != 0 else xval
    new_y = int(round((1.0*yval/zval * -1.0 * PROJECTION_RATIO*(SCREEN_WIDTH/2.0)+0.5) + SCREEN_HEIGHT/2)) if zval != 0 else yval
    return Coord(new_x,new_y)

def xform_and_project_poly(surface, xform4X4, polypts3d, colour = 0x00ff00,draw_hlines=False):
    plt = PygamePlotter(surface,default_colour=colour)
    polypts2d = []
    if False:
        for pt in polypts3d:
            txpolypt = xformvec(xform4X4,pt)
            xval,yval,zval,wval = txpolypt

            '''
            so far theory is:
            we start at center point x,y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
            if the 3d point goes to the left or right it moves by by xval/zval (zval larger, perceived xposition further away)
            if the 3d point goes to up or down it moves by by yval/zval.
            '''
            new_x = int(round((1.0*xval/zval * 1.0  * PROJECTION_RATIO*(SCREEN_WIDTH/2.0)+0.5) + SCREEN_WIDTH/2)) if zval != 0 else xval
            new_y = int(round((1.0*yval/zval * -1.0 * PROJECTION_RATIO*(SCREEN_WIDTH/2.0)+0.5) + SCREEN_HEIGHT/2)) if zval != 0 else yval
            polypts2d.append(Coord(new_x,new_y))  
    else:
        polypts2d = map(partial(gen_proj_pt,xform4X4=xform4X4), polypts3d)
    return fill_convex_poly(polypts2d,drawer=plt,colour=colour,draw_hlines=draw_hlines)
    
def render(surface,rotation=0, new_hotness=True):
    vertices = [
        numpy.array([[-30],
                     [-15],
                     [-1],
                     [1]]),
        numpy.array([[0],
                     [15],
                     [0],
                     [1]]),
        numpy.array([[10],
                     [-5],
                     [0],
                     [1]])
        ]
    worldform =  numpy.matrix([[1,0,0,0],
                               [0,1,0,0],
                               [0,0,1,0],
                               [0,0,0,1]])

    polyform =    numpy.matrix([[1.0, 0.0, 0.0, 0.0],
                                [0.0, 1.0, 0.0, 0.0],
                                [0.0, 0.0, 1.0, -140.0],
                                [0.0, 0.0, 0.0, 1.0] ])

    polyform[0,0] = polyform[2,2] = cos(rotation)
    polyform[0,2] = sin(rotation)
    polyform[2,0] = -polyform[0,2]

    worldviewxform = concat_x_forms(worldform, polyform)
    draw_hlines = False if new_hotness else True
    hlinesdata = xform_and_project_poly(surface, worldviewxform, vertices, draw_hlines=draw_hlines)
    if not draw_hlines:
        vals = hlinesdata.gettuples()
        temp_array = numpy.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))   
        
        idx = 0
        y = hlinesdata.ystart
        for v in vals:
            x1, x2 = v
            if x1 > x2:
                temp_array[x2:x1,y].fill(0xff0000)
            else:
                temp_array[x1:x2,y].fill(0xff0000)
            y += 1
        pygame.surfarray.blit_array(surface,temp_array)

clock = pygame.time.Clock()
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    rotation = 0
    
    while running:
        
        render(screen,rotation*pi/30)
        rotation += 1
        for event in pygame.event.get():
            if event.type == KEYDOWN: #QUIT:
                running = False
            else:
                print event
                

        pygame.display.flip()
        clock.tick(40)
        screen.fill((0,0,0))
        
    pygame.quit()
  
if __name__=='__main__':
    main()
