'''
I want to do lightling, but my own code is confusing me.

I need refactor of poly3d.

I want to focus on simplifying :

- remove dependency on gfxutil [DONE]
- simplify DDA (like bresenham) to use as module.
- USE ONLY 3 points or numpy arrays. This mixing is causeing confusion [Done?]
- Coordinate types: Object --> World --> View --> Screen (the pipeline?)
- SIMPLE CODE!!!

'''
import pygame
from pygame.locals import *
from math import pi, cos,sin
import numpy

PROJECTION_RATIO =-5.0
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 800


# ------------------ 3d Graphics
class Vector(object):
    '''
    Immutable
    '''
    def __init__(self, x=0,y=0,z=0,w=0):
        self._numarray=numpy.array([ [x],
                                     [y],
                                     [z]],dtype=numpy.int) 
    
    def __repr__(self):
        #import pdb; pdb.set_trace()
        return "<XYZ:%s>"%(str(self._numarray))


    def get_array(self):
        return numpy.append(self._numarray,numpy.array([[1]]),axis=0)
    def set_array(self,input_array):        
        self._numarray = numpy.array(input_array[:3])
    array = property(get_array,set_array)

    def transform(self, xform4X4):
        v = Vector()
        v.array = xform4X4*self.array
        return v

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

    def dot(self,other):
        return self._numarray.T[0].dot(other._numarray.T[0])[0]  # sigh.. ugly

    @property
    def length(self):
        return numpy.sqrt(numpy.sum(self._numarray*self._numarray))

    @property
    def square_length(self):
        return numpy.sum(self._numarray*self._numarray)

    @property
    def unit(self):
        retval = Vector()
        retval._numarray = self._numarray/self.length
        return retval

class Coord(Vector):
    pass
 

class Polygon(list):  

    def transform(self, xform4X4):
        tx_pts = Polygon()
        for pt in self:
            tx_pts.append(pt.transform(xform4X4))
            #import pdb; pdb.set_trace()
            #print type(tx_pts[-1])
        return tx_pts

    def gen_vertices(self,backward=False):
        _circdec = lambda i,length: (length+(i-1))%length
        _circinc = lambda i,length: (i+1)%length

        '''
        should use itertools.cycle, but want to get into C mode just now..
        v = vertice_iterate("Test string 123",True)  # True means reverse iterate
        for i in range(0,100):
            print v.next()
    
        '''
    
        length = len(self)
        i = 0 if not backward else length-1
        while True:        
            yield self[i]
            if backward:
                i = _circdec(i,length)
            else:
                i = _circinc(i,length)


    def find_y_bounds(self):
        length = len(self)
        if length ==0:
            return None
        
        at_min_y = at_max_y = self[0]  # at at_min_y or at at_max_y
        min_idx = max_idx = 0
        i = 0
        vgen = self.gen_vertices() #vertice_iterate(vertices)
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

        

    @property
    def facing(self):
        v = self[1] - self[0]
        w = self[-1] - self[0]
        return (v[0]*w[1] - v[1]*w[0]) < 0

    @property
    def normal(self):
        v = self[1] - self[0]
        w = self[-1] - self[0]

        return Vector((v[1]*w[2] - v[2]*w[1]),
                      (v[2]*w[0] - v[0]*w[2]),
                      (v[0]*w[1] - v[1]*w[0]))


    def project(self):
        poly2d = Polygon()
        for pt in self:
            xval,yval,zval,wval = pt.array
            new_x = int(round((1.0*xval/zval * 1.0  * PROJECTION_RATIO*(SCREEN_WIDTH/2.0)+0.5) + SCREEN_WIDTH/2)) if zval != 0 else xval
            new_y = int(round((1.0*yval/zval * -1.0 * PROJECTION_RATIO*(SCREEN_WIDTH/2.0)+0.5) + SCREEN_HEIGHT/2)) if zval != 0 else yval
            poly2d.append(Coord(new_x,new_y))
        return poly2d
                        
       

class HLineList(object):
    def __init__(self,ystart=0):
        self.__hlines_tuples = None
        self.ystart = ystart
        self.startcount = 0
        self.stopcount = 0
        self.__hlines_tuples = [[None,None]] 

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

def fill_convex_poly(vertices, debug=False, hlinelist = None):
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
    circdec = lambda i,length: (length+(i-1))%length
    circinc = lambda i,length: (i+1)%length
    dxdy = lambda start,stop : (stop.x - start.x, stop.y - start.y)

    # GPBB Chapter 38
    # global circinc,circdec
    length = len(vertices)
    if length == 0:
        return None
    miny_maxy_idxes =  vertices.find_y_bounds() #find_y_bounds(vertices)
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

        
    left_edge_dir = -1  # left edge indexing direction
    if flat:
        if vertices[miny_left_idx].x > vertices[miny_right_idx].y:
            # py swap!
            miny_left_idx, miny_right_idx = miny_right_idx, miny_left_idx
            left_edge_dir = 1

    next_idx = circdec(miny_right_idx,length)    
    previous_idx = circinc(miny_left_idx,length)    


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
    hlinelist = HLineList(y_start)

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

    return hlinelist  


def rotate_poly_matrix(rotation):
    cos_rotation = cos(rotation)
    sin_rotation = sin(rotation)
    polyform     = numpy.matrix([[cos_rotation,            0.0, sin_rotation,    0.0],
                                 [0.0,                     1.0, 0.0,             0.0],
                                 [-sin_rotation,           0.0, cos_rotation, -180.0],
                                 [0.0,                     0.0, 0.0,             1.0] ])
    return polyform
#colour = 0
#-------------------------------------------------
# ------------------ Colour/Palette stuff for light


# #define DOT_PRODUCT(V1,V2) \
#    (FixedMul(V1.X,V2.X)+FixedMul(V1.Y,V2.Y)+FixedMul(V1.Z,V2.Z))
#dot_product =lambda v1,v2: v1.x*v2.x + v1.y*v2.y + v1.z*v2.z
dot_product =lambda v1,v2: v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

class RGBModel(object):
    def __init__(self,red=0,green=0,blue=0):
        self._numarray = numpy.array([colour_comp for colour_comp in [red,green,blue]])
        #print self._numarray
        
    def __repr__(self):
        #import pdb; pdb.set_trace()
        data = tuple([str(colelem) for colelem in [self._numarray[0],self._numarray[1],self._numarray[2]]])
        return "<red:%s,green:%s,blue:%s>"%data
        
    def get_red(self):
        return self._numarray[0]       
    def set_red(self,value):
        self._numarray[0] = value
    red = property(get_red,set_red)
      
    def get_green(self):
        return self._numarray[1]       
    def set_green(self,value):
        self._numarray[1] = value
    green= property(get_green,set_green)

    def get_blue(self):
        return self._numarray[2]       
    def set_blue(self,value):
        self._numarray[2] = value
    blue= property(get_blue,set_blue)

    def __mul__(self,other):
        returnvalue = RGBModel(0,0,0)

        if isinstance(other, float) or isinstance(other, int):
             returnvalue._numarray = self._numarray*other
             return returnvalue

        product_array = self._numarray*other._numarray
        returnvalue._numarray = numpy.where(product_array < 255, product_array, 255)
        return returnvalue
 
    def __add__(self, other):
        returnvalue = RGBModel(0,0,0)
        returnvalue._numarray = self._numarray + other._numarray
        return returnvalue
        

class ColourModel(RGBModel):
    pass

class IntensityModel(RGBModel):
    pass

gamma4_levs = [0,39,53,63]
gamma64_levs = [ 0, 10, 14, 17, 19, 21, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34,
                 35, 36, 37, 37, 38, 39, 40, 41, 41, 42, 43, 44, 44, 45, 46, 46,
                 47, 48, 48, 49, 49, 50, 51, 51, 52, 52, 53, 53, 54, 54, 55, 55,
                 56, 56, 57, 57, 58, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63];

def set_palette(surface):
    cmap = numpy.zeros((256,3))
    red,green,blue = 0,1,2

    for r in range(0,4):
        for g in range(0,4):
            for b in range(0,4):
                idx = (r<<4)+(g<<2)+b;
                cmap[idx, :]= gamma4_levs[r], gamma4_levs[g], gamma4_levs[b]

    for r in range(0,64):
        cmap[64+r, :] = gamma64_levs[r], 0,0

    for g in range(0,64):
        cmap[128+g, :] = 0, gamma64_levs[g], 0

    for b in range(0,64):
        cmap[192+b, :] = 0,0,gamma64_levs[b]

    surface.set_palette(cmap)

def get_colour_index(colour_model):
    # I think this index calc is dodgey. Might need upgrade, need to test more
    import math
    intround = lambda x : int(math.floor(x)) 
    #intround = lambda x : int(math.floor((x*1000.0)/1000.0))

    red = intround(colour_model.red)
    green = intround(colour_model.green)
    blue = intround(colour_model.blue)

    if red == 0 and green == 0 and blue !=0:
        return 192+(blue >> 2)

    if red == 0 and blue == 0 and green != 0:
        return 128+(green >> 2)

    if blue == 0 and green == 0 and red != 0:
        return 64+(red >> 2)
    
    ret =  (((red & 0xC0) >>2)|
            ((green & 0xC0) >>4)|
            ((blue & 0xC0) >>6))
    #print ret,colour_model
    return ret

model_intensity = IntensityModel(0.0,0.0,0.0)

class SpotLight(object):
    def __init__(self, direction_vector, intensity_model):
        self.direction_vector = direction_vector
        self.intensity_model = intensity_model

spotlights = []
spotlights.append(SpotLight(Vector(-1,-1,-1), IntensityModel(0.0,0.6,0.0)))
spotlights.append(SpotLight(Vector(1,1,-1), IntensityModel(0.6,0.0,0.0)))
spotlights.append(SpotLight(Vector(-1,0,0), IntensityModel(0.0,0.0,0.6)))


cur_colour = None

def xform_and_project_poly(surface, xform4X4, polypts3d, debug=False):
    global cur_colour
    
    polypts2d = Polygon()
    
    
    txpolypts_array= polypts3d.transform(xform4X4)
    
    intensity = IntensityModel(0,0,0)
    for spot in spotlights:
        diffusion = txpolypts_array.normal.unit.dot( spot.direction_vector)
        if diffusion > 0:
            intensity = intensity + spot.intensity_model*diffusion

    cur_colour = ColourModel(255,255,255) * intensity
    
    if debug: print intensity, diffusion,cur_colour

    retvals = None
    if txpolypts_array.facing:
        polypts2d = txpolypts_array.project()
        retvals = fill_convex_poly(polypts2d)

    return retvals

vertices = Polygon([ Coord(-30,-15,-20), Coord(0,15,-10), Coord(10,-5, -10)])

#-------------------------------------------------
def render(surface,rotation=0):

    worldform =  numpy.matrix([[1,0,0,0],
                               [0,1,0,0],
                               [0,0,1,0],
                               [0,0,0,1]])  

    polyform = rotate_poly_matrix(rotation)

    worldviewxform =  polyform * worldform

    hlinesdata = xform_and_project_poly(surface, worldviewxform, vertices)
    temp_array = numpy.zeros((SCREEN_WIDTH, SCREEN_HEIGHT))   
  
    if hlinesdata:
        y = hlinesdata.ystart
        for v in hlinesdata.gettuples():
            x1, x2 = v
            # colour  += 50
            # colour = colour %255
            if x1 > x2:                
                #print cur_colour, get_colour_index(cur_colour)
                temp_array[x2:x1,y].fill(get_colour_index(cur_colour))
            # else:
            #     temp_array[x1:x2,y].fill(0x00ff00)
            y += 1
    pygame.surfarray.blit_array(surface,temp_array)

clock = pygame.time.Clock()
def main():
    global cur_colour
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,8)

    running = True
    rotation = 0
    set_palette(screen)
    cur_colour = ColourModel(255,255,255)
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
