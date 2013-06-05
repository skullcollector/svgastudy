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

surface = pygame.Surface((width,height),0,8)

class ModelColor (object):
    red = 0
    green = 0
    blue = 0

gamma4_levs = [0,39,53,63]
gamma64_levs = [ 0, 10, 14, 17, 19, 21, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34,
                 35, 36, 37, 37, 38, 39, 40, 41, 41, 42, 43, 44, 44, 45, 46, 46,
                 47, 48, 48, 49, 49, 50, 51, 51, 52, 52, 53, 53, 54, 54, 55, 55,
                 56, 56, 57, 57, 58, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63];

pblock = {}
def init_palette():
    global pblock
    for r in range(0,4):
        for g in range(0,4):
            for b in range(0,4):
                idx = (r<<4)+(g<<2)+b;
                #print r,g,b,hex(idx),idx
                pblock.update({idx: [gamma4_levs[r], gamma4_levs[g], gamma4_levs[b]] })
        for r in range(0,64):
            pblock.update({64+r: [gamma64_levs[r], 0,0] })

        for g in range(0,64):
            pblock.update({128+g: [0, gamma64_levs[g], 0] })

        for b in range(0,64):
            pblock.update({192+b: [0,0,gamma64_levs[b]] })

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

init_palette()
for i in pblock.items():
    print i

print len(gamma64_levs)

def render():
    pass

random.seed()
pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen.set_alpha(None)
clock = pygame.time.Clock()

def main():
    running = True
    #set_palette(fire_surface)
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
        screen.blit(surface, (0,0))  


        pygame.display.flip()

    pygame.quit()
  
if __name__=='__main__':
    main()
