import pygame
from pygame.locals import *
from gfxutil import *
from numpy import pi as nm_pi

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

def render(surface,rotation):
    #test_plotter(surface)
    convexpoly_algo(surface,rotation=rotation)

clock = pygame.time.Clock()

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    running = True
    rotation = 0
    
    while running:
        
        render(screen,rotation*pi/10)
        rotation += 1
        rotation = rotation % 10
        for event in pygame.event.get():
            if event.type == KEYDOWN: #QUIT:
                running = False
            else:
                print event
                

        pygame.display.flip()
        clock.tick(20)
        screen.fill((0,0,0))
        
    pygame.quit()
  
if __name__=='__main__':
    main()
