# From wiki and http://www.cs.helsinki.fi/group/goa/mallinnus/lines/bresenh.html
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

(x+1, y)    => newerror =  yreal-y     = error + M
OR
(x+1, y+1)  => newerror =  yreal-(y+1) = error + M - 1 

pick either based on smalles new error.

'''
pt1 = Coord(0,0)
pt2 = Coord(20,5)

dx,dy = dxdy(pt1, pt2)
start = pt1
stop = pt2
M = (1.0*dy)/dx

error = { 0 : lambda olderror: olderror + M,
          1 : lambda olderror: (olderror + M)-1}

y = start.y
olderror = 0
for x in range(start.x, stop.x):
    print x, y, olderror
    if error[0](olderror) < 0.5:
        olderror = error[0](olderror)
    else:   
        olderror = error[1](olderror)
        y = y+1

y = start.y
olderror = 0
for x in range(start.x, stop.x):
    print x, y, olderror
    if error[0](olderror) < 0.5:
        olderror = error[0](olderror)
    #else:   
    elif error[1](olderror) < 0.5:
        olderror = error[1](olderror)
        y = y+1

y = start.y
olderror = 0
for x in range(start.x, stop.x):
    print x, y, olderror
    if error[1](olderror) > 0.5:
        olderror = error[1](olderror)
        y = y+1
    else:
        olderror = error[0](olderror)
