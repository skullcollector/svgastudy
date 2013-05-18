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

fire_array = numpy.zeros((width, height))
fire_surface = pygame.Surface((width,height),0,8)

def render_fire():
    global fire_array
    global fire_surface
    width,height = fire_array.shape

    temp_array = numpy.zeros((width, height))    
    for x in range(0,width):
        for y in range(0,height):

            x_test = x-1 if x-1 > 0 else 0
            #_left_of_current = int(fire_array.item(max(0,x-1), y))
            _left_of_current = fire_array.item(x_test, y)

            x_test = x+1 if x+1 < width-1 else width-1
            #_right_of_current = int(fire_array.item(min(width-1,x+1),y))
            _right_of_current = fire_array.item(x_test,y)

            y_test = y+1 if y+1 < height-1 else height-1
            #_above_current = int(fire_array.item(x,min(height-1, y+1)))
            _above_current = fire_array.item(x,y_test)

            y_test = y-1 if y > 1 else 0
            #_below_current = int(fire_array.item(x,max(0, y-1)))
            _below_current = fire_array.item(x,y_test)

            _above_index = y-1 if y > 1 else 0
            #_above_index = max(0,y-1)
            fire_avg = ( _left_of_current + _right_of_current + _above_current + _below_current)/4 - 1
            #temp_array.itemset(x, _above_index , min(255, max(0,fire_avg)) )
            fire_avg = fire_avg if fire_avg > 0 else 0
            fire_avg = 255 if fire_avg > 255 else fire_avg
            temp_array.itemset(x, _above_index , fire_avg )

    if False:

        for x in range(0,width,2):   # replace this with some matrix op perhaps?
            fuel = fire_array.item(x,height-1) + numpy.random.randint(-30,30)
            fuel = fuel if fuel > 0 else 0
            fuel = fuel if fuel < 255 else 255
            #fuel = min(255, max(0,fire_array.item(x,height-1) + numpy.random.randint(-30,30)))
            temp_array.itemset(x,height-1, fuel)

            temp_array.itemset(x+1,height-1, fuel )
    else:
        if True:            
            # #fire_array[:,height-1] = numpy.sum([fire_array[:,height-1:], numpy.random.randint(-30,30,width)])
            #fuel = fire_array
            # for c,f in enumerate(fuel):
            #     #print c,c, f
            #     fuel[c,height-1] += numpy.random.randint(-30,30)
            randints = numpy.random.randint(-30,40,width)
            #print len(randints), len(temp_array[:,height-1]), randints, temp_array[:,height-1]
            fire_array[:,height-1] = numpy.sum([fire_array[:,height-1], randints], axis=0)
        else:
            fuel = fire_array
            for c,f in enumerate(fuel):
                #print c,c, f
                fuel[c,height-1] += numpy.random.randint(-30,30)
        for x in range(0,width,2):   # replace this with some matrix op perhaps?
            #fuel = fire_array.item(x,height-1) + numpy.random.randint(-30,30)
            fuel = fire_array.item(x,height-1)
            fuel = fuel if fuel > 0 else 0
            fuel = fuel if fuel < 255 else 255
            #fuel = min(255, max(0,fire_array.item(x,height-1) + numpy.random.randint(-30,30)))
            temp_array.itemset(x,height-1, fuel)

            temp_array.itemset(x+1,height-1, fuel )

        
    fire_array = temp_array
    #pygame.surfarray.blit_array(fire_surface,temp_array.astype('int') )    
    pygame.surfarray.blit_array(fire_surface,temp_array )    
    #return fire_surface
    
random.seed()
pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen.set_alpha(None)
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
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    t = True
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

        # pos = (0, 0)
        # fire_surface1 = pygame.transform.scale(fire_surface, (DISPLAY_WIDTH,DISPLAY_HEIGHT))
        # for i in range(0, 4, 2):
        #     #screen.blit(fire_surface1, (pos[0] + fire_surface.get_width()*i, pos[1]))
        #     screen.blit(fire_surface1, (pos[0] ,  pos[1]))

        #clock.tick(20)

        pygame.display.flip()

    pygame.quit()
  
if __name__=='__main__':
    main()
