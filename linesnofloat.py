from lineutil import *

crds = [Coord(10,10),
        Coord(10,20),
        Coord(20,20),
        Coord(20,10)]

def oct_x_dom_imp_float(ptA,ptB):
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

    M = 1.0*dy/dx       

    new_error = { 'skipping y': lambda current_error : current_error + M,
                  'adding to y': lambda current_error : current_error + M - 1}
        
    x = startx
    y = starty
    current_error = 0
    while dx > 0:
        dx -= 1      
        x += 1
        a_error =new_error['skipping y'](current_error)
        if a_error < 0.5:
            current_error = new_error['skipping y'](current_error)
        else:
            y = y + yincr
            current_error = new_error['adding to y'](current_error)

        yield x,y


def oct_y_dom_imp_float(ptA,ptB):
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

    M = 1.0*dx/dy

    new_error = { 'skipping x': lambda current_error : current_error + M,
                  'adding to x': lambda current_error : current_error + M -1}
        
    x = startx
    y = starty
    current_error = 0
    while dy > 0:
        dy -= 1      
        y += 1
        a_error =new_error['skipping x'](current_error)
        if a_error < 0.5:
            current_error = new_error['skipping x'](current_error)
        else:
            x = x + xincr
            current_error = new_error['adding to x'](current_error)

        yield x,y





def oct_x_dom_imp(ptA,ptB):
    '''
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


def oct_y_dom_imp(ptA,ptB):
    '''
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




plt2 = CharPlotter(oct_x_dom=oct_x_dom_imp, oct_y_dom=oct_y_dom_imp)
plt2.regupoly(crds,marks='.')
plt2.render()

print list(plt2.line(Coord(10,10),Coord(20,10)))
print list(plt2.line(Coord(20,10),Coord(10,10)))
print list(plt2.line(Coord(10,10),Coord(10,20)))
print list(plt2.line(Coord(10,20),Coord(10,10)))



plt2.oct_x_dom = oct_x_dom_imp
gradient_list = [1,0.75,0.5,0.25,0.15,0.1,0.05,-1]

cases = testcases(gradient_list=gradient_list,start_coord=Coord(10,25), radius=20)
for n,i in enumerate(cases):
    print gradient_list[n],i
    plt2.charline(*i, marks=True)
plt2.render()

gradient_list = [-gradient_list[i] for i in range(len(gradient_list)-1,0,-1)]
cases = testcases(gradient_list=gradient_list,start_coord=Coord(10,25), radius=20)
for n,i in enumerate(cases):
    print gradient_list[n],i
    #import pdb;pdb.set_trace()
    plt2.charline(*i, marks=True)
    print i,dxdy(*i) ,list(plt2.call_line(*i))
#plt2.render()

plt2.regupoly(crds,marks='.')
plt2.regupoly(plt2.create_npoly(x=25,y=14,num_of_corners=5,theta=pi/2),marks='.')
plt2.render()


