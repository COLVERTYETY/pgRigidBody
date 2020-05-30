import nodebasedberlet as nverlet
import numpy as np

def make_a_net():
    the_grid = []
    nodelust = []
    xoffset = 100
    yoffset = 100
    standard = 60
    for i in range(10):
        temp = []
        for j in range(10):
            tt = nverlet.node(np.array([xoffset+standard*i,yoffset+standard*j]))
            temp.append(tt)
            nodelust.append(tt)
        the_grid.append(temp)

    the_grid[0][0].pinned = True
    the_grid[len(the_grid)-1][0].pinned = True

    stickarry = []
    for line in range(len(the_grid)):
        for row in range(len(the_grid[line])):
            if row > 0:
                stickarry.append( nverlet.stick(the_grid[line][row-1],the_grid[line][row],standard))
            if line > 0:
                stickarry.append( nverlet.stick(the_grid[line-1][row],the_grid[line][row],standard))

    thestruct  = nverlet.structure()
    thestruct.nodearray = nodelust
    thestruct.stickarray = stickarry
    return thestruct
