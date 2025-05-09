import numpy as np

class estimate_pos:
    def __init__(self,posision):#posision = [latitude,longitude,depth]
        self.posision = posision
        #self.posision = [0,0,0]
    def uppdate(self,heading,speed,depth):
        self.posision[2] = depth
        self.heading_too_vector(heading)
        self.posision[0] += self.vector[0]*speed
        self.posision[1] += self.vector[1]*speed
        
    def heading_too_vector(self,heading):
        #heading 0/360 = [1,0]
        #heading 90 = [0,1]
        #heading 180 = [-1,0]
        #heading 270 = [0,-1]
        self.vector = [np.sin((heading+90)*np.pi/180),np.cos((heading+90)*np.pi/180)]
        