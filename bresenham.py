
# He split it into octants...
#
class Coord:
    x = 0;
    y = 0;
    def __init__(self, x,y):
        self.x, self.y = x,y

    def __str__(self):
        return "<%d,%d>"%(self.x, self.y)

def categorise(start, end):
    
    deltaX = end.x - start.x
    deltaY = end.y - start.y
    close_too_nothing = lambda val : abs(val) < 0.5

    if close_too_nothing(deltaX):
        return "vertical"
    if close_too_nothing(deltaY):
        return "horizontal"
    
    # if the line is as much in the X axis as in the Y axis..
    if abs(deltaX) < abs(deltaY):
        return "Y Dominates"
    else:
        return "X Dominates"
        

def line0(start, end):
    deltax = end.x-start.x
    deltay = end.y-start.y

    m = 1.0*deltay/deltax

    x = start.x
    y = start.y

    for x in range(start.x, end.x):
        yield x, y
        yreal = m*(x-start.x)+start.y
        if abs(y-yreal) >= 0.5:
            y += 1
            
pt1 = Coord(10,0)
pt2 = Coord(300,100)
print pt1,pt2,'vs', list(line0(pt1, pt2))[-1]
print categorise(pt1,pt2)
            

# too steep
pt1 = Coord(10,20)
pt2 = Coord(200,300)
print pt1,pt2,'vs', list(line0(pt1, pt2))[-1]
print categorise(pt1,pt2)

# last coord incorrect.
def line1(start, end):
    deltax = end.x-start.x
    deltay = end.y-start.y

    m = 1.0*deltay/deltax
    
    x = start.x
    y = start.y

    for y in range(start.y, end.y):
        yield x, y
        xreal = (y-start.y)/m+start.x
        if abs(x-xreal) >= 0.5:
            x += 1
# too steep
pt1 = Coord(10,20)
pt2 = Coord(200,300)
print pt1,pt2,'vs', list(line1(pt1, pt2))[-1]
print categorise(pt1,pt2)


# Now, how about the other directions...
def line2(start, end):
    deltax = end.x-start.x
    deltay = end.y-start.y

    m = 1.0*deltay/deltax

    x = start.x
    y = start.y
    

    for y in range(start.y, end.y, -1):
        yield x, y

        xreal = (y-start.y)/m+start.x
        if abs(x-xreal) >= 0.5:
            x += 1

print 200*'--'
pt1 = Coord(200,300)
pt2 = Coord(300,10)  # y decline is very steep!!
print pt1,pt2,'vs', list(line2(pt1, pt2))[-1]
print categorise(pt1,pt2)

print 200*'--'
pt1 = Coord(200,300)
pt2 = Coord(300,200)  # y decline is not steep!!
print pt1,pt2,'vs', list(line2(pt1, pt2))[-1]
print categorise(pt1,pt2)


# combine line  1 and line 2:
def line_ydom(start, end):
    incrementy = 1 if start.y < end.y else -1        
    incrementx = 1 if start.x < end.x else -1        
    deltax = end.x-start.x
    deltay = end.y-start.y

    m = 1.0*deltay/deltax

    x = start.x
    y = start.y
    
    for y in range(start.y, end.y, incrementy):
        yield x, y

        xreal = (y-start.y)/m+start.x
        if abs(x-xreal) >= 0.5:
            x = x + incrementx

# and then deduce from line 0 and above:
def line_xdom(start, end ):
    incrementy = 1 if start.y < end.y else -1
    incrementx = 1 if start.x < end.x else -1 

    deltax = end.x-start.x
    deltay = end.y-start.y

    m = 1.0*deltay/deltax

    x = start.x
    y = start.y

    for x in range(start.x, end.x, incrementx):
        yield x, y
        yreal = m*(x-start.x)+start.y
        if abs(y-yreal) >= 0.5:
            y = y + incrementy


def line(start,end):
    #import pdb; pdb.set_trace()
    pt_range = []
    increment = lambda begin,end: 1 if end > begin else -1;
            
    category = categorise(start,end)
    if category == "X Dominates":
        pt_range = line_xdom(start, end)
    elif category == "Y Dominates":
        pt_range = line_ydom(start, end)
    elif category == "horizontal":
        pt_range = [(x, start.y) for x in range(*([start.x, end.x, increment(start.x,end.x)]))]
    else : # category == "vertical":
        pt_range = [(start.x, y) for y in range(*([start.y, end.y, increment(start.x,end.x)]))]
    return pt_range
        
print 200*'='
pt1 = Coord(200,300)
pt2 = Coord(300,10)  # y decline is very steep!!
print pt1,pt2,'vs', list(line(pt1, pt2))[-1]
print categorise(pt1,pt2)

print 200*'=='
pt1 = Coord(200,300)
pt2 = Coord(300,200)  # y decline is not steep!!
print pt1,pt2,'vs', list(line(pt1, pt2))[-1]
print categorise(pt1,pt2)

# Now let's try our older examples:


# too steep
pt1 = Coord(10,20)
pt2 = Coord(200,300)
print pt1,pt2,'vs', list(line(pt1, pt2))[-1]
print categorise(pt1,pt2)

print pt2,pt1,'vs', list(line(pt2, pt1))[-1]
print categorise(pt1,pt2)


pt1 = Coord(10,0)
pt2 = Coord(300,100)
print pt1,pt2,'vs', list(line(pt1, pt2))[-1]
print categorise(pt1,pt2)

print pt2,pt1,'vs', list(line(pt2, pt1))[-1]
print categorise(pt1,pt2)


print "horiz test"
pt1 = Coord(10,0)
pt2 = Coord(300,0)

print pt1,pt2,'vs'
print list(line(pt1, pt2))[-1]
            
print "Vert test"
pt1 = Coord(0,220)
pt2 = Coord(0,10)
print pt1,pt2,'vs', list(line(pt1, pt2))[-1]


