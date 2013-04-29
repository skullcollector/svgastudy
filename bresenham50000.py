class Coord:
    x = 0;
    y = 0;
    def __init__(self, x,y):
        self.x, self.y = x,y

    def __str__(self):
        return "<%d,%d>"%(self.x, self.y)


dxdy = lambda start,stop : (stop.x - start.x, stop.y - start.y)


def octant_super_45(x,y,dx,dy,xdir,ydir,error,debug=False):
    
    current_error = 0
    while dy > 0:
        dy -= 1 
        y += ydir
        if error[0](current_error) < 0.5:
            current_error = error[0](current_error)
        else:
            current_error = error[1](current_error)
            x += xdir
        if debug:
            yield x,y, current_error
        else:
            yield x,y


def octant_sub_45(x,y,dx,dy,xdir,ydir,error,debug=False):
    
    current_error = 0
    while dx > 0:
        dx -= 1 
        x += xdir
        if error[0](current_error) < 0.5:
            current_error = error[0](current_error)
        else:
            current_error = error[1](current_error)
            y += ydir
        if debug:
            yield x,y, current_error
        else:
            yield x,y

pts = [[Coord(20,20), Coord(40,30)],
       [Coord(40,30), Coord(20,20)],
       [Coord(20,20), Coord(0,10)],]

for p in pts:
    dx,dy = dxdy(*p)
    M = 1.0*dy/dx
    xdir =1
    x,y = p[0].x, p[0].y
    if dx < 0 and dy < 0:
        x,y = p[1].x, p[1].y
        xdir = 1
        dx,dy = -dx, -dy

    error = { 0: lambda eps: eps + M,
              1: lambda eps: eps + M -1}
    ydir = 1
    l =list(octant_sub_45(x,y,dx,dy,xdir,ydir, error,debug=True))
    print M,dx,dy,l[0],l[-1]

print "Negative gradients"
pts = [[Coord(20,20), Coord(40,10)],
       [Coord(40,10), Coord(20,20)],
       ]
for p in pts:
    dx,dy = dxdy(*p)
    M = abs(1.0*dy/dx)
    xdir =1
    x,y = p[0].x, p[0].y
    if (dx < 0 and dy > 0):
        x,y = p[1].x, p[1].y
        dx,dy = -dx, -dy

    error = { 0: lambda eps: eps + M,
              1: lambda eps: eps + M -1}
    ydir = -1
    l =list(octant_sub_45(x,y,dx,dy,xdir,ydir, error,debug=True))
    print M,dx,dy,l[0],l[-1]

print " again.."
pts = [[Coord(20,20), Coord(40,30)],
       [Coord(40,30), Coord(20,20)],
       [Coord(20,20), Coord(0,10)],
       [Coord(20,20), Coord(40,10)],
       [Coord(40,10), Coord(20,20)],]

for p in pts:
    dx,dy = dxdy(*p)
    M = abs(1.0*dy/dx)
    xdir =1
    x,y = p[0].x, p[0].y

    if dx < 0:
        x, y = p[1].x, p[1].y
        dx, dy = -dx, -dy
    
    ydir = 1
    if dy < 0:
        ydir = -1

    error = { 0: lambda eps: eps + M,
              1: lambda eps: eps + M -1}

    l =list(octant_sub_45(x,y,dx,dy,xdir,ydir, error,debug=True))
    print p[0],p[1],M,dx,dy,l[0],l[-1]

print "....."
pts = [[Coord(30,40), Coord(20,20)],
       [Coord(20,20), Coord(30,40)],
       [Coord(20,20), Coord(0,1)],
       [Coord(20,20), Coord(0,5)], 
       [Coord(20,20), Coord(0,40)],
       [Coord(0,40), Coord(20,20)],
       [Coord(20,20), Coord(10,0)]      ]

for p in pts:
    dx,dy = dxdy(*p)
    M = abs(1.0*dx/dy)
    xdir =1
    x,y = p[0].x, p[0].y

    if dy < 0:
        x, y = p[1].x, p[1].y
        dx, dy = -dx,-dy
        ydir = 1

    xdir = 1
    if dx < 0:
        xdir = -1

    error = { 0: lambda eps: eps + M,
              1: lambda eps: eps + M -1}

    l =list(octant_super_45(x,y,dx,dy,xdir,ydir, error,debug=True))
    print M,dx,dy,l[0],l[-1]


def theline0(start,stop, debug=False):    
    dx,dy = dxdy(start,stop)

    if dy ==0 and dx == 0:
        return None
    
    if dx == 0:
        # vertical
        return [ (start.x, y) for y in range(*[int(round(i))+1 for i in sorted([start.y,stop.y])])]

    if dy == 0:
        # vertical
        return [ (x, start.y) for x in range(*[int(round(i))+1 for i in sorted([start.x,stop.x])])]

    if dx > dy:
        M = abs(1.0*dy/dx)
        xdir =1
        x,y = p[0].x, p[0].y
    
        if dx < 0:
            x, y = p[1].x, p[1].y
            dx, dy = -dx, -dy
    
        ydir = 1
        if dy < 0:
            ydir = -1
    
        error = { 0: lambda eps: eps + M,
                  1: lambda eps: eps + M -1}
    
        return list(octant_sub_45(x,y,dx,dy,xdir,ydir, error,debug=debug))
    else:
        M = abs(1.0*dx/dy)
        xdir =1
        ydir = 1
        x,y = p[0].x, p[0].y
        
        if dy < 0:
            x, y = p[1].x, p[1].y
            dx, dy = -dx,-dy
            ydir = 1
        
        xdir = 1
        if dx < 0:
            xdir = -1
        
        error = { 0: lambda eps: eps + M,
                  1: lambda eps: eps + M -1}
        
        return list(octant_super_45(x,y,dx,dy,xdir,ydir, error,debug=debug))


print "try it agaqin..."
pts = [[Coord(30,40), Coord(20,20)],
       [Coord(20,20), Coord(30,40)],
       [Coord(20,20), Coord(0,1)],
       [Coord(20,20), Coord(0,5)], 
       [Coord(20,20), Coord(0,40)],
       [Coord(0,40), Coord(20,20)],
       [Coord(20,20), Coord(10,0)]      ]

for p in pts:
    l = theline0(*p)
    print p[0],p[1],l[0],l[-1],len(l)
print "rotate test"
from math import pi, sin, cos
MAX_CORNERS = 6
CORNER_ANGLE = 2*pi/MAX_CORNERS
CENTER = Coord(20,20)
RADIUS = 10
morecases = []
for corner in range(0,MAX_CORNERS):
    corner = corner*CORNER_ANGLE
    rcs, rsn = CENTER.x+RADIUS*cos(corner), CENTER.y+RADIUS*sin(corner)
    morecases.append([CENTER,Coord(rcs, rsn)])
for p in morecases:
    l = theline0(*p)
    print p[0],p[1],l[0],l[-1],len(l)

#import pdb;pdb.set_trace()
print theline0(*morecases[-1])
# print "move by 60 degrees"
# MAX_CORNERS = 6
# offset = 0 # pi/6
7# CORNER_ANGLE = 2*pi/MAX_CORNERS
# CENTER = Coord(20,20)
# RADIUS = 10
# morecases = []
# for corner in range(0,MAX_CORNERS):
#     corner = corner*CORNER_ANGLE
#     rcs, rsn = int(round(CENTER.x+RADIUS*cos(offset+corner))), int(round(CENTER.y+RADIUS*sin(offset+corner)))
#     morecases.append([CENTER,Coord(rcs, rsn)])



XDIM,YDIM = 50,40
buffer = ['.' for i in range(XDIM*YDIM)]
def putchar(x,y,char):
    global XDIM
    x = int(round(x))
    y = int(round(y))
    buffer[x+y*YDIM] = char

pt1,pt2 = Coord(10,10), Coord(20,20)
def charline(pt1, pt2):
    aline = list(theline0(pt1,pt2))
    for i in aline:
        x,y = i 
        putchar(x,y,'*')
    putchar(pt1.x,pt1.y,'X')
    putchar(pt2.x,pt2.y,'Q')


crds = [Coord(10,10),
        Coord(10,20),
        Coord(20,20),
        Coord(20,10)]

# CLEN = len(crds)
# for i in range(0,CLEN):
#     #print crds[i], crds[(i+1)%CLEN]
#     charline(crds[i],crds[(i+1)%CLEN])

def regupoly(points):
    number_of_pnts = len(points)
    for i in range(0,number_of_pnts):
        charline(points[i], points[(i+1)%number_of_pnts])

#regupoly(crds)
#--------- random shape drawer
from math import pi, sin, cos
corners = 6
center = Coord(20,20)
radius = 10
angle = lambda num : num*2*pi/(1.0*corners)
output = []
for corner in range(0,corners):
    a = angle(corner)
    x,y = (center.x+radius*cos(a)), (center.y+radius*sin(a))
    putchar(x,y,'@')
    output += [Coord(x,y)]
for o in output:
    print o

regupoly(output)
#--------- print the "backbuffer" of chars

for y in range(0,YDIM):
    for x in range(0,XDIM):
        print buffer[x+y*YDIM],
    print
