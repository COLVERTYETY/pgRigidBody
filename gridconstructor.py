import nodebasedberlet as nverlet
import numpy as np

descriptor = [
    [00,00,00,00,10,00],
    [00,00,00,10,00],
    [00,00,10,00],
    [00,10,00],
    [10,00],
    [00],
]

generatedstructure = nverlet.structure()

firstpos = np.array([400,200])
secondpos = np.array([380,150])

firstnode  = nverlet.node(firstpos)
firstnode.pinned = True
secondnode = nverlet.node(secondpos)
secondnode.pinned = True
nodelist  = []
for i in range(len(descriptor)):
    nodelist.append(nverlet.node())
nodelist[0] = firstnode
nodelist[len(nodelist)-1] = secondnode
generatedstructure.nodearray = nodelist

for line in range(len(nodelist)):
    for j in range(len(nodelist[line])):
        pass
