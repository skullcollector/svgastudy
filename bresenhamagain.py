# Based on info from wiki and http://www.cs.helsinki.fi/group/goa/mallinnus/lines/bresenh.html
#
# He split it into octants...
#
class Coord:
    x = 0;
    y = 0;
    def __init__(self, x,y):
        self.x, self.y = x,y

    def __str__(self):
        return "<%d,%d>"%(self.x, self.y)


dxdy = lambda start,stop : (stop.x - start.x, stop.y - start.y)

'''
point chosen now is x,y.
x, y are int. xreal and yreal follow:
              yreal = M * xreal + b

So now we have:

(x, y)      => yreal-y  = error

For new points we have 2 possible error values based on 2 possible choices for the new Y:

(x+1, y)    => newerror =  yreal-y     = olderror + M
OR
(x+1, y+1)  => newerror =  yreal-(y+1) = olderror + M - 1 

pick either based on smalles new error.

'''
pt1 = Coord(0,0)
pt2 = Coord(20,5)


def line0(start, stop, debug = False):
    dx,dy = dxdy(start, stop)
    M = (1.0*dy)/dx

    error = { 0 : lambda olderror: olderror + M,
              1 : lambda olderror: (olderror + M)-1}

    y = start.y
    olderror = 0
    for x in range(start.x, stop.x):
        if debug:
            yield x, y, olderror
        else:
            yield x,y
        if error[0](olderror) < 0.5:
            olderror = error[0](olderror)
        else:
            olderror = error[1](olderror)
            y = y+1

def line1(start, stop, debug = False):
    dx,dy = dxdy(start, stop)
    M = (1.0*dy)/dx

    error = { 0 : lambda olderror:  (olderror + M),    # x,y   below yreal  by    error+M
              1 : lambda olderror: (olderror + M)-1}   # x,y+1 above yreal  by 1-(error+M)

    y = start.y
    olderror = 0
    for x in range(start.x, stop.x):
        if debug:            
            yield x, y, olderror
        else:
            yield x,y
        if abs(error[0](olderror)) < 0.5 :
            olderror = error[0](olderror)
            continue
        else:
            olderror = error[1](olderror)
            y = y+1
            continue


#Snippet from  M Abrash's code:
#  http://www.phatcode.net/res/224/files/html/ch36/36-01.html

# void Octant0(X0, Y0, DeltaX, DeltaY, XDirection)
# unsigned int X0, Y0;          /* coordinates of start of the line */
# unsigned int DeltaX, DeltaY;  /* length of the line (both > 0) */
# int XDirection;               /* 1 if line is drawn left to right,
#                                  -1 if drawn right to left */
# {
#    int DeltaYx2;
#    int DeltaYx2MinusDeltaXx2;
#    int ErrorTerm;
#    /* Set up initial error term and values used inside drawing loop */
#    DeltaYx2 = DeltaY * 2;
#    DeltaYx2MinusDeltaXx2 = DeltaYx2 - (int) ( DeltaX * 2 );
#    ErrorTerm = DeltaYx2 - (int) DeltaX;

#    /* Draw the line */
#    EVGADot(X0, Y0);              /* draw the first pixel */
#    while ( DeltaX-- ) {
#       /* See if it's time to advance the Y coordinate */
#       if ( ErrorTerm >= 0 ) {
#          /* Advance the Y coordinate & adjust the error term
#             back down */
#          Y0++;
#          ErrorTerm += DeltaYx2MinusDeltaXx2;
#       } else {
#          /* Add to the error term */
#          ErrorTerm += DeltaYx2;
#       }
#       X0 += XDirection;          /* advance the X coordinate */
#       EVGADot(X0, Y0);           /* draw a pixel */
#    }
# }
# def oct0(x,y, delx,dely, xdir):
#     delmod = dely*2 - delx*2
#     delmod2 = dely*2
#     error = dely*2 - delx
    
#     while delx > 0:
#         delx -= 1
#         if error >= 0:
#             y += 1
#             error += delmod
#         else:
#             error += delmod2
#         x += xdir
#         yield (x,y)


# let me try something like this...
def oct0(x,y,dx, dy, xdir,ydir, debug=False):
    M = 1.0*dy/dx  # I still use floats... for now.
    error = { 0 : lambda olderror:  (olderror + M),    # x,y   below yreal  by    error+M
              1 : lambda olderror: (olderror + M)-1}   # x,y+1 above yreal  by 1-(error+M)

    cur_error=0

    while dx > 0:
        dx -= 1
        if error[0](cur_error) < 0.5:
            cur_error = error[0](cur_error)
        else:
            cur_error = error[1](cur_error)
            y += ydir
        x += xdir
        if debug:
            yield x, y, cur_error
        else:
            yield x,y

def oct1(x,y,dx, dy,xdir, ydir, debug=False):
    M = 1.0*dx/dy
    error = { 0 : lambda olderror:  (olderror + M),    # x,y   below yreal  by    error+M
              1 : lambda olderror: (olderror + M)-1}   # x,y+1 above yreal  by 1-(error+M)

    cur_error = 0
    while dy > 0:
        dy -= 1
        if error[0](cur_error) < 0.5:
            cur_error = error[0](cur_error)
        else:
            cur_error = error[1](cur_error)
            x += xdir
        y += ydir       
        if debug:
            yield x, y, cur_error
        else:
            yield x,y
    
def line2(start, stop, debug=False):        
    dx,dy = dxdy(start, stop)
    
    # error = { 0 : lambda olderror:  (olderror + M),    # x,y   below yreal  by    error+M
    #           1 : lambda olderror: (olderror + M)-1}   # x,y+1 above yreal  by 1-(error+M)
    

    xincr = -1 if dx < 0 else 1
    yincr = -1 if dy < 0 else 1
    if dx < 0:
        dx = -dx
        x,y = stop.x, stop.y        
    else:
        x,y = start.x, start.y        

    if dy < 0:
        dy = -dy
        x,y = stop.x, stop.y        
    else:
        x,y = start.x, start.y        

    # if dx ==0:
    #     return [(x, yy) for yy in range(y,y+dy,yincr)]

    # if dy ==0:
    #     return [(xx, y) for xx in range(x+dx,x,xincr)]

    if dx > dy:
        return oct0(x, y, dx,dy, xincr,yincr, debug=debug)
    else:
        return oct1(x, y, dx,dy, xincr,yincr, debug=debug)
        

from math import sqrt
cases = [ [Coord(20,20), Coord(40,30)],
          [Coord(20,20), Coord(40,35)],
          [Coord(20,20), Coord(30,40)],   # next anticlock octant
          [Coord(20,20), Coord(10,40)],
          [Coord(20,20), Coord(0,30)]]
swap = lambda testcasepoints: [testcasepoints[1], testcasepoints[0]]
close_enough = lambda actualpnt, calcpnt: sqrt((actualpnt.x-calcpnt.x)**2 + (actualpnt.y-calcpnt.y)**2) < 2
def test(linefunc,testcases, stopidx=-1):
    for idx,testcase in enumerate(testcases):
        if idx == stopidx:
            break;
        try:
            lastelem = list(linefunc(*testcase, debug=True))[-1]
            howclose = "close enough " if close_enough (testcase[-1], Coord(*lastelem[:-1])) else "too far away"
            lastelem = list(lastelem) + [howclose]
        except Exception,ex:
            print ex
            lastelem = "no luck for couple", str(testcase[0]), str(testcase[1])
        dx, dy = dxdy(*testcase)
        M = (1.0*dy)/dx
        print testcase[0], testcase[1], M, lastelem

stopidx = 2
test(line0,cases,stopidx=stopidx)
test(line1,cases,stopidx=stopidx)

for i in line1(*cases[1], debug=True):
    print i
test(line2,cases)

from math import pi, sin, cos
print "now rotate a few times"
MAX_CORNERS = 6
CORNER_ANGLE = 2*pi/MAX_CORNERS
CENTER = Coord(20,20)
RADIUS = 10
morecases = []
for corner in range(0,MAX_CORNERS):
    corner = corner*CORNER_ANGLE
    rcs, rsn = CENTER.x+RADIUS*cos(corner), CENTER.y+RADIUS*sin(corner)
    morecases.append([CENTER,Coord(rcs, rsn)])
test(line2, morecases)
print "move by 60 degrees"
MAX_CORNERS = 6
offset = 0 # pi/6
CORNER_ANGLE = 2*pi/MAX_CORNERS
CENTER = Coord(20,20)
RADIUS = 10
morecases = []
for corner in range(0,MAX_CORNERS):
    corner = corner*CORNER_ANGLE
    rcs, rsn = int(round(CENTER.x+RADIUS*cos(offset+corner))), int(round(CENTER.y+RADIUS*sin(offset+corner)))
    morecases.append([CENTER,Coord(rcs, rsn)])
test(line2, morecases)
