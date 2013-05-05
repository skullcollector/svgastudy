from lineutil import *

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
add_after_last_point(poly4,-5,-8)

circdec = lambda i,length: (length+(i-1))%length
circinc = lambda i,length: (i+1)%length
def vertirate(vertices,backward=False):
    '''
    should use itertools.cycle, but want to get into C mode just now..
    v = vertirate("Test string 123",True)  # True means reverse iterate
    for i in range(0,100):
        print v.next()

    '''
    global circdec, circinc

    length = len(vertices)
    i = 0 if not backward else length-1
    while True:
        
        yield vertices[i]
        if backward:
            i = circdec(i,length)
        else:
            i = circinc(i,length)
        

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


def fill_convex_poly(vertices,ch=None):
    global circinc,circdec
    length = len(vertices)
    if length == 0:
        return None
    miny_maxy_idxes = find_y_bounds(vertices)
    if not miny_maxy_idxes:
        return None
    miny_left_idx,maxy_idx = miny_maxy_idxes

    miny_point = vertices[miny_left_idx]

    # find right most point of top edge
    miny_right_idx = miny_left_idx
    while vertices[miny_right_idx].y == miny_point.y:
        miny_right_idx =circinc(miny_right_idx,length)
    miny_right_idx = circdec(miny_right_idx,length)

    # find left most point of top edge
    while vertices[miny_left_idx].y == miny_point.y:
        miny_left_idx =circdec(miny_left_idx,length)
    miny_left_idx = circinc(miny_left_idx,length)
    
    flat = False
    if vertices[miny_left_idx].x != vertices[miny_right_idx].x:
        print "FLAT", vertices[miny_left_idx], vertices[miny_right_idx]
        flat = True
    else:
        print "not FLAT", vertices[miny_left_idx], vertices[miny_right_idx]
        flat = False
        
    if ch:
        # for a square the X and 0 will be
        # on opposite sides 
        # compare poly1 (square like) vs poly4 (diamond like)
        rv = vertices[miny_right_idx]
        lv = vertices[miny_left_idx]
        ch.putchar(rv.x,rv.y,'X')
        ch.putchar(lv.x,lv.y,'O')
        
    if flat:
        if vertices[miny_left_idx].x > vertices[miny_right_idx].y:
            # py swap!
            miny_left_idx, miny_right_idx = miny_right_idx, miny_left_idx

    if ch:
        # for a square the X and 0 will be
        # on opposite sides 
        # compare poly1 (square like) vs poly4 (diamond like)
        rv = vertices[miny_right_idx]
        lv = vertices[miny_left_idx]
        ch.putchar(rv.x,rv.y,'X')
        ch.putchar(lv.x,lv.y,'O')

    next_idx = circdec(miny_right_idx,length)    
    previous_idx = circinc(miny_left_idx,length)    

    if ch:
        # for a square the X and 0 will be
        # on opposite sides 
        # compare poly1 (square like) vs poly4 (diamond like)
        nrv = vertices[next_idx]
        plv = vertices[previous_idx]

        ch.putchar(nrv.x,nrv.y,'Xn')
        ch.putchar(plv.x,plv.y,'Op')

    # gradient from next to center vs
    # gradient from previous to center
    dxn,dyn = dxdy(vertices[next_idx], vertices[miny_left_idx])
    dxp,dyp = dxdy(vertices[previous_idx], vertices[miny_left_idx])

    # YN/XN > YP/XP  ==>  YN/XN-YP/XP > 0 ==> XNXP * (YN/XN-YP/XP)  > 0 
    #                ==>  (XP*YN- XN*YP)  > 0
    # not sure how you can assume XNXP > 0 ?
    #
    if (dxp*dyn - dxn*dyp) > 0:
        miny_left_idx,miny_right_idx = miny_right_idx, miny_left_idx
    
ch1 = CharPlotter(oct_x_dom=oct_x_dom_implementation, oct_y_dom=oct_y_dom_implementation)
ch1.regupoly(poly1,marks='.')
ch1.regupoly(poly4,marks='.')
fill_convex_poly(poly1,ch=ch1)
fill_convex_poly(poly4,ch=ch1)
ch1.render()
