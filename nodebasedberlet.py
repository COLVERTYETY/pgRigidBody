import numpy as np

the_node_array = []
the_stick_array = []
WIDTH = 400
HEIGHT = 400
nupdates = 5

class structure(object):
    def __init__(self):
        self.nodearray=[]
        self.stickarray=[]
    def allupdate(self):
        global nupdates
        for node in self.nodearray:
            node.update()
        for _ in range(nupdates):
            for stick in self.stickarray:
                stick.update()
    def allpickup(self,m_pos):
        for node in self.nodearray:
            dist = np.linalg.norm(m_pos-node.pos)
            if dist<5:
                node.pickup()
    def allletgo(self):
        for node in self.nodearray:
            node.letgo()
    def motion(self,m_pos):
        for node in self.nodearray:
            node.movedaround(m_pos)

class node(object):
    def __init__(self,pos):
        self.pos = pos
        self.oldpos = pos
        self.acc = np.zeros(2)
        self.grav = np.array([0,1])
        self.pinned = False
        self.pickedup = False
        self.mass = 1
        #the_node_array.append(self)
    
    def pickup(self):
        self.pickedup = True

    def movedaround(self,m_pos):
        if self.pickedup:
            self.pos = m_pos
            self.oldpos = m_pos
    
    def letgo(self):
        if self.pickedup:
            self.pickedup = False

    def update(self):
        if  not self.pinned and not self.pickedup:
            self.accumulateforces()
            self.apply_verlet(1)

    def apply_verlet(self,timestep):
        temp = 2*self.pos - self.oldpos + self.acc*timestep*timestep
        self.oldpos = self.pos
        self.pos = temp
        self.acc = np.zeros(2)
    
    def apply_gravity(self):
        self.acc+=self.grav

    def hardborder(self):
        global WIDTH , HEIGHT
        bouncedrag = 0.4
        vel = (self.pos- self.oldpos)*bouncedrag
        limit = np.array([WIDTH,HEIGHT])
        if np.any(np.greater(self.pos,limit)):
            self.pos = np.minimum(self.pos,limit)
            self.oldpos = np.ma.array((self.pos+vel),mask=np.not_equal(self.pos,limit)).filled(self.oldpos)#we only need to change where there is a difference
        if np.any(np.less(self.pos,np.zeros(2))):
            self.pos = np.maximum(self.pos,np.zeros(2))
            self.oldpos = np.ma.array((self.pos+vel),mask=np.not_equal(self.pos,np.zeros(2))).filled(self.oldpos)

    def accumulateforces(self):
        self.apply_gravity()
        #self.hardborder()

class stick(object):
    def __init__(self,pointa,pointb,length):
        self.pointa = pointa
        self.pointb = pointb
        self.length = length
        self.strain = 0
        #the_stick_array.append(self)
    
    def conraintsticklength(self):
        # distance = np.linalg.norm(self.pointa.pos-self.pointb.pos)
        small = 0.1
        dpos = self.pointa.pos-self.pointb.pos
        ratio = ((self.length - np.linalg.norm(dpos))/self.length)
        self.strain = ratio
        offset = dpos * ratio
        if not self.pointb.pinned and not self.pointb.pickedup:
            self.pointb.pos = self.pointb.pos - (offset*self.pointa.mass)/(self.pointa.mass+self.pointb.mass+small)
        if not self.pointa.pinned and not self.pointa.pickedup:
            self.pointa.pos = self.pointa.pos + (offset*self.pointb.mass)/(self.pointa.mass+self.pointb.mass+small)
    def update(self):
        self.conraintsticklength()
        # self.pointa.hardborder()
        # self.pointb.hardborder()
    def calculatecolor(self):
        var = 2e-09
        mean = -8.022117194929565e-05
        color = (0,0,0)
        if self.strain<mean-var:
            r = int(np.clip(np.abs(self.strain)*1000,0,255))
            color = (r,r//10,0)
        elif  self.strain>mean+var:
            r = int(np.clip(np.abs(self.strain)*1000,0,255))
            color = (0,r//10,r)
        return color

def allupdate():
    global the_node_array , the_stick_array , nupdates
    for node in the_node_array:
        node.update()
    for _ in range(nupdates):
        for stick in the_stick_array:
            stick.update()

def allpickup(m_pos):
    global the_node_array
    for node in the_node_array:
        dist = np.linalg.norm(m_pos-node.pos)
        if dist<5:
            node.pickup()
def allletgo():
    global the_node_array
    for node in the_node_array:
        node.letgo()

def motion(m_pos):
    global the_node_array
    for node in the_node_array:
        node.movedaround(m_pos)

class engine(object):
    def __init__(self,anchor,rotor,torc):
        self.anchor = anchor
        self.rotor = rotor
        self.length = np.linalg.norm(anchor.pos-rotor.pos)
        self.stick = stick(self.anchor,self.rotor,self.length)
        self.torc = torc
    def update(self):
        temp =  self.rotor.pos - self.anchor.pos
        (temp[0],temp[1]) = (-1*temp[1],temp[0])
        temp = self.torc*(temp/np.linalg.norm(temp))
        self.rotor.acc+=temp