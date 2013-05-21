from functools import partial
from itertools import starmap,permutations, combinations_with_replacement

worldform =  [[1,0,0,0],
              [0,1,0,0],
              [0,0,1,0],
              [0,0,0,1]]

polyform =    [[1.0, 0.0, 0.0, 0.0],
               [0.0, 1.0, 0.0, 0.0],
               [0.0, 0.0, 1.0, -140.0],
               [0.0, 0.0, 0.0, 1.0] ]


dest4X4 = [[0 for j in range(4)] for i in range(4)]    
def func(k,j,i,source1, source2, dest):
    dest[i][j] +=  source1[i][k] * source2[k][j]    
    #print k,j,i,dest[i][j],  source1[i][k] , source2[k][j]    
# for i in range(4):
#     for j in range(4):
#         for k in range(4):
#             #dest4X4[i][j] = func(k,j,i, source4X4_first, source4X4_second,dest4X4)
#             func(k,j,i, source4X4_first, source4X4_second,dest4X4)
    
# func_kji = partial(func, dest=dest4X4, source1= worldform, source2 = polyform)
# print list(starmap(func_kji,list(combinations_with_replacement(range(4),r=3))))
# print dest4X4 

def funcx(i,j,k,source1,source2,dest):
    print "k=",k,'j=',j,'i=',i, dest[i][j] ,'+=', source1[i][k] ,'*', source2[k][j],
    dest[i][j] +=  (source1[i][k] * source2[k][j]  )
    print "result", dest[i][j]
print worldform, polyform
dest4X4_2 = [[2 for j in range(4)] for i in range(4)]        
funcy = partial(funcx, source2= worldform, source1=polyform, dest=dest4X4_2)
lcombo = list(combinations_with_replacement(range(4),r=3))
list(starmap(funcy,lcombo))
print dest4X4_2
# for i in  list(combinations_with_replacement(range(4),r=3)):
#     print i
