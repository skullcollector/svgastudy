from math import pi, sin, cos

class Coord:
    x = 0;
    y = 0;
    def __init__(self, x,y):
        self.x, self.y = x,y

    def __str__(self):
        return "<%d,%d>"%(self.x, self.y)


dxdy = lambda start,stop : (stop.x - start.x, stop.y - start.y)


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
