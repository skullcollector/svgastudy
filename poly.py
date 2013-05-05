from lineutil import *

def oct_x_dom_imp(ptA,ptB):
    '''
    Redefinition:
    current_error = DY*current_error (from float implementation)
    '''

    dx, dy = dxdy(ptA,ptB)

    startx,starty = ptA.x,ptA.y
    stopx,stopy = ptB.x,ptB.y

    if dx < 0:
        startx,starty = ptB.x,ptB.y
        stopx,stopy = ptA.x,ptA.y
        dx, dy = dxdy(ptB,ptA)

    yincr = 1
    if dy < 0:
        dy = -dy
        yincr = -1

    #M = 1.0*dy/dx       
    DX,DY = dx, dy

    # new_error = { 'skipping y': lambda current_error : current_error + M,
    #               'adding to y': lambda current_error : current_error + M - 1}

    new_error = { 'skipping y': lambda current_error : current_error + DY,
                  'adding to y': lambda current_error : current_error + DY - DX}

    x = startx
    y = starty
    current_error = 0
    while dx > 0:
        dx -= 1      
        x += 1
        a_error =new_error['skipping y'](current_error)
        if 2*a_error < DX:
            current_error = a_error #new_error['skipping y'](current_error)
        else:
            y = y + yincr
            current_error = new_error['adding to y'](current_error)

        yield x,y


def oct_y_dom_imp(ptA,ptB):
    '''
    Redefinition:
    current_error = DX*current_error (from float implementation)
    '''
    dx, dy = dxdy(ptA,ptB)

    startx,starty = ptA.x,ptA.y
    stopx,stopy = ptB.x,ptB.y

    if dy < 0:
        startx,starty = ptB.x,ptB.y
        stopx,stopy = ptA.x,ptA.y
        dx, dy = dxdy(ptB,ptA)
       
    xincr = 1
    if dx < 0:
        dx = -dx
        xincr = -1

    #M = 1.0*dx/dy
    DX, DY = dx, dy

    new_error = { 'skipping x': lambda current_error : current_error + DX,
                  'adding to x': lambda current_error : current_error + DX -DY}
        
    x = startx
    y = starty
    current_error = 0
    while dy > 0:
        dy -= 1      
        y += 1
        a_error =new_error['skipping x'](current_error)
        if 2*a_error < DX:   # was a_error < 0.5 but multiplied with 2 
            current_error = a_error #new_error['skipping x'](current_error)
        else:
            x = x + xincr
            current_error = new_error['adding to x'](current_error)

        yield x,y

# assuming poly vertices are in order..
# square
poly1 = [Coord(0,0)]
poly1 = poly1+ [poly1[0].add(y=10),
                poly1[0].add(x=10,y=10),
                poly1[0].add(x=10), ]


# diamond
poly3 = [Coord(0,20)]
poly3 = poly3+[poly3[0].add(x=10,y=-10),
               poly3[0].add(x=20,y=0),
               poly3[0].add(x=10,y=10),]


# a polygon with convex vertices
add_after_last_point = lambda lst,x,y: lst.append(lst[-1].add(x,y))
poly4 = [Coord(20,0)]
add_after_last_point(poly4,-4,2)
add_after_last_point(poly4,-6,10)
add_after_last_point(poly4,10,10)
add_after_last_point(poly4,10,-10)

def vertirate(vertices,backward=False):
    '''
    should use itertools.cycle, but want to get into C mode just now..
    v = vertirate("Test string 123",True)  # True means reverse iterate
    for i in range(0,100):
        print v.next()

    '''
    length = len(vertices)
    i = 0 if not backward else length-1
    while True:
        
        yield vertices[i]
        if backward:
            i = (length+(i-1))%length    
        else:
            i = (i+1)%length
        

def find_y_bounds(vertices):
    length = len(vertices)
    if length ==0:
        return None

    at_min_y = at_max_y = vertices[0]  # at at_min_y or at at_max_y
    min_idx = max_idx = 0
    i = 0
    vgen = vertirate(vertices)
    for i in range(0,length):
        v = vgen.next()
        if  v.y < at_min_y.y:
            at_min_y = v
            min_idx = i
        elif v.y > at_max_y.y:
            at_max_y = v
            max_idx = i
        i +=1
    return min_idx, max_idx

print find_y_bounds(poly3)
print poly3

print find_y_bounds(poly4)
print poly4


def fill_convex_poly(vertices):
    miny_maxy = find_y_bounds(vertices)
    if not miny_maxy:
        return None
    miny,maxy = miny_maxy

ch1 = CharPlotter(oct_x_dom=oct_x_dom_imp, oct_y_dom=oct_y_dom_imp)
ch1.regupoly(poly4,marks='.')
ch1.render()
