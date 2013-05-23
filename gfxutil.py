from math import pi, sin, cos, sqrt, atan
from functools import partial


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
        
class Coord3(Coord):
    z= 0
    def __init__(self,x=0,y=0,z=0):        
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "<%d,%d,%d>"%(self.x, self.y,self.z)

    def __repr__(self):
        return "<%d,%d,%d>"%(self.x, self.y,self.z)

    def add(self, x = 0, y = 0,z=0):
        return Coord3(self.x+x, self.y+y, self.z+z)

    @forinstance
    def __add__(self, other):
        return self.add(x=other.x, y=other.y, z=other.z)

    def sub(self, x= 0, y = 0,z=0):
        return Coord3(self.x-x, self.y-y, self.z-z)

    @forinstance
    def __sub__(self, other):
        return self.sub(x=other.x, y=other.y, z= other.z)

# class MultiDimCoord(object):
#     '''
#     Due to my annoying habit of me switching between 2D 3D (4D?)
#     matrixes, coordinates and vectors, I want something that can 
#     expand dimension on the fly
    
#     MultiDim keywords maps to coordinate values:
#     MultiDim (x=2,y=3,z=0,w=12)
#     '''
#     def __init__(self,*args,**kwargs):
#         self.data = kwargs
#         for kw,value in kwargs.items():
#             setattr(self, kw, value)
            
#     def __str__(self):
#         return "<%s>"%','.join([k+":"+str(v) for k,v in self.data.items()])

#     def __repr__(self):
#         return "<%s>"%','.join([k+":"+str(v) for k,v in self.data.items()])

#     def add(self, *args,**kwargs):
#         self.data = kwargs
#         for kw,value in kwargs.items():
#             setattr(self, kw, value)


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

class Plotter(object):
    def __init__(self,default_colour, XDIM=50, YDIM=40, linefunc=line_skeleton, buffer=None, oct_x_dom=None, oct_y_dom=None):
        self.XDIM = XDIM
        self.YDIM = YDIM
        self.line = linefunc
        self.oct_x_dom = oct_x_dom
        self.oct_y_dom = oct_y_dom
        self.buffer = [] if not buffer else buffer
        if default_colour == None:
            raise Exception("Give me a default colour!")

    def call_line(self, start,stop):
        for i in self.line(start,stop,oct_x_dom=self.oct_x_dom, oct_y_dom=self.oct_y_dom):
            yield i
        
    def put_pixel(self, x, y, colour):
        self.buffer[x][y] = colour
        # delete pixelarray

    def render(self):
        pass # sdl
            
    def put_line(self, pt1, pt2, colour):  # charline from charplotter
        aline = list(self.call_line(pt1,pt2))
        for i in aline:
            x,y = i 
            self.put_pixel(x,y,colour)

    def regupoly(self,points,colour):
        number_of_pnts = len(points)
        for i in range(0,number_of_pnts):
            self.put_line(points[i], points[(i+1)%number_of_pnts],colour)

        
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


class HLineList(object):
    def __init__(self,ystart=0, length=0, drawer=None, use_floats=False, malloc_size=20000):
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
            #self.__hlines_tuples = [[0,0] for i in range(malloc_size)] # fake "malloc"
            self.__hlines_tuples = [[None,None]] # fake "malloc"

        self.drawer = drawer
        self.edgecalc = self.__add_edge_float if use_floats else self.__add_edge_int

    def gettuples(self):
        return self.__hlines_tuples[:]

    def addstart(self,xstart):
        if self.__hlines_tuples[-1][0] is None:
            self.__hlines_tuples[-1][0] = xstart
        else:
            self.__hlines_tuples.append([xstart,None])
        self.startcount += 1

    def addstop(self,xstop):
        if self.__hlines_tuples[self.stopcount][1] is None:
            self.__hlines_tuples[self.stopcount][1] = xstop
        else:
            import pdb;pdb.set_trace()
            raise Exception("what? This is not supposed to happen!")
        self.stopcount += 1         

    def __add_edge_int(self,
                       x1,y1,
                       x2,y2,
                       skipfirst = 0,
                       leftedge=False,
                       char=None):        
        # Chapter 39 GPBB
        edge_to_add_to = self.addstart if leftedge else self.addstop
        
        height = dy = y2-y1 # should always > 0, going down from miny to maxy
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

            # if >= 0 left -> right else right -> left
            error = 0 if dx >= 0 else -height +1                  
            if skipfirst != 0:
                error += width
                if error > 0:
                    x1 += xincr
                    error -= height

            # Basically Bresenham's algo (y dominant case)
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
            x_dom_incr = (width/height)*xincr  # width > height (ints=> 1, 2, etc)
            error_incr = width % height # width > height   ( 0 1 2... height-1, 0, 1...)

            # if >= 0 left -> right else right -> left
            error = 0 if dx >= 0 else -height +1
            if skipfirst != 0:
                x1 += x_dom_incr
                error += error_incr
                if error > 0:
                    x1 += xincr
                    error -= height

            # Basically Bresenham's algo (Y dominant case, adjusted for special case)
            '''
            This is Bresenham for the Y dominant case (even though this is supposed to be the X dominant.)
            
            So the way I understand it is:
            x increases always during the X dominant state.
            y increases only if error value > some threshold, (y increases, error adjusts back to < the threshold)
            
            The problem now is that y will increase regardless of what we want.
            
            it then means that x will have to ADJUSTED AGAIN based on whatever state y finds itself in.

            '''
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
        
            # if self.drawer:
            #     self.drawer.putchar(x,y,char)

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


    def draw_hlines(self,use_tuples=True,colour=0x00ff00):
        if not self.drawer:
            raise Exception("Nothing to draw hlines with")
            
        length_start = len(self.__hlines_start)
        length_stop = len(self.__hlines_stop)
        if length_start != length_stop :
            # not sure about this algo yet...
            raise Exception("Something wrong with your algorithm, stop points(%d) != start points(%d)"%(length_stop,length_start))

        if True:
            tuples = self.gettuples()
            put_pixel = self.drawer.put_pixel
            y = self.ystart
            def per_tuple(idx_and_tuple,local_vals):
                idx,tple = idx_and_tuple  # thanks enumerate
                xstart,xstop = tple
                y = local_vals['y']+idx
                if xstart < xstop:
                    x_range = xrange(xstart,xstop)
                else:
                    x_range = xrange(xstop,xstart)   
                map(partial(put_pixel, y=y, colour=colour),x_range)                

            map(partial(per_tuple,local_vals=locals()), enumerate(tuples)) # local_vals for y

        if False:
            t = self.gettuples()
            put_pixel = self.drawer.put_pixel
            y = self.ystart
            for i in range(0,min([length_start,length_stop])):
                xstart,xstop = t[i]
                y += 1             
                if xstart < xstop:
                    x_range = range(xstart,xstop)
                else:
                    x_range = range(xstop,xstart)   
                map(partial(put_pixel, y=y, colour=colour),[xx for xx in x_range])

        if False:
            t = self.gettuples()
            put_pixel = self.drawer.put_pixel
            for i in range(0,min([length_start,length_stop])):

                xstart,xstop = t[i]
                y = self.ystart+i                
                if xstart < xstop:
                    map(partial(put_pixel, y=y, colour=colour),[xx for xx in range(xstart,xstop)])
                else:
                    map(partial(put_pixel, y=y, colour=colour),[xx for xx in range(xstop,xstart)])

        #else:
        if False:
            t = self.gettuples()
            for i in range(0,min([length_start,length_stop])):

                xstart,xstop = t[i]
                y = self.ystart+i                
                if xstart < xstop:
                    for xx in range(xstart,xstop):
                        self.drawer.put_pixel(xx,y,colour=0xff0000)
                else:
                    for xx in range(xstop, xstart):
                        self.drawer.put_pixel(xx,y,colour=0xff0000)
            


def fill_convex_poly(vertices,drawer=None, debug=False, colour = 0xff0000, hlinelist = None, draw_hlines=True):
    '''
    Basic idea,
    - use everything as indexes.
    - make notes in code about what index is where
    - when iterating, use indexes. simpler to clump x,y vals together
    - Notes to make:
      - When y is smallest,
      - When y is largest.
      - X for left and right side when y is smallest (top left, top right)
      - when top is flat.
      
    '''
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

        # drawer.putchar(nrv.x,nrv.y,'Xn')
        # drawer.putchar(plv.x,plv.y,'Op')

    # gradient from next to center vs
    # gradient from previous to center
    dxn,dyn = dxdy(vertices[next_idx], vertices[miny_left_idx])
    dxp,dyp = dxdy(vertices[previous_idx], vertices[miny_left_idx])

    '''
    Assumptions:
    Previous point (Xp) before min (Xmin) point on X axis.
    Next point  (Xn) after min (Xmin) point on X axis.
    Y is ever in creasing. So Ymin < Yp and Ymin < Yn

    In other "words":

    Xp < Xmin => Xmin > Xp => Xmin-Xp > 0 => DXP > 0
    Xn > Xmin => Xmin < Xn => Xmin-Xn < 0 => DXN < 0 => -DXN > 0
    =>
    (-DXN * DXP) >0

    Ymin < Yn and  Ymin < Yp  # increasing
    
    Ymin - Yn < 0 and Ymin - Yp < 0
    =>
    DYN < 0 and DYP < 0
    
    Alrighty,
    Since DYN < 0 and DYP < 0 then DYN*DYP > 0
    (negative * negative > 0)

    normally:
    Incline of line_xn(between next and min) will be more than line_xp(between previous and min)
      DYP/DXP < DYN/DXN
    => 
      DYP/DXP < DYN/DXN
    =>
      DYP/DXP - DYN/DXN < 0
    =>
      (-DXN * DXP)*(DYP/DXP - DYN/DXN) < 0
    =>
      (-DXN * DXP)*DYP/DXP - (-DXN * DXP)*DYN/DXN < 0
    =>
      - DXN*DYP + (DXP * DYN) < 0
    =>
      (DXP*DYN)-DXN*DYP < 0
      
     if opposite is true (DXP*DYN)-DXN*DXP > 0 then lines are switched

    '''
    if (dxp*dyn - dxn*dyp) > 0:
        # swap.. again !
        miny_left_idx,miny_right_idx = miny_right_idx, miny_left_idx
        left_edge_dir = 1      


    dec_if_flat = 1 if flat else 0
    y_start = miny_point.y + 1 - dec_if_flat
    y_length = vertices[maxy_idx].y - vertices[miny_left_idx].y - 1 + dec_if_flat
    if hlinelist is None:
        hlinelist = HLineList(y_start,y_length,drawer=drawer,use_floats=False)
    else:
        # this case doesnt work yet...
        hlinelist.y_start = y_start
        hlinelist.length = y_length
        hlinelist.drawer = drawer
        
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
            # drawer.putchar(x,hlinelist.ystart+i,'S')

        for i in range(hlinelist.stopcount):
            x = tuples[i][1]
            # drawer.putchar(x,hlinelist.ystart+i,'P')

    if draw_hlines:
        hlinelist.draw_hlines(colour=colour)

    return hlinelist

    #

