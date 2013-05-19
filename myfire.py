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

# Speed up attempt:Removed random from the loop.. negligible.
random_strings = [ numpy.random.randint(-30,30,width) for i in range(40)]
random_string_idx = 0

fire_array = numpy.zeros((width, height))
fire_surface = pygame.Surface((width,height),0,8)

def render_fire():
    global fire_array
    global fire_surface
    global random_strings
    global random_string_idx
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
            
    #randints = numpy.random.randint(-30,30,width)
    randints = random_strings[random_string_idx]
    random_string_idx = (random_string_idx+1) % len(random_strings)
    fire_array[:,height-1] = numpy.sum([fire_array[:,height-1], randints], axis=0)
    for x in range(0,width,2):   # replace this with some matrix op perhaps?
        #fuel = fire_array.item(x,height-1) + numpy.random.randint(-30,30)
        fuel = fire_array.item(x,height-1)
        fuel = fuel if fuel > 0 else 0
        fuel = fuel if fuel < 255 else 255
        temp_array.itemset(x,height-1, fuel)        
        temp_array.itemset(x+1,height-1, fuel )

        
    fire_array = temp_array
    #pygame.surfarray.blit_array(fire_surface,temp_array.astype('int') )    
    pygame.surfarray.blit_array(fire_surface,fire_array )    
    #return fire_surface
    
random.seed()
pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen.set_alpha(None)
clock = pygame.time.Clock()



def set_palette(surface):
    gstep, bstep = 75, 150
    cmap = numpy.zeros((256, 3))
    red,green,blue = 0,1,2
    cmap[:, red] = numpy.minimum(numpy.arange(256) * 3, 255)
    cmap[gstep:, green] = cmap[:-gstep, red]
    cmap[bstep:, blue] = cmap[:-bstep, red]
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
