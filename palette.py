# CHapter 55 of the Graphics programming black book M Abrash
# I dont get it completely yet. Mostly just copied
#

import pygame
import sys
import random
import numpy

from pygame.locals import *


DISPLAY_WIDTH, DISPLAY_HEIGHT = 1024,800
if True:
    width,height = DISPLAY_WIDTH/4,DISPLAY_HEIGHT/8
else:
    width,height = DISPLAY_WIDTH, DISPLAY_HEIGHT

fsurface = pygame.Surface((width,height),0,8)
farray = numpy.zeros((width, height))

class ModelColor (object):
    red = 0
    green = 0
    blue = 0

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

    # for i in cmap:
    #     print i
        
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

print len(gamma64_levs)

def render():
    global farray
    global fsurface
    width, height = farray.shape
    temp_array = numpy.zeros((width, height))    

    col = 0
    for x in range(0,width):
        for y in range(0,height):
            temp_array.itemset(x,y,col) 
        col += 1

    farray = temp_array
    pygame.surfarray.blit_array(fsurface,farray )    


random.seed()
pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen.set_alpha(None)
clock = pygame.time.Clock()

def main():
    global fsurface
    running = True
    set_palette(fsurface)
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    t = True    
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type==KEYUP: #QUIT:
                running = False                
            else:
                print event

        #fire_array,fire_surface = render_fire(fire_array,fire_surface)
        render()
        
        '''
        to see the original image
        '''
        screen.blit(fsurface, (0,0))  

        pygame.display.flip()

    pygame.quit()
  
if __name__=='__main__':
    main()
    
