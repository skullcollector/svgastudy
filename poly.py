from lineutil import *

# assuming poly vertices are in order..
# square
poly1 = [Coord(0,0)]
poly1 = poly1+ [poly1[0].add(y=10),
                poly1[0].add(x=10,y=10),
                poly1[0].add(x=10), ]


# diamond
poly2 = [Coord(20,0)]
poly2 = poly2+[poly2[0].add(x=-10,y=10),
               poly2[0].add(x=10,y=10),
               poly2[0].add(x=20,y=20),]

def vertirate(vertices,backward=False):
    '''
    should use itertools.cycle, but want to get into C mode just now..
    '''
    length = len(vertices)
    i = 0 if not backward else length-1
    while True:
        
        yield vertices[i]
        if backward:
            i = (length+(i-1))%length    
        else:
            i = (i+1)%length
        
# v = vertirate("Test string 123",True)
# for i in range(0,100):
#     print v.next()
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

print find_y_bounds(poly2)
print poly2
