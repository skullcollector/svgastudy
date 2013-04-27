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


# now how about some int math in stead?
'''
Error value was 
newerror0 = olderror + M    = olderror + dy/dx
newerror1 = olderror + M -1 = olderror + dy/dx -1

now we take away the division:

newerror0 = olderror*dx + M*dx     = olderror*dx + dy
newerror1 = olderror*dx + M*dx -dx = olderror*dx + dy - dx

Now the Helsinki guys redefined their error' value as olderror'*dx

so now the values area;

newerror0' = olderror' + dx     
newerror1' = olderror' + dy -dx 

this part I did wrong initially. I had it as follows:
    if 2*error_int[0](olderror) < dx:
        olderror = 2*error_int[0](olderror) 
    else:   
        olderror = 2*error_int[1](olderror) 
        y = y+1

in the end the error' value stays the error value, the test just changed.

'''
print 'attempt A) int,'*20
dx,dy = dxdy(pt1, pt2)
start = pt1
stop = pt2
#M = (1.0*dy)/dx
# error = { 0 : lambda olderror: olderror + M,
#           1 : lambda olderror: (olderror + M)-1}

 
error_int = { 0 : lambda olderror: olderror + dy,
              1 : lambda olderror: olderror + dy-dx}


y = start.y
olderror = dx*0;
for x in range(start.x, stop.x):
    print x, y, olderror
    if 2*error_int[0](olderror) < dx:
        olderror = error_int[0](olderror) #olderror +dy
    else:   
        olderror = error_int[1](olderror) #olderror +dy -dx
        y = y+1

print pt1, pt2, dx, dy
# other octants:
# error = { 0 : lambda olderror: olderror + M,
#           1 : lambda olderror: (olderror + M)+1}
print 'attempt B) int)'*20

pt1 = Coord(40,0)
pt2 = Coord(20,5)
dx,dy = dxdy(pt1, pt2)
start = pt1
stop = pt2
error_int = { 0 : lambda olderror: olderror + dy,
              1 : lambda olderror: olderror + dy+dx}

y = start.y
olderror = dx*0;
for x in range(start.x, stop.x,-1):
    print x, y, olderror
    if 2*error_int[0](olderror) < dx: # mmmm not what the website said..  error_int[0](olderror) > -dx... see attempt C
    #if -1*2*error_int[0](olderror) < dx:
        olderror = error_int[0](olderror) #olderror +dy
    else:   
        olderror = error_int[1](olderror) #olderror +dy +dx
        y = y+1

print pt1, pt2, dx, dy
'''
Above mystery solved: I picked the wrong coords for the website example... 
the following should be more correct...
'''
print 'attempt C) int,'*20  # mystery solved..

pt1 = Coord(0,5)
pt2 = Coord(20,2)
dx,dy = dxdy(pt1, pt2)
start = pt1
stop = pt2
error_int = { 0 : lambda olderror: olderror + dy,
              1 : lambda olderror: olderror + dy+dx}

y = start.y
olderror = dx*0;
for x in range(start.x, stop.x,1):
    print x, y, olderror
    if 2*error_int[0](olderror) > -dx: # OH HERE WE GO!
    #if -1*2*error_int[0](olderror) < dx:
        olderror = error_int[0](olderror) #olderror +dy
    else:   
        olderror = error_int[1](olderror) #olderror +dy +dx
        y = y-1

print pt1, pt2, dx, dy

print 'refactor '*20

'''
mmmm not sure why the error looks like this now... 
I wanted to make attempt C fit with the form of attempt A, B
In order to do so however, I multiplied everything with -1,
moved -1 into the error functions.

BUT shouldnt the error functions be -olderror -dy and -olderror-dy-dx?

That doesnt work with the refactor though ... 
'''
pt1 = Coord(0,5)
pt2 = Coord(200,4)
dx,dy = dxdy(pt1, pt2)
start = pt1
stop = pt2
error_int = { 0 : lambda olderror: olderror - dy,
              1 : lambda olderror: olderror - dy-dx}

y = start.y
olderror = dx*0;
for x in range(start.x, stop.x,1):
    print x, y, olderror
    if 2*error_int[0](olderror) < dx: # OH HERE WE GO!
        olderror = error_int[0](olderror) #olderror +dy
    else:   
        olderror = error_int[1](olderror) #olderror +dy +dx
        y = y-1

print pt1, pt2, dx, dy

print 'refactor2 '*20

def xline(start, stop):
    '''
    only covers half the octants...
    '''
    dx,dy = dxdy(start, stop)
    xincr = -1 if dx < 0 else 1
    yincr = -1 if dy < 0 else 1
    
    error_function_pos_dy = { 0: lambda old_error: old_error + dy,
                              1: lambda old_error: old_error + dy - dx }
    
    error_function_neg_dy = { 0: lambda old_error: old_error - dy,
                              1: lambda old_error: old_error - dy - dx }

    error_function = error_function_pos_dy if yincr == 1 else error_function_neg_dy

    y = start.y
    olderror = 0;
    for x in range(start.x, stop.x,xincr):
        yield (x,y)
        if 2*error_function[0](olderror) < dx:
            olderror = error_function[0](olderror)
        else:   
            olderror = error_function[1](olderror) 
            y = y + yincr

pt1 = Coord(0,5)
pt2 = Coord(200,4)
print pt1,pt2,list(xline(pt1, pt2))[-1]
pt1 = Coord(0,5)
pt2 = Coord(20,2)
print pt1,pt2,list(xline(pt1, pt2))[-1]

pt1 = Coord(0,0)
pt2 = Coord(20,5)
print pt1,pt2,list(xline(pt1, pt2))[-1]


print 'refactor.. what if the line is y dominant? '*20
'''
this should cover the other octants...
'''        
def yline(start, stop):
    ''' 
    covers half of the octants
    '''
    dx,dy = dxdy(start, stop)
    xincr = -1 if dx < 0 else 1
    yincr = -1 if dy < 0 else 1
    
    error_function_pos_dy = { 0: lambda old_error: old_error + dx,
                              1: lambda old_error: old_error + dx - dy }
    
    error_function_neg_dy = { 0: lambda old_error: old_error - dx,
                              1: lambda old_error: old_error - dx - dy }

    error_function = error_function_pos_dy if xincr == 1 else error_function_neg_dy

    x = start.x
    olderror = 0;
    for y in range(start.y, stop.y,yincr):
        yield (x,y)
        if 2*error_function[0](olderror) < dy:
            olderror = error_function[0](olderror)
        else:   
            olderror = error_function[1](olderror) 
            x = x + xincr

pt1 = Coord(0,5)
pt2 = Coord(22,400)
print pt1,pt2,list(yline(pt1, pt2))[-1]
pt1 = Coord(10,5)
pt2 = Coord(4,200)
print pt1,pt2,list(yline(pt1, pt2))[-1]

# pt1 = Coord(0,0)
# pt2 = Coord(20,5)
# print pt1,pt2,list(xline(pt1, pt2))[-1]


def line (start, stop):
    dxdy = lambda start,stop : (stop.x - start.x, stop.y - start.y)
    close_too_nothing = lambda val : abs(val) < 0.5

    dx,dy = dxdy(start, stop)
    xincr = -1 if dx < 0 else 1
    yincr = -1 if dy < 0 else 1

    vertical = close_too_nothing(dx)
    horizontal = close_too_nothing(dy)

    if vertical:
        return [(start.x, y) for y in range(*([start.y, stop.y,yincr]))]
    elif horizontal:
        return [(x, start.y) for x in range(*([start.x, stop.x,xincr]))]

    if abs(dx) < abs(dy):
        return list(yline(start,stop))
    else:
        return list(xline(start,stop))

# copying the char drawing code here..
XDIM,YDIM = 50,40
buffer = ['.' for i in range(XDIM*YDIM)]
def putchar(x,y,char):
    global XDIM
    for i,c in enumerate(char):
        buffer[x+i+y*YDIM] = c

pt1,pt2 = Coord(10,10), Coord(20,20)
def charline(pt1, pt2):
    aline = list(line(pt1,pt2))
    for i in aline:
        x,y = i 
        putchar(x,y,'*')
    putchar(pt1.x,pt1.y,'%s,%s>'%(pt1.x,pt1.y))
    putchar(pt2.x,pt2.y,'%s,%s<'%(pt2.y,pt2.y))


# crds = [Coord(10,10),
#         Coord(10,20),
#         Coord(20,20),
#         Coord(20,10)]

def regupoly(points):
    number_of_pnts = len(points)
    for i in range(0,number_of_pnts):
        charline(points[i], points[(i+1)%number_of_pnts])

# regupoly(crds)
#--------- random shape drawer
from math import pi, sin, cos
corners = 6
center = Coord(20,20)
radius = 10
angle = lambda num : num*2*pi/(1.0*corners)
output = []
for corner in range(corners,0,-1):
    a = angle(corner)
    x,y = int(round(center.x+radius*cos(a))), int(round(center.y+radius*sin(a)))
    putchar(x,y,'@')
    output += [Coord(x,y)]
print output

regupoly(output)
#--------- print the "backbuffer" of chars

for y in range(0,YDIM):
    for x in range(0,XDIM):
        print buffer[x+y*YDIM],
    print
import pdb; pdb.set_trace()
pt2 = Coord(15,29)
pt1 = Coord(10,20)
print pt1,pt2,line(pt1,pt2)[-1]
print pt1,pt2,list(xline(pt1,pt2))[-1]
print pt1,pt2,list(yline(pt1,pt2))[-1]
