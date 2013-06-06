'''
example borrowing heavily from M Abrash's Game Programming Black Book CHapter 50 and 55.

Z increases into the screen.

Uses convex poly drawing code only

Less SLow! needs to be a lot faster.
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
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 800


class ModelColor (object):
    red = 0
    green = 0
    blue = 0
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

class ModelIntensity (object):
    red = 0
    green = 0
    blue = 0
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

gamma4_levs = [0,39,53,63]
gamma64_levs = [ 0, 10, 14, 17, 19, 21, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34,
                 35, 36, 37, 37, 38, 39, 40, 41, 41, 42, 43, 44, 44, 45, 46, 46,
                 47, 48, 48, 49, 49, 50, 51, 51, 52, 52, 53, 53, 54, 54, 55, 55,
                 56, 56, 57, 57, 58, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63];

def set_palette(surface):
    cmap = numpy.zeros((256,3))
    red,green,blue = 0,1,2

    for r in range(0,4):
        for g in range(0,4):
            for b in range(0,4):
                idx = (r<<4)+(g<<2)+b;
                cmap[idx, :]= gamma4_levs[r], gamma4_levs[g], gamma4_levs[b]

    for r in range(0,64):
        cmap[64+r, :] = gamma64_levs[r], 0,0

    for g in range(0,64):
        cmap[128+g, :] = 0, gamma64_levs[g], 0

    for b in range(0,64):
        cmap[192+b, :] = 0,0,gamma64_levs[b]

    surface.set_palette(cmap)

# From L55-3.c        
def model_colour_to_colour_index(color):
    if color.red == 0:
        if color.green ==0:
            return 192+(color.blue >> 2)
        elif color.blue ==0:
            return 128+(color.green >> 2)

    elif color.green ==0 and color.blue ==0:
        return 64+(color.red >> 2)

    return (((color.red & 0xC0) >>2)|
            ((color.green & 0xC0) >>4)|
            ((color.blue & 0xC0) >> 6))



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

def isbackface(polypts):
    v1 = float(polypts[1][0] - polypts[0][0])
    v2 = float(polypts[1][1] - polypts[0][1])

    w1 = float(polypts[-1][0] - polypts[0][0])
    w2 = float(polypts[-1][1] - polypts[0][1])
    
    xproduct = v1*w2 - v2*w1 
    return xproduct > 0

def xform_and_project_poly(surface, xform4X4, polypts3d, colour = 0x00ff00,draw_hlines=False):
    plt = PygamePlotter(surface,default_colour=colour)
    polypts2d = []
    if True:
        txpolypts_array = []
        for pt in polypts3d:
            txpolypts_array.append(xformvec(xform4X4,pt))
        #if not isbackface(txpolypts_array):
        for txpolypt in txpolypts_array:
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
        # else:
        #     polypts2d = [Coord(0,0) for i in txpolypts_array]
    else:
        polypts2d = map(partial(gen_proj_pt,xform4X4=xform4X4), polypts3d)
    return fill_convex_poly(polypts2d,drawer=plt,colour=colour,draw_hlines=draw_hlines),isbackface(txpolypts_array)

spot0 = {'direction': numpy.array([ [-1], [-1], [-1], [1]]),
         'intensity': numpy.array([ [0.0], [0.75], [0.0], [1]]),}
spot1 = {'direction': numpy.array([ [1], [1], [-1], [1] ]),
         'intensity': numpy.array([ [0.0], [0.4], [0.0], [1.0]]),}
spot2 = {'direction': numpy.array([ [1], [0], [0], [1.0] ]),
         'intensity': numpy.array([ [0.0], [0.0], [0.6], [1.0]]),}

spot_data = [spot0, spot1, spot2]
spot_direction_world = [ [] for i in spot_data ]
spot_direction_view = [ [] for i in spot_data ] 

# #define DOT_PRODUCT(V1,V2) \
#    (FixedMul(V1.X,V2.X)+FixedMul(V1.Y,V2.Y)+FixedMul(V1.Z,V2.Z))
dot_product =lambda v1,v2: v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def set_spot_intensity(spot_idx, intensity):
    global spot_data
    spot_data[spot_idx]['intensity'][0] = intensity.red
    spot_data[spot_idx]['intensity'][1] = intensity.green
    spot_data[spot_idx]['intensity'][2] = intensity.blue

def set_spot_direction(spot_idx,  xform4X4):
    global spot_direction_world
    global spot_direction_view
    global spot_data
    spot_vec = spot_data[spot_idx]['direction']
    x_length = spot_vec[0]
    y_length = spot_vec[1]
    z_length = spot_vec[1]
    length = numpy.sqrt(x_length*x_length+y_length*y_length+z_length*z_length)
    spot_direction_world[spot_idx] = numpy.array([ [x_length/length], [y_length/length], [z_length/length], [1.0]])
    spot_direction_view[spot_idx] = xformvec(xform4X4, spot_direction_world[spot_idx])
    spot_direction_view[spot_idx][0] *= -1
    spot_direction_view[spot_idx][1] *= -1
    spot_direction_view[spot_idx][2] *= -1
    #print spot_direction_world, spot_direction_view

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
    set_spot_direction(0,worldviewxform)
    hlinesdata,is_behind_poly = xform_and_project_poly(surface, worldviewxform, vertices, draw_hlines=draw_hlines)
    if not draw_hlines:
        vals = hlinesdata.gettuples()
        temp_array = numpy.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))   
        '''
        stil calculates polys even if not facing... bad? unnecesary?
        '''
        color = ModelColor(255,255,255)
        if not is_behind_poly:
            y = hlinesdata.ystart
            for v in vals:
                x1, x2 = v
                if x1 > x2:                
                    temp_array[x2:x1,y].fill(model_colour_to_colour_index(color))
                else:
                    temp_array[x1:x2,y].fill(model_colour_to_colour_index(color))
                y += 1
        pygame.surfarray.blit_array(surface,temp_array)

clock = pygame.time.Clock()
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,8)

    running = True
    rotation = 0
    set_palette(screen)
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
