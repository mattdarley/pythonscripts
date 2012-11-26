# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 16:29:01 2012

@author: matt
"""

import exceptions
import numpy as np

#mshStructure
#Header
#   MSHX1     
#   GROUPS 98
#Group1
#   LABEL Payload bay door R_Color1
#   MATERIAL 1
#   TEXTURE 0
#   GEOM 154 260
#   -1.6555803e-17 3.1436993 2.3 1.7317608e-2 0.99985002 1.8587557e-4 
#   0.29180471 3.1285329 1.3298007 0.10386067 0.99459186 -1.6189888e-17 
#   ...(154)
#   2 1 0
#   5 4 3
#   ...(260)
#Group2
#   LABEL Payload bay door R_Hvitegrey
#   MATERIAL 5
#   TEXTURE 0
#   GEOM 416 340
#   -1.6352000e-17 3.1436993 -10.0 0.0 0.0 -1.0 
#   -1.6352000e-17 3.1136993 -10.0 0.0 0.0 -1.0 
#   ...(416)
# etc
#Materials
#   MATERIALS 10
#   Color1
#   Color2
#   Dish
#   Engine
#   Hvitegrey
#   Metal
#   Radiator
#   Robotic_arm
#   Tail_auv
#   Tyres
#   MATERIAL Color1
#   0.25 0.25 0.25 1.0
#   0.025 0.025 0.025 1.0
#   1.0 1.0 1.0 1.0 99
#   0.0 0.0 0.0 1.0
#   MATERIAL Color2



class OrbiterGroup(object):
    def __init__(self):
        self.name=""
        self.nvertices=0
        self.nfacets=0
        self.vertices=np.zeros((1,3),dtype=np.float)
        self.facets=np.zeros((1,3),dtype=np.int)

    def populate(self, fin):
        self.vertices=np.zeros((self.nvertices,3),dtype=np.float)
        self.facets=np.zeros((self.nfacets,3),dtype=np.int)
        for i in range(self.vertices.shape[0]):
            line=fin.readline()
            self.vertices[i][0]=num(line.split(" ")[0])
            self.vertices[i][1]=num(line.split(" ")[1])
            self.vertices[i][2]=num(line.split(" ")[2])
        for i in range(self.facets.shape[0]):
            line=fin.readline()
            self.facets[i][0]=num(line.split(" ")[0])
            self.facets[i][1]=num(line.split(" ")[1])
            self.facets[i][2]=num(line.split(" ")[2])
            
    def groupInfo(self, fin, name):
        self.name = name
        line=fin.readline()
        while line.split(" ")[0]!="GEOM":
            line=fin.readline()
        self.nvertices=num(line.split(" ")[1])
        self.nfacets=num(line.split(" ")[2])


class OrbiterMsh(object):
    def __init__(self, num):
        self.groups=num
        self.group= [OrbiterGroup() for each in range(num)]

# parse numeric string to integer or float
# credit: Javier on http://stackoverflow.com/questions/379906/python-parse-string-to-float-or-int
def num (s):
    try:
        return int(s)
    except exceptions.ValueError:
        return float(s)



fin=open('Skylon.msh','r')

a=fin.readline()
while a.split(" ")[0]!="GROUPS":
    a=fin.readline()
print a

mshGroups=OrbiterMsh(num(a.split(" ")[1]))

for i in range(mshGroups.groups):
    while a.split(" ")[0]!="LABEL":
        a=fin.readline()
    mshGroups.group[i].groupInfo(fin,a.partition(" "))
    mshGroups.group[i].populate(fin)

fin.close()

for j in range(mshGroups.groups):
    print mshGroups.group[j].nvertices
    print mshGroups.group[j].vertices
    print mshGroups.group[j].nfacets
    print mshGroups.group[j].facets
    
