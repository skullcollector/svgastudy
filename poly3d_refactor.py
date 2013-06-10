'''
I want to do lightling, but my own code is confusing me.

I need refactor of poly3d.

I want to focus on simplifying :

- remove dependency on gfxutil [DONE]
- simplify DDA (like bresenham) to use as module.
- USE ONLY 3 points or numpy arrays. This mixing is causeing confusion
- Coordinate types: Object --> World --> View --> Screen (the pipeline?)
- SIMPLE CODE!!!

'''
import pygame
from pygame.locals import *
from math import pi, cos,sin
import numpy

PROJECTION_RATIO =-5.0
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 800


# class Coord(object):
#     '''
#     Immutable
#     '''
#     def __init__(self, x=0,y=0,z=0,w=0):
#         dimensions = 4       # hardcoded, for now.
#         self._numarray=numpy.zeros(3, dtype=numpy.int) 
#         self._numarray[0] = x
#         self._numarray[1] = y   
#         self._numarray[2] = z
#         # self._numarray[3] = 0 
   
#     def get_x(self):
#         return self._numarray[0]
#     def set_x(self,value):
#         self._numarray[0] = value
#     x = property(get_x,set_x)

#     def get_y(self):
#         return self._numarray[1]       
#     def set_y(self,value):
#         self._numarray[1] = value
#     y = property(get_y,set_y)

#     def get_z(self):
#         return self._numarray[2]       
#     def set_z(self,value):
#         self._numarray[2] = value
#     z = property(get_z,set_z)
    
#     def __add__(self, other):
#         return self._numarray+other._numarray
       
#     def __sub__(self, other):
#         return self._numarray-other._numarray 

#     @property
#     def length(self):
#         return numpy.sqrt(numpy.sum(self._numarray*self._numarray))

#     @property
#     def square_length(self):
#         return numpy.sum(self._numarray*self._numarray)

#     @property
#     def unit(self):
#         retval = Coord()
#         retval._numarray = self._numarray/self.length
#         return retval


class Coord(object):
    '''
    Immutable
    '''
    def __init__(self, x=0,y=0,z=0,w=0):
        self._numarray=numpy.array([ [x],
                                     [y],
                                     [z]],dtype=numpy.int) 

    @property
    def as_array(self):
        return numpy.append(self._numarray,numpy.array([[1]]),axis=0)

    def get_x(self):
        return self._numarray[0,0]
    def set_x(self,value):
        self._numarray[0,0] = value
    x = property(get_x,set_x)

    def get_y(self):
        return self._numarray[1,0]       
    def set_y(self,value):
        self._numarray[1,0] = value
    y = property(get_y,set_y)

    def get_z(self):
        return self._numarray[2,0]       
    def set_z(self,value):
        self._numarray[2,0] = value
    z = property(get_z,set_z)
    
    def __add__(self, other):
        return self._numarray+other._numarray
       
    def __sub__(self, other):
        return self._numarray-other._numarray 

    @property
    def length(self):
        return numpy.sqrt(numpy.sum(self._numarray*self._numarray))

    @property
    def square_length(self):
        return numpy.sum(self._numarray*self._numarray)

    @property
    def unit(self):
        retval = Coord()
        retval._numarray = self._numarray/self.length
        return retval



circdec = lambda i,length: (length+(i-1))%length
circinc = lambda i,length: (i+1)%length
dxdy = lambda start,stop : (stop.x - start.x, stop.y - start.y)
def vertice_iterate(vertices,backward=False):
    '''
    should use itertools.cycle, but want to get into C mode just now..
    v = vertice_iterate("Test string 123",True)  # True means reverse iterate
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
    vgen = vertice_iterate(vertices)
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
    def __init__(self,ystart=0, length=0, drawer=None, use_floats=False):
        self.__hlines_tuples = None
        self.ystart = ystart
        self.length = length
        self.startcount = 0
        self.stopcount = 0
        if length <=0:
            self.__hlines_tuples = [[0,0]]
        else:
            self.__hlines_tuples = [[None,None]] # fake "malloc"

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

    def add_edge_int(self,
                     x1,y1,
                     x2,y2,
                     skipfirst = 0,
                     leftedge=False):
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

            i = height - skipfirst
            while i > 0:
                i -= 1
                edge_to_add_to(x1)

        elif width == height:
            ''' diagonal '''

            x1 = x1+xincr if skipfirst else x1

            i = height - skipfirst
            while i > 0:
                i -= 1
                edge_to_add_to(x1)
                x1 += xincr

        elif height > width:
            ''' y dominant '''
            
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
            x_dom_incr = (width/height)*xincr  # width > height (ints=> 1, 2, etc)
            error_incr = width % height # width > height   ( 0 1 2... height-1, 0, 1...)

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

    def scanedge_left(self,
                      x1,y1,
                      x2,y2,
                      skipfirst = 0):
        self.add_edge_int(x1,y1,
                          x2,y2,
                          skipfirst = skipfirst,
                          leftedge=True)
                  
    def scanedge_right(self,
                      x1,y1,
                      x2,y2,
                      skipfirst = 0):
        self.add_edge_int(x1,y1,
                          x2,y2,
                          skipfirst = skipfirst,
                          leftedge=False)

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
    # global circinc,circdec
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
   
def xformvec(xform4X4, source4X1):
    #print xform4X4,source4X1.as_array
    #return xform4X4*source4X1.as_array    
    return xform4X4*source4X1.as_array

def concat_x_forms(source4X4_first, source4X4_second):   
    return source4X4_first * source4X4_second

def isbackface(polypts):
    v1 = float(polypts[1][0] - polypts[0][0])
    v2 = float(polypts[1][1] - polypts[0][1])

    w1 = float(polypts[-1][0] - polypts[0][0])
    w2 = float(polypts[-1][1] - polypts[0][1])
    
    xproduct = v1*w2 - v2*w1
    return xproduct > 0

def xform_and_project_poly(surface, xform4X4, polypts3d, colour = 0x00ff00,draw_hlines=False):
    polypts2d = []
    txpolypts_array = []
    for pt in polypts3d:
        xxx = xformvec(xform4X4,pt)
        print xxx
        txpolypts_array.append(xxx)
    #print txpolypts_array
    for txpolypt in txpolypts_array:
        xval,yval,zval,wval = txpolypt
        '''
        so far theory is:
        we start at center point x,y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
        if the 3d point goes to the left or right it moves by by xval/zval (zval larger, perceived xposition further away)
        if the 3d point goes to up or down it moves by by yval/zval.
        '''
        new_x = int(round((1.0*xval/zval * 1.0  * PROJECTION_RATIO*(SCREEN_WIDTH/2.0)+0.5) + SCREEN_WIDTH/2)) if zval != 0 else xval
        new_y = int(round((1.0*yval/zval * -1.0 * PROJECTION_RATIO*(SCREEN_WIDTH/2.0)+0.5) + SCREEN_HEIGHT/2)) if zval != 0 else yval
        polypts2d.append(Coord(new_x,new_y))  
        #print new_x,new_y
    return fill_convex_poly(polypts2d,drawer=None,colour=colour,draw_hlines=draw_hlines),isbackface(txpolypts_array)
    
def render(surface,rotation=0, new_hotness=True):
    # vertices = [
    #     numpy.array([[-30],
    #                  [-15],
    #                  [-1],
    #                  [1]]),
    #     numpy.array([[0],
    #                  [15],
    #                  [0],
    #                  [1]]),
    #     numpy.array([[10],
    #                  [-5],
    #                  [0],
    #                  [1]])
    #     ]
    vertices = [ Coord(-30,-15,-1), Coord(0,15,0), Coord(10,-5, 0)]
    worldform =  numpy.matrix([[1,0,0,0],
                               [0,1,0,0],
                               [0,0,1,0],
                               [0,0,0,1]])

    polyform =    numpy.matrix([[1.0, 0.0, 0.0, 0.0],
                                [0.0, 1.0, 0.0, 0.0],
                                [0.0, 0.0, 1.0, -140.0],
                                [0.0, 0.0, 0.0, 1.0] ])

    polyform[0,0] = polyform[2,2] = cos(rotation)
    polyform[0,2] = sin(rotation)
    polyform[2,0] = -polyform[0,2]

    worldviewxform = concat_x_forms(worldform, polyform)
    draw_hlines = False if new_hotness else True
    hlinesdata,is_behind_poly = xform_and_project_poly(surface, worldviewxform, vertices, draw_hlines=draw_hlines)
    if not draw_hlines:
        vals = hlinesdata.gettuples()
        #print vals
        temp_array = numpy.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))   
        '''
        stil calculates polys even if not facing... bad? unnecesary?
        '''
        if not is_behind_poly:
            y = hlinesdata.ystart
            for v in vals:
                #v = v[0][0], v[1][0]
                #print v
                x1, x2 = v
                if x1 > x2:                
                    temp_array[x2:x1,y].fill(0xff0000)
                else:
                    temp_array[x1:x2,y].fill(0x00ff00)
                y += 1
        pygame.surfarray.blit_array(surface,temp_array)

clock = pygame.time.Clock()
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    rotation = 0
    
    while running:
        
        render(screen,rotation*pi/30)
        rotation += 1
        for event in pygame.event.get():
            if event.type == KEYDOWN: #QUIT:
                running = False
            else:
                print event
                

        pygame.display.flip()
        clock.tick(40)
        screen.fill((0,0,0))
        
    pygame.quit()
  
if __name__=='__main__':
    main()
