from math import pi, sin, cos, sqrt, atan


def forinstance(inputfunction, *args,**kwargs):
    '''
    decorator to make sure we're (sub/add/..)ing typeX to typeX
    '''
    def fn(self, other):
        if isinstance(other,self.__class__):
            return inputfunction(self, other, *args, **kwargs)
        else:
            raise Exception("I cant do this with types %s and %s"%(self.__class__,type(other)))
    return fn

class Coord(object):
    '''
    Immutable
    '''
    x = 0;
    y = 0;
    def __init__(self, x,y):
        self.x, self.y = x,y

    def __str__(self):
        return "<%d,%d>"%(self.x, self.y)

    def __repr__(self):
        return "<%d,%d>"%(self.x, self.y)

    def add(self, x = 0, y = 0):
        return Coord(self.x+x, self.y+y)

    @forinstance
    def __add__(self, other):
        return self.add(x=other.x, y=other.y)

    def sub(self, x= 0, y = 0):
        return Coord(self.x-x, self.y-y)

    @forinstance
    def __sub__(self, other):
        return self.sub(x=other.x, y=other.y)
        
dxdy = lambda start,stop : (stop.x - start.x, stop.y - start.y)
close_enough = lambda actualpnt, calcpnt: sqrt((actualpnt.x-calcpnt.x)**2 + (actualpnt.y-calcpnt.y)**2) < 2
practically_nothing = lambda val : abs(val) < 0.1

#------- Test helpers----

def gen_pts_with_gradient(gradient,start_coord=Coord(0,0),radius=10):
    # (Ystop-Ystart)/(Xstop-Xstart) = (y-Ystart)/(x-Xstart)
    # y = 1.0*(Ystop-Ystart)/(Xstop-Xstart)*(x-Xstart) + Ystart
    #size = gradient
    angle = atan(gradient)
    print 180*angle/pi, gradient,'...'
    x,y = start_coord.x+int(round(radius*cos(angle))),start_coord.y+int(round(radius*sin(angle)))
    end_coord = Coord(x,y)
    return [start_coord, end_coord]


def print_gradient_example(gradient, radius=100, start_coord=Coord(0,0)):
    start,stop = gen_pts_with_gradient(gradient=gradient,radius=radius, start_coord=start_coord)
    dx,dy = dxdy(start,stop)
    M = 1.0*dy/dx
    print start,stop,M  


def testcases(gradient_list=[2,1.75,1.5,1.25,1,0.75,0.5,0.25,0.15], start_coord=Coord(0,0),radius=10):
    for grad in gradient_list:       
        yield gen_pts_with_gradient(grad, start_coord=start_coord,radius=radius)
              
#------------------------
# def curry(fn, **kwargs):
#     def wrapped(*args,**kw):
#         return fn(kwargs)

def line_skeleton(ptA,ptB,oct_x_dom=None,oct_y_dom=None):
    '''
    assumptions:
    x is only increasing.
    '''
    dx,dy = dxdy(ptA,ptB)

    startx, starty = ptA.x,ptA.y
    stopx, stopy = ptB.x,ptB.y

    if practically_nothing(dx):
        y = starty
        while dy > 0:
            dy -= 1
            yield (startx, y)
            y += 1
            
        while dy < 0:
            dy += 1
            yield (startx, y)
            y -= 1
        
            
    if practically_nothing(dy):
        x = startx
        while dx > 0:
            dx -= 1
            yield (x, starty)
            x += 1
            
        while dx < 0:
            dx += 1
            yield (x, starty)
            x -= 1

    if not practically_nothing(dy) and not practically_nothing(dx):

        #import pdb; pdb.set_trace()
        dx,dy = dxdy(ptA,ptB)
        
        startx, starty = ptA.x,ptA.y
        stopx, stopy = ptB.x,ptB.y

        points = []
        if abs(dx) >= abs(dy):
            if not oct_x_dom:
                raise Exception("X dominant Line octants not implemented")

            for pt in oct_x_dom(ptA,ptB):
                yield pt
        else:
            if not oct_y_dom:
                raise Exception("Y dominant Line octants not implemented")
                
            for pt in oct_y_dom(ptA,ptB):
                yield pt

            
class CharPlotter(object):
    def __init__(self, XDIM=50, YDIM=40, linefunc=line_skeleton, buffer=None, filler_char=' ', oct_x_dom=None, oct_y_dom=None):
        self.XDIM = XDIM
        self.YDIM = YDIM
        self.line = linefunc
        self.oct_x_dom = oct_x_dom
        self.oct_y_dom = oct_y_dom
        self.buffer = [filler_char for i in range(self.XDIM*self.YDIM)] if not buffer else buffer

    def call_line(self,start,stop):
        for i in self.line(start,stop,oct_x_dom=self.oct_x_dom, oct_y_dom=self.oct_y_dom):
            yield i

    def render(self):
        for y in range(0,self.YDIM):
            for x in range(0,self.XDIM):
                print self.buffer[x+y*self.YDIM],
            print

    def putchar(self,x,y,char):
        for i,c in enumerate(char):
            self.buffer[x+i+y*self.YDIM] = c

    def charline(self,pt1, pt2, marks=None):        
        #aline = list(self.line(pt1,pt2,oct_x_dom= self.oct_x_dom,oct_y_dom = self.oct_y_dom))
        aline = list(self.call_line(pt1,pt2))
        for i in aline:
            x,y = i 
            self.putchar(x,y,'*')
        if marks is None:
            self.putchar(pt1.x,pt1.y,'%s,%s>'%(pt1.x,pt1.y))
            self.putchar(pt2.x,pt2.y,'%s,%s<'%(pt2.y,pt2.y))
        else:
            self.putchar(pt1.x,pt1.y,'A')
            self.putchar(pt2.x,pt2.y,'B')
            
    def regupoly(self,points,marks=None):
        number_of_pnts = len(points)
        for i in range(0,number_of_pnts):
            self.charline(points[i], points[(i+1)%number_of_pnts],marks=marks)

    def create_npoly(self, **kwargs):
        x = kwargs.get('x',20)
        y = kwargs.get('y',20)
        theta = kwargs.get('theta',0)
        corners = kwargs.get('num_of_corners',4)        
        radius =  kwargs.get('radius', 10)
        angle = lambda num : num*2*pi/(1.0*corners)
        output = []
        for corner in range(corners,0,-1):
            a = angle(corner)+theta
            xn,yn = int(round(x+radius*cos(a))), int(round(y+radius*sin(a)))
            self.putchar(xn,yn,'@')
            output += [Coord(xn,yn)]
        return output


def oct_x_dom_implementation(ptA,ptB):
    '''
    No float x dominant line drawing.. part of line drawing algo.

    Use in above CharPlotter contstructor to draw non horiztonal/vertical lines as well

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


def oct_y_dom_implementation(ptA,ptB):
    '''
    No float y dominant line drawing.. part of line drawing algo.

    Use in above CharPlotter contstructor to draw non horiztonal/vertical lines as well

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

# Convex Polygon code
class HLineList(object):
    def __init__(self,ystart=0, length=0, drawer=None, use_floats=False, malloc_size=100):
        self.__hlines_start = [] # extra storage, debugging
        self.__hlines_stop = []  # extra storage, debugging
        self.__hlines_tuples = None
        self.ystart = ystart
        self.length = length
        self.startcount = 0
        self.stopcount = 0
        if length <=0:
            self.__hlines_tuples = [[0,0]]
        else:
            self.__hlines_tuples = [[0,0] for i in range(malloc_size)] # fake "malloc"

        self.drawer = drawer
        self.edgecalc = self.__add_edge_float if use_floats else self.__add_edge_int

    def gettuples(self):
        return self.__hlines_tuples[:]

    def addstart(self,xstart):
        # adding as single items
        self.__hlines_start.append(xstart)
        # adding as part of a tuple.
        self.__hlines_tuples[self.startcount][0] = xstart        
        self.startcount+=1
        # Both approaches not required, but still need to figure out if the left points will always match right.

    def addstop(self,xstop):
        # adding as single items
        self.__hlines_stop.append(xstop)
        # adding as part of a tuple.
        self.__hlines_tuples[self.stopcount][1] = xstop
        self.stopcount+=1
        # Both approaches not required, but still need to figure out if the left points will always match right.

    def __add_edge_int(self,
                       x1,y1,
                       x2,y2,
                       skipfirst = 0,
                       leftedge=False,
                       char=None):        
        # Chapter 39 GPBB
        edge_to_add_to = self.addstart if leftedge else self.addstop
        
        height = dy = y2-y1 # always > 0, going down from miny to maxy
        width = dx = x2-x1
        if dy <= 0:
            return

        width = width if width > 0 else -width
        xincr = 1 if dx > 0 else -1
        if width == 0:
            ''' vertical '''

            #for i in range(height-skipfirst,-1,-1):
            i = height - skipfirst
            while i > 0:
                i -= 1
                edge_to_add_to(x1)

        elif width == height:
            ''' diagonal '''

            x1 = x1+xincr if skipfirst else x1

            #for i in range(height-skipfirst,-1,-1):
            i = height - skipfirst
            while i > 0:
                i -= 1
                edge_to_add_to(x1)
                x1 += xincr

        elif height > width:
            ''' y dominant '''

            error = 0
            if dy < 0:
                error = -height +1  # right -> left
            if skipfirst != 0:
                error += width
                if error > 0:
                    x1 += xincr
                    error -= height

            #for i in range(height-skipfirst,-1,-1):
            i = height - skipfirst
            while i > 0:
                i -= 1

                edge_to_add_to(x1)

                error += width
                if error > 0:
                    x1 += xincr
                    error -= height

        else:
            ''' edge is X dominant '''            
            #x_dom_incr = int(floor(1.0*width/height)*xincr)  # what? Floats????
            x_dom_incr = (width/height)*xincr  # what? Floats????
            error_incr = width % height # more float ops???
            error = 0
            if dx < 0:
                error = -height +1
            if skipfirst != 0:
                x1 += x_dom_incr
                error += error_incr
                if error > 0:
                    x1 += xincr
                    error -= height

            #for i in range(height-skipfirst,-1,-1):
            i = height - skipfirst
            while i > 0:
                i -= 1

                edge_to_add_to(x1)

                x1 += x_dom_incr
                error += error_incr
                if error > 0:
                    x1 += xincr
                    error -= height
           

    def __add_edge_float(self,                   
                         x1,y1,
                         x2,y2,
                         skipfirst = 0,
                         leftedge=False,
                         char=None):    
        # GPBB Chapter 38    
        # Not used, but left to show the basic idea
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
                      skipfirst = 0):
        self.edgecalc(x1,y1,
                      x2,y2,
                      skipfirst = skipfirst,
                      leftedge=True,
                      char='$')


    def scanedge_right(self,
                      x1,y1,
                      x2,y2,
                      skipfirst = 0):
        self.edgecalc(x1,y1,
                      x2,y2,
                      skipfirst = skipfirst,
                      leftedge=False,
                      char='&')


    def draw_hlines(self,use_tuples=True):
        if not self.drawer:
            raise Exception("Nothing to draw hlines with")
            
        length_start = len(self.__hlines_start)
        length_stop = len(self.__hlines_stop)
        if length_start != length_stop :
            raise Exception("Something wrong with your algorithm, stop points(%d) != start points(%d)"%(length_stop,length_start))

        #for i,startpnt in enumerate(self.__hlines_start):            
        if use_tuples:
            for i in range(0,min([length_start,length_stop])):
                t = self.gettuples()
                xstart,xstop = t[i]
                y = self.ystart+i
                self.drawer.putchar(xstart,y,'~'*(xstop-xstart))
                
        else:
            for i in range(0,min([length_start,length_stop])):
                startpnt = self.__hlines_start[i]
                y = self.ystart + i
                x = startpnt
                x_stop = self.__hlines_stop[i]            
                self.drawer.putchar(x,y,'='*(x_stop - x))  # in C, I'd rather memset this.



def fill_convex_poly(vertices,drawer=None, debug=False):
    # GPBB Chapter 38
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
        if debug: 
            print "FLAT", vertices[miny_left_idx], vertices[miny_right_idx]
        flat = True
    else:
        if debug:
            print "not FLAT", vertices[miny_left_idx], vertices[miny_right_idx]
        flat = False

    if drawer and debug:
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

    next_idx = circdec(miny_right_idx,length)    
    previous_idx = circinc(miny_left_idx,length)    

    if drawer and debug:
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
    #
    if (dxp*dyn - dxn*dyp) > 0:
        # swap.. again !
        miny_left_idx,miny_right_idx = miny_right_idx, miny_left_idx
        left_edge_dir = 1      


    dec_if_flat = 1 if flat else 0
    y_start = miny_point.y + 1 - dec_if_flat
    y_length = vertices[maxy_idx].y - vertices[miny_left_idx].y - 1 + dec_if_flat
    hlinelist = HLineList(y_start,y_length,drawer=drawer,use_floats=False)

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
                                skipfirst=skipfirst)
        skipfirst = 0
        prev_idx = current_idx


    prev_idx = current_idx = miny_right_idx
    skipfirst = 0 if flat else 1    
    while current_idx != maxy_idx:
        current_idx = circdec(current_idx,length)
        X1 = vertices[prev_idx].x-1
        Y1 = vertices[prev_idx].y
        X2 = vertices[current_idx].x-1
        Y2 = vertices[current_idx].y
        hlinelist.scanedge_right(X1,Y1,
                                 X2,Y2,
                                 skipfirst=skipfirst)
        skipfirst = 0
        prev_idx = current_idx

    if drawer and debug:
        tuples = hlinelist.gettuples()
        for i in range(hlinelist.startcount):
            x = tuples[i][0]
            drawer.putchar(x,hlinelist.ystart+i,'S')

        for i in range(hlinelist.stopcount):
            x = tuples[i][1]
            drawer.putchar(x,hlinelist.ystart+i,'P')

    hlinelist.draw_hlines()

