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
add_after_last_point(poly4,-1,5)
add_after_last_point(poly4,5,8)
add_after_last_point(poly4,3,3)
add_after_last_point(poly4,4,-4)
add_after_last_point(poly4,6,-9)

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

class HLineList(object):
    def __init__(self,ystart=0, length=0, drawer=None):
        self.__hlines_start = []
        self.__hlines_stop = []
        self.ystart = ystart
        self.length = length
        self.drawer = drawer

    def addstart(self,xstart):
        self.__hlines_start.append(xstart)

    def addstop(self,xstop):
        self.__hlines_stop.append(xstop)

    def __add_edge(self,                   
                   x1,y1,
                   x2,y2,
                   skipfirst = 0,
                   leftedge=False,
                   char=None):        
        dy = y2-y1
        dx = x2-x1
        if dy <= 0:
            return
        invM = (1.0*dx)/dy
        
        for y in range(y1+skipfirst, y2):
            x = int(ceil(invM*(y-y1)+x1))
            if leftedge:
                self.addstart(x)
            else:
                self.addstop(x)
        
            if self.drawer:
                self.drawer.putchar(x,y,char)

    def scanedge_left(self,
                      x1,y1,
                      x2,y2,
                      skipfirst = 0,
                      char=None):
        self.__add_edge(x1,y1,
                        x2,y2,
                        skipfirst = skipfirst,
                        leftedge=True,
                        char=char)


    def scanedge_right(self,
                      x1,y1,
                      x2,y2,
                      skipfirst = 0,
                      char=None):
        self.__add_edge(x1,y1,
                        x2,y2,
                        skipfirst = skipfirst,
                        leftedge=False,
                        char=char)


    def draw_hlines(self):
        if not self.drawer:
            raise Exception("Nothing to draw hlines with")
            
        length_start = len(self.__hlines_start)
        length_stop = len(self.__hlines_stop)
        if length_start != length_stop :
            raise Exception("Something wrong with your algorithm, stop points(%d) != start points(%d)"%(length_stop,length_start))

        for i,startpnt in enumerate(self.__hlines_start):            
            y = self.ystart + i
            x = startpnt
            x_stop = self.__hlines_stop[i]            
            self.drawer.putchar(x,y,'='*(x_stop - x))  # in C, I'd rather memset this.

def fill_convex_poly(vertices,drawer=None):
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
        
    if drawer:
        # for a square the X and 0 will be
        # on opposite sides 
        # compare poly1 (square like) vs poly4 (diamond like)
        rv = vertices[miny_right_idx]
        lv = vertices[miny_left_idx]
        drawer.putchar(rv.x,rv.y,'X')
        drawer.putchar(lv.x,lv.y,'O')
        
    left_edge_dir = -1  # left edge indexing direction
    if flat:
        if vertices[miny_left_idx].x > vertices[miny_right_idx].y:
            # py swap!
            miny_left_idx, miny_right_idx = miny_right_idx, miny_left_idx
            left_edge_dir = 1

    if drawer:
        # for a square the X and 0 will be
        # on opposite sides 
        # compare poly1 (square like) vs poly4 (diamond like)
        rv = vertices[miny_right_idx]
        lv = vertices[miny_left_idx]
        drawer.putchar(rv.x,rv.y,'X')
        drawer.putchar(lv.x,lv.y,'O')

    next_idx = circdec(miny_right_idx,length)    
    previous_idx = circinc(miny_left_idx,length)    

    if drawer:
        # for a square the X and 0 will be
        # on opposite sides 
        # compare poly1 (square like) vs poly4 (diamond like)
        nrv = vertices[next_idx]
        plv = vertices[previous_idx]

        drawer.putchar(nrv.x,nrv.y,'Xn')
        drawer.putchar(plv.x,plv.y,'Op')

    # gradient from next to center vs
    # gradient from previous to center
    dxn,dyn = dxdy(vertices[next_idx], vertices[miny_left_idx])
    dxp,dyp = dxdy(vertices[previous_idx], vertices[miny_left_idx])

    '''
    Assumptions:
    Previous point (Xp) before min (Xmin) point on X axis.
    Next point  (Xn) after min (Xmin) point on X axis.

    In other "words":

    Xp < Xmin => Xmin - Xp < 0 => DXP < 0
    Xn > Xmin => Xn - Xmin > 0 => -DXN > 0
    
    So, 
    -DXP > 0
    -DXN > 0
    => -DXP * -DXN  > 0
    => DXP * DXN > 0

    And that's why you can assume XNXP > 0 

    If the signs are wrong way around, it will still be -1* somthing * -1 * somethingelse

    Booyah.
    '''
    # YN/XN > YP/XP  ==>  YN/XN-YP/XP > 0 ==> XNXP * (YN/XN-YP/XP)  > 0 
    #                ==>  (XP*YN- XN*YP)  > 0
    # not sure how you can assume XNXP > 0 ?
    #
    if (dxp*dyn - dxn*dyp) > 0:
        # swap.. again !
        miny_left_idx,miny_right_idx = miny_right_idx, miny_left_idx
        left_edge_dir = 1      


    dec_if_flat = 1 if flat else 0
    y_start = miny_point.y + 1 - dec_if_flat
    y_length = vertices[maxy_idx].y - vertices[miny_left_idx].y - 1 + dec_if_flat
    hlinelist = HLineList(y_start,y_length,drawer=drawer)

    prev_idx = current_idx = miny_left_idx
    skipfirst = 0 if flat else 1    
    while current_idx != maxy_idx:
        current_idx = circinc(current_idx,length)
        X1 = vertices[prev_idx].x
        Y1 = vertices[prev_idx].y
        X2 = vertices[current_idx].x
        Y2 = vertices[current_idx].y
        hlinelist.scanedge_left(X1,Y1,
                                X2,Y2,
                                skipfirst=skipfirst,
                                char='$')
        skipfirst = 0
        prev_idx = current_idx


    prev_idx = current_idx = miny_left_idx
    skipfirst = 0 if flat else 1    
    while current_idx != maxy_idx:
        current_idx = circdec(current_idx,length)
        X1 = vertices[prev_idx].x
        Y1 = vertices[prev_idx].y
        X2 = vertices[current_idx].x
        Y2 = vertices[current_idx].y
        hlinelist.scanedge_right(X1,Y1,
                                 X2,Y2,
                                 skipfirst=skipfirst,
                                 char='&')
        skipfirst = 0
        prev_idx = current_idx


    hlinelist.draw_hlines()

drawer1 = CharPlotter(oct_x_dom=oct_x_dom_implementation, oct_y_dom=oct_y_dom_implementation)
drawer1.regupoly(poly1,marks='.')
drawer1.regupoly(poly4,marks='.')
fill_convex_poly(poly1,drawer=drawer1)
fill_convex_poly(poly4,drawer=drawer1)
drawer1.render()


