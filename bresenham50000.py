class Coord:
    x = 0;
    y = 0;
    def __init__(self, x,y):
        self.x, self.y = x,y

    def __str__(self):
        return "<%d,%d>"%(self.x, self.y)


dxdy = lambda start,stop : (stop.x - start.x, stop.y - start.y)

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

    # if (dx < 0 and dy > 0):
    #     x,y = p[1].x, p[1].y
    #     dx,dy = -dx, -dy

    # if (dx < 0 and dy > 0):
    #     x,y = p[1].x, p[1].y
    #     dx,dy = -dx, -dy
    
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

