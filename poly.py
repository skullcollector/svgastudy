from lineutil import *
from math import ceil
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
add_after_last_point(poly4,-6,-9)

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

class HlineList(object):
    def __init__(self,ystart=0):
        self.__hlines = []
        self.ystart = ystart

    def add(xstart, ystart):
        self.__hlines.append((xstart,ystart))


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
        
    left_edge_dir = -1
    if flat:
        if vertices[miny_left_idx].x > vertices[miny_right_idx].y:
            # py swap!
            miny_left_idx, miny_right_idx = miny_right_idx, miny_left_idx
            left_edge_dir = 1

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
        # swap !
        miny_left_idx,miny_right_idx = miny_right_idx, miny_left_idx
        left_edge_dir = 1

    
    # Gather stats:
    # where does is the ystart?
    ystart = vertices[miny_left_idx].y
    # how many hlines do we wants? malloc
    num_hlines = vertices[maxy_idx].y - vertices[miny_left_idx].y -1  #---> need more refining.


    def scanedge(x1,y1,x2,y2,drawer=None,chr='#'):
        dx,dy = x2-x1, y2-y1
        if dy <= 0:
            return [ ]
        inv_slope = 1.0*dx/dy
        xvals = []
        for y in range(y1,y2):
            xvals.append(x1+int(ceil((y-y1)*inv_slope)))
            if drawer:
                drawer.putchar(xvals[-1],y,chr)
        return xvals


    skipfirst = 0 if flat else 1
    
    left_edge_dir = -1
    prev_idx = current_idx = miny_left_idx
    start_hlines = []        
    # for this Ystart, get all edge horizontal lines...
    increment = circinc if left_edge_dir < 0 else circdec
    while current_idx != maxy_idx:
        current_idx = increment(current_idx,length)
        start_hlines.extend(scanedge(vertices[prev_idx].x,
                                     vertices[prev_idx].y,
                                     vertices[current_idx].x,
                                     vertices[current_idx].y,drawer=None))

        prev_idx = current_idx


    stop_hlines = []
    prev_idx = current_idx = miny_right_idx
    increment = circinc if left_edge_dir > 0 else circdec
    while current_idx != maxy_idx:
        current_idx = increment(current_idx,length)
        stop_hlines.extend(scanedge(vertices[prev_idx].x -1,
                                     vertices[prev_idx].y,
                                     vertices[current_idx].x -1,
                                     vertices[current_idx].y,drawer=None,chr='@'))
        prev_idx = current_idx

    
    for i,x in enumerate(start_hlines): 
        x2 = stop_hlines[i]
        ch.putchar(x,ystart+i,'%'*(x2-x))

    # total_hlines = vertices[maxy_idx].y - vertices[miny_left_idx].y - 1
    # if flat:
    #     total_hlines -= 1

    # ystart = vertices[miny_left_idx].y +1
    # if flat:
    #     ystart -= 1
        
    # hlinelist = []

    # increment = circinc if 1 else decinc
    # v = scanedge(vertices[prev_idx].x, vertices[prev_idx].y, vertices[current_idx].x, vertices[current_idx].y, total_hlines)
    # while current_idx != maxy_idx:
    #     current_idx = increment(current_idx, length)
    #     # do something
    #     try:
    #         hlinelist.append(v.next())
    #     except StopIteration,ex:
    #         break;
    #     ch.putchar(vertices[prev_idx].x, vertices[prev_idx].y,'=')
    #     ch.putchar(vertices[current_idx].x, vertices[current_idx].y,'+')
    #     ch.putchar(hlinelist[-1],ystart,'&')

    #     prev_idx= current_idx



ch1 = CharPlotter(oct_x_dom=oct_x_dom_implementation, oct_y_dom=oct_y_dom_implementation)
ch1.regupoly(poly1,marks='.')
ch1.regupoly(poly4,marks='.')
fill_convex_poly(poly1,ch=ch1)
fill_convex_poly(poly4,ch=ch1)
ch1.render()
