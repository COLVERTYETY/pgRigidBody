import sys
import pygame as pg
import numpy as np
import drawings as dr
import nodebasedberlet as nverlet
import net
WIDTH = 800
HEIGHT = 800
(nverlet.WIDTH,nverlet.HEIGHT) = (WIDTH-10,HEIGHT-10)
pg.init()#pylint: disable=no-member
screen = pg.display.set_mode((WIDTH,HEIGHT))
tempsurf = pg.Surface((WIDTH,HEIGHT)) #pylint: disable=too-many-function-args
tempsurf.fill((255,255,255))
done = False
font = pg.font.Font(None, 30)
clock = pg.time.Clock()
leftisdown = False
"""
initialize objs
"""

"""
the chain
"""
# thestrucutre = nverlet.structure()
# pointd = nverlet.node(np.array([200,120]))
# pointe = nverlet.node(np.array([300,120]))
# pointe.pinned = True
# theengine = nverlet.engine(pointe,pointd,3)

# """
# the triangle
# """
# pointa = nverlet.node(np.array([100,100]))
# pointa.oldpos = np.array([90,110])
# pointb = nverlet.node(np.array([150,150]))
# pointb.oldpos = np.array([160,150])
# pointc = nverlet.node(np.array([100,150]))
# stickab = nverlet.stick(pointa,pointb,50)
# stickac = nverlet.stick(pointa,pointc,50)
# stickcb = nverlet.stick(pointc,pointb,50)

# stickcd = nverlet.stick(pointc,pointd,90)

# thestrucutre.nodearray.extend([pointa,pointb,pointc,pointd,pointe])
# thestrucutre.stickarray.extend([stickab,stickac,stickcb,stickcd,theengine.stick])
"""
make a net
"""
thestrucutre = net.make_a_net()
"""
do one render for pause
"""
# screen.fill((255,255,255))
# screen.blit(tempsurf,(0,0))
# dr.iterdrawnode(screen,nverlet.the_node_array)
# dr.iterdrawstick(screen,nverlet.the_stick_array,font)
# pg.display.flip()
# input()
while not done:
    for event in pg.event.get():
                if event.type == pg.QUIT:# pylint: disable=no-member
                    done = True
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:  #pylint: disable = no-member
                        if event.button== 1:#LEFT
                                mpos = np.array([*pg.mouse.get_pos()])
                                leftisdown = True
                                thestrucutre.allpickup(mpos)
                if event.type == pg.MOUSEBUTTONUP: #pylint: disable = no-member
                        if event.button==1:
                                leftisdown = False
                                thestrucutre.allletgo()
                if event.type == pg.MOUSEMOTION:#pylint: disable = no-member
                        if leftisdown:
                                mpos = np.array([*pg.mouse.get_pos()])
                                thestrucutre.motion(mpos)      
    
    """
    update nodes
    """
    # pointa.update()
    # pointb.update()
    # thestick.updateloop()
    #thestruct.update()
    thestrucutre.allupdate()
    #theengine.update()
    """
    draw stuff
    """
    screen.fill((255,255,255))
    #screen.blit(tempsurf,(0,0))
    #pg.draw.circle(tempsurf,(200,200,200),(int(pointa.pos[0]),int(pointa.pos[1])),1)
    dr.iterdrawnode(screen,thestrucutre.nodearray)
    dr.iterdrawstick(screen,thestrucutre.stickarray,font)
    fps = font.render(str(int(clock.get_fps())), True, pg.Color('black'))
    screen.blit(fps, (10, 10))
    clock.tick(300)
    pg.display.flip()


    