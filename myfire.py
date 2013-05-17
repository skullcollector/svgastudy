import pygame
import sys
import random
import numpy

from pygame.locals import *
width,height = 320,100

fire_array = numpy.zeros((width, height))
fire_surface = pygame.Surface((width,height),0,8)

def render_fire():
    global fire_array
    global fire_surface
    width,height = fire_array.shape

    temp_array = numpy.zeros((width, height))
    
    for x in range(0,width):
        for y in range(0,height):
            _left_of_current = int(fire_array[max(0,x-1), y])
            _right_of_current = int(fire_array[min(width-1,x+1),y])
            _above_current = int(fire_array[x,min(height-1, y+1)])
            _below_current = int(fire_array[x,max(0, y-1)])
            _above_index = max(0,y-1)
            fire_avg = ( _left_of_current + _right_of_current + _above_current + _below_current)/4
            temp_array[x, _above_index] = min(255, max(0,fire_avg))
            
    for x in range(0,width,2):
        fuel = min(255, max(0,fire_array[x,height-1] + random.randint(-20,34)))
        temp_array[x,height-1] = fuel

        temp_array[x+1,height-1] = fuel 

    fire_array = temp_array
    pygame.surfarray.blit_array(fire_surface,fire_array.astype('int') )    
    #return fire_surface
    
random.seed()
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def set_palette(surface):
    colours = numpy.ones((256,3))
    red,green,blue = 0,1,2
    colours[:,red] = numpy.arange(256)
    colours[:,green] = numpy.arange(256)
    #colours[:,blue] = numpy.arange(256)
    surface.set_palette(colours)

def main():
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

        screen.blit(fire_surface, (0,0))
        clock.tick(30)

        pygame.display.flip()

    pygame.quit()
  
if __name__=='__main__':
    main()
