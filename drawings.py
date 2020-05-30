import pygame as pg

radius = 5
width = 2


def iterdrawstick(surface,arryofsticks,font):
    for stick in arryofsticks:
        color = stick.calculatecolor()
        drawstick(stick,surface,color)
        #writestrain(stick,surface,font)

def iterdrawnode(surface,arryofnodes):
    for node in arryofnodes:
        drawpoint(node,surface)

def drawpoint(thepoint,surface,color=(255,0,0)):
    global radius
    pg.draw.circle(surface,color,(int(thepoint.pos[0]),int(thepoint.pos[1])),radius)

def writestrain(stick,surface,font):
    text = font.render(str(stick.strain), True, pg.Color('black'))
    pos = (stick.pointa.pos+stick.pointb.pos)/2
    surface.blit(text,(int(pos[0]),int(pos[1])))

def drawstick(thestick,surface,color = (0,0,0)):
    global width
    pg.draw.line(surface,color,(int(thestick.pointa.pos[0]),int(thestick.pointa.pos[1])),(int(thestick.pointb.pos[0]),int(thestick.pointb.pos[1])),width)