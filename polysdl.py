import pygame
from pygame.locals import *
from gfxutil import *

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
    

def convexpoly_algo(surface):
    plt = PygamePlotter(surface,default_colour=0xff0000)
    output = plt.create_npoly(num_of_corners=9,radius=100,x=200,y=200);
    fill_convex_poly(output,drawer=plt)

def render(surface):
    #test_plotter(surface)
    convexpoly_algo(surface)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    running = True

    while running:
        
        render(screen)
        
        for event in pygame.event.get():
            if event.type == KEYDOWN: #QUIT:
                running = False
            else:
                print event
                
        #screen.fill((120, 120, 120))
        pygame.display.flip()
        
    pygame.quit()
  
if __name__=='__main__':
    main()
