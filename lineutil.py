from math import pi, sin, cos, sqrt, atan

class Coord:
    x = 0;
    y = 0;
    def __init__(self, x,y):
        self.x, self.y = x,y

    def __str__(self):
        return "<%d,%d>"%(self.x, self.y)

    def __repr__(self):
        return "<%d,%d>"%(self.x, self.y)

dxdy = lambda start,stop : (stop.x - start.x, stop.y - start.y)
close_enough = lambda actualpnt, calcpnt: sqrt((actualpnt.x-calcpnt.x)**2 + (actualpnt.y-calcpnt.y)**2) < 2

#------- Test helpers----

def gen_pts_with_gradient(gradient,start_coord=Coord(0,0),radius=10):
    # (Ystop-Ystart)/(Xstop-Xstart) = (y-Ystart)/(x-Xstart)
    # y = 1.0*(Ystop-Ystart)/(Xstop-Xstart)*(x-Xstart) + Ystart
    angle = atan(gradient)
    x,y = start_coord.x+int(round(radius*cos(angle))),start_coord.y+int(round(radius*sin(angle)))
    end_coord = Coord(x,y)
    return [start_coord, end_coord]


def print_gradient_example(gradient, radius=100, start_coord=Coord(0,0)):
    start,stop = gen_pts_with_gradient(gradient=gradient,radius=radius, start_coord=start_coord)
    dx,dy = dxdy(start,stop)
    M = 1.0*dy/dx
    print start,stop,M  


def testcases(gradient_list=[2,1.75,1.5,1.25,1,0.75,0.5,0.25,0.15], start_coord=Coord(0,0)):
    for grad in gradient_list:       
        yield gen_pts_with_gradient(grad, start_coord=start_coord)
              
#------------------------


class CharPlotter(object):
    def __init__(self, XDIM=50, YDIM=40, linefunc=lambda x,y: [(x,y) for i in range(0,10)]):
        self.XDIM = XDIM
        self.YDIM = YDIM
        self.line = linefunc
        self.buffer = ['.' for i in range(self.XDIM*self.YDIM)]

    def render(self):
        for y in range(0,self.YDIM):
            for x in range(0,self.XDIM):
                print self.buffer[x+y*self.YDIM],
            print

    def putchar(self,x,y,char):
        for i,c in enumerate(char):
            self.buffer[x+i+y*self.YDIM] = c

    def charline(self,pt1, pt2, marks=None):        
        aline = list(self.line(pt1,pt2))
        for i in aline:
            x,y = i 
            self.putchar(x,y,'*')
        if marks is None:
            self.putchar(pt1.x,pt1.y,'%s,%s>'%(pt1.x,pt1.y))
            self.putchar(pt2.x,pt2.y,'%s,%s<'%(pt2.y,pt2.y))
        else:
            self.putchar(pt1.x,pt1.y,'A')
            self.putchar(pt2.x,pt2.y,'B')
            
    def regupoly(self,points,marks=None):
        number_of_pnts = len(points)
        for i in range(0,number_of_pnts):
            self.charline(points[i], points[(i+1)%number_of_pnts],marks=marks)

    def create_npoly(self, **kwargs):
        x = getattr(kwargs,'x',20)
        y = getattr(kwargs,'y',20)
        
        corners = kwargs.get('num_of_corners',4)        
        radius =  kwargs.get('radius', 10)
        angle = lambda num : num*2*pi/(1.0*corners)
        output = []
        for corner in range(corners,0,-1):
            a = angle(corner)
            x,y = int(round(x+radius*cos(a))), int(round(y+radius*sin(a)))
            self.putchar(x,y,'@')
            output += [Coord(x,y)]
        return output
