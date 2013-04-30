from lineutil import *

crds = [Coord(10,10),
        Coord(10,20),
        Coord(20,20),
        Coord(20,10)]

#plt = CharPlotter()
# gradient_list = [1.75,1.5,1.25,1,0.75,0.5,0.25,0.15]
# gradient_list = [-gradient_list[i] for i in range(len(gradient_list)-1,0,-1)]+gradient_list
# cases = testcases(gradient_list=gradient_list,start_coord=Coord(15,20), radius=20)
# for n,i in enumerate(cases):
#     print gradient_list[n],i
#     plt.charline(*i, marks=True)
# plt.render()

plt2 = CharPlotter()
plt2.regupoly(crds,marks='.')
plt2.render()

print list(plt2.line(Coord(10,10),Coord(20,10)))
print list(plt2.line(Coord(20,10),Coord(10,10)))
print list(plt2.line(Coord(10,10),Coord(10,20)))
print list(plt2.line(Coord(10,20),Coord(10,10)))

def oct_x_dom_imp(ptA,ptB):
    dx, dy = dxdy(ptA,ptB)

    startx,starty = ptA.x,ptA.y
    stopx,stopy = ptB.x,ptB.y

    M = 1.0*dy/dx
    xincr = 1
    if dx < 0:
        dx = -dx        
        xincr = -1
        
    yincr = 1
    if dy < 0:
        dy = -dy
        yincr = -1
        
    new_error = { 'skipping y': lambda current_error : current_error + M,
                  'adding to y': lambda current_error : current_error + M - 1}
    x = startx
    y = starty
    current_error = 0
    while dx > 0:
        dx -= 1      
        x += 1
        if new_error['skipping y'](current_error) < 0.5:
            current_error = new_error['skipping y'](current_error)
        else:
            y += yincr
            current_error = new_error['adding to y'](current_error)

        yield x,y


plt2.oct_x_dom = oct_x_dom_imp
gradient_list = [0.75,0.5,0.25,0.15]
cases = testcases(gradient_list=gradient_list,start_coord=Coord(15,20), radius=20)
for n,i in enumerate(cases):
    print gradient_list[n],i
    plt2.charline(*i, marks=True)
plt2.render()
