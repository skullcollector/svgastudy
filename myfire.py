import pygame
import sys
import random
import numpy

from pygame.locals import *
width,height = 320,200


# def init_fire(width = 640, height=480):
#     fire_array = numpy.zeros((width, height))
#     fire_surface = pygame.Surface((width,height),0,8)

#     return  fire_array,fire_surface
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
            fire_avg = sum([ _left_of_current + _right_of_current + _above_current + _below_current])/4 
            temp_array[x, _above_index] = min(255, max(0,fire_avg))
            
    for x in range(0,width,2):
        temp_array[x,height-1] += random.randint(100,255)

        temp_array[x+1,height-1] = temp_array[x,height-1]

    fire_array = temp_array
    pygame.surfarray.blit_array(fire_surface,fire_array.astype('int') )    
    return fire_array,fire_surface
    
random.seed()
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def main():
    running = True
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
