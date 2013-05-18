import pygame
import sys
import random
import numpy

from pygame.locals import *


DISPLAY_WIDTH, DISPLAY_HEIGHT = 320,200
if False:
    width,height = 60,40
else:
    width,height = DISPLAY_WIDTH, DISPLAY_HEIGHT

fire_array = numpy.zeros((width, height))
fire_surface = pygame.Surface((width,height),0,8)

def render_fire():
    global fire_array
    global fire_surface
    width,height = fire_array.shape

    temp_array = numpy.zeros((width, height))
    
    for x in range(0,width):
        for y in range(0,height):
            _left_of_current = int(fire_array.item(max(0,x-1), y))
            _right_of_current = int(fire_array.item(min(width-1,x+1),y))
            _above_current = int(fire_array.item(x,min(height-1, y+1)))
            _below_current = int(fire_array.item(x,max(0, y-1)))
            _above_index = max(0,y-1)
            fire_avg = ( _left_of_current + _right_of_current + _above_current + _below_current)/4 -2
            temp_array.itemset(x, _above_index , min(255, max(0,fire_avg)) )
            
    for x in range(0,width,2):
        fuel = min(255, max(0,fire_array.item(x,height-1) + numpy.random.randint(-30,30)))
        temp_array.itemset(x,height-1, fuel)

        temp_array.itemset(x+1,height-1, fuel )

    fire_array = temp_array
    #pygame.surfarray.blit_array(fire_surface,temp_array.astype('int') )    
    pygame.surfarray.blit_array(fire_surface,temp_array )    
    #return fire_surface
    
random.seed()
pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT),0,8)
clock = pygame.time.Clock()

def set_palette(surface):
    # colours = numpy.ones((256,3))
    # red,green,blue = 0,1,2
    # colours[:,red] = numpy.arange(256)
    # colours[:,green] = numpy.arange(256)
    # #colours[:,blue] = numpy.arange(256)
    # surface.set_palette(colours)

    gstep, bstep = 75, 150
    cmap = numpy.zeros((256, 3))
    cmap[:, 0] = numpy.minimum(numpy.arange(256) * 3, 255)
    cmap[gstep:, 1] = cmap[:-gstep, 0]
    cmap[bstep:, 2] = cmap[:-bstep, 0]
    for i in enumerate(cmap):
        print i
    surface.set_palette(cmap)

'''
 question: How does the pygame guys manage to make fast fire effect?
 answer: They cheat.
 make a 40X40 image of flames, then scale it!

'''
def main():
    global fire_surface
    running = True
    set_palette(fire_surface)
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type==KEYUP: #QUIT:
                running = False                
            else:
                print event

        #fire_array,fire_surface = render_fire(fire_array,fire_surface)
        render_fire()
        
        '''
        to see the original image
        '''
        screen.blit(fire_surface, (0,0))  

        pos = (0, 0)
        fire_surface1 = pygame.transform.scale(fire_surface, (DISPLAY_WIDTH,DISPLAY_HEIGHT))
        for i in range(0, 4, 2):
            #screen.blit(fire_surface1, (pos[0] + fire_surface.get_width()*i, pos[1]))
            screen.blit(fire_surface1, (pos[0] ,  pos[1]))

        clock.tick(30)

        pygame.display.flip()

    pygame.quit()
  
if __name__=='__main__':
    main()
