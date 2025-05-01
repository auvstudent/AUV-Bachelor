import pygame
import numpy as np

class wire_frame:
    def __init__(self,df):
        self.df = df
        self.count = 0
        self.countway = 1
        self.rot2 = 0
        self.back_color = "black"
        self.scale = 20
        self.distance = 40
        self.paint_distance = 1
        self.paint = self.distance-self.paint_distance
        self.camera = np.array([0,-self.distance,4]).reshape(3,1)
        # form x y z
        self.x = np.array([2,0,0]).reshape(3,1)
        self.y = np.array([0,2,0]).reshape(3,1)
        self.z = np.array([0,0,2]).reshape(3,1)
        
        
        self.root = 1+np.sqrt(2)
        self.origo = np.array([0,0,0]).reshape(3,1)
        self.b1 = np.array([-10,1,self.root]).reshape(3,1)
        self.b2 = np.array([-10,self.root,1]).reshape(3,1)
        self.b3 = np.array([-10,self.root,-1]).reshape(3,1)
        self.b4 = np.array([-10,1,-self.root]).reshape(3,1)
        self.b5 = np.array([-10,-1,-self.root]).reshape(3,1)
        self.b6 = np.array([-10,-self.root,-1]).reshape(3,1)
        self.b7 = np.array([-10,-self.root,1]).reshape(3,1)
        self.b8 = np.array([-10,-1,self.root]).reshape(3,1)
        
        self.f1 = np.array([10,1,self.root]).reshape(3,1)
        self.f2 = np.array([10,self.root,1]).reshape(3,1)
        self.f3 = np.array([10,self.root,-1]).reshape(3,1)
        self.f4 = np.array([10,1,-self.root]).reshape(3,1)
        self.f5 = np.array([10,-1,-self.root]).reshape(3,1)
        self.f6 = np.array([10,-self.root,-1]).reshape(3,1)
        self.f7 = np.array([10,-self.root,1]).reshape(3,1)
        self.f8 = np.array([10,-1,self.root]).reshape(3,1)
        
        self.t1 = np.array([-3,1/3,self.root/3]).reshape(3,1)
        self.t2 = np.array([-3,self.root/3,1/3]).reshape(3,1)
        self.t3 = np.array([-3,self.root/3,-1/3]).reshape(3,1)
        self.t4 = np.array([-3,1/3,-self.root/3]).reshape(3,1)
        self.t5 = np.array([-3,-1/3,-self.root/3]).reshape(3,1)
        self.t6 = np.array([-3,-self.root/3,-1/3]).reshape(3,1)
        self.t7 = np.array([-3,-self.root/3,1/3]).reshape(3,1)
        self.t8 = np.array([-3,-1/3,self.root/3]).reshape(3,1)
        self.t_origo = np.array([0,0,0]).reshape(3,1)
        
        self.points_origin = [self.origo,self.x,self.y,self.z,
                              self.b1,self.b2,self.b3,self.b4,self.b5,self.b6,self.b7,self.b8,
                              self.f1,self.f2,self.f3,self.f4,self.f5,self.f6,self.f7,self.f8,
                              self.t_origo,self.t1,self.t2,self.t3,self.t4,self.t5,self.t6,self.t7,self.t8]
        
        self.points = [self.origo,self.x,self.y,self.z,
                       self.b1,self.b2,self.b3,self.b4,self.b5,self.b6,self.b7,self.b8,
                       self.f1,self.f2,self.f3,self.f4,self.f5,self.f6,self.f7,self.f8,
                       self.t_origo,self.t1,self.t2,self.t3,self.t4,self.t5,self.t6,self.t7,self.t8]
        
        self.truster_points_origin = [self.t_origo,self.t1,self.t2,self.t3,self.t4,self.t5,self.t6,self.t7,self.t8]
        
        #self.truster_points = [self.t_origo,self.t1,self.t2,self.t3,self.t4,self.t5,self.t6,self.t7,self.t8]
        
        
        self.edges = [[0,1],[0,2],[0,3],
                      [4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,4],
                      [12,13],[13,14],[14,15],[15,16],[16,17],[17,18],[18,19],[19,12],
                      [4,12],[5,13],[6,14],[7,15],[8,16],[9,17],[10,18],[11,19],
                      [20,21],[20,22],[20,23],[20,24],[20,25],[20,26],[20,27],[20,28],
                      [21,22],[22,23],[23,24],[24,25],[25,26],[26,27],[27,28],[28,21],]
        
        self.board_dim = (1204,780)
        
        self.mid = (self.board_dim[0]/2,self.board_dim[1]/2)
        self.board = pygame.Surface(self.board_dim)
        
        self.rotate(0,0,np.pi/4,0,0,0)
        
        
        
        
        #self.uppdate()
    
    def uppdate(self):
        self.fix()
        self.board.fill(self.back_color)
        pygame.draw.rect(self.board,"white",pygame.Rect(2,2,self.board_dim[0]-4,self.board_dim[1]-4))
        color = "black"
        for i in self.edges:
            color = "black"
            if i[0] == 0:
                if i[1] == 1:
                    color = "red"
                elif i[1] == 2:
                    color = "green"
                elif i[1] == 3:
                    color = "blue"
            
            pygame.draw.line(self.board, color,
                             (int(self.mid[0]+self.scale*self.points[i[0]][0]),int(self.mid[1]+self.scale*self.points[i[0]][1])),
                             (int(self.mid[0]+self.scale*self.points[i[1]][0]),int(self.mid[1]+self.scale*self.points[i[1]][1])),width=2)
        
    def fix(self):
        temp = []
        temp2 = []
        
        for i in self.points:
            temp.append(i-self.camera)

        for i in temp:
            a = (np.arctan([i[0][0]/i[1][0],-i[2][0]/i[1][0]]))
            temp2.append([a[0]*self.paint,a[1]*self.paint])
            
        self.points = temp2
        
    
     
    def rot_tail(self,x,y,z):
        
        rotx = x
        rotz = z
        roty = y
        
        Rx = np.array([[1],[0],[0],
                   [0],[np.cos(rotx)],[-np.sin(rotx)],
                   [0],[np.sin(rotx)],[np.cos(rotx)]]).reshape(3,3)
        
        Ry =np.array([[np.cos(roty)],[0],[np.sin(roty)],
                      [0],[1],[0],
                      [-np.sin(roty)],[0],[np.cos(roty)]]).reshape(3,3)
        
        Rz = np.array([[np.cos(rotz)],[-np.sin(rotz)],[0],
                       [np.sin(rotz)],[np.cos(rotz)],[0],
                       [0],[0],[1]]).reshape(3,3)
        
        
        full_rot = np.dot(np.dot(Rz,Ry),Rx)
        offset = len(self.points_origin)-len(self.truster_points_origin)
        
        for i in range(len(self.truster_points_origin)):
            self.points_origin[i+offset] = np.dot(full_rot,self.truster_points_origin[i])
            self.points_origin[i+offset][0][0] -= 15
            
        #self.uppdate()
        
    def rotate(self,x,y,z,tx,ty,tz):
        self.rot_tail(tx,ty,tz)
        rotx = x
        rotz = z
        roty = y
        
        Rx = np.array([[1],[0],[0],
                   [0],[np.cos(rotx)],[-np.sin(rotx)],
                   [0],[np.sin(rotx)],[np.cos(rotx)]]).reshape(3,3)
        
        Ry =np.array([[np.cos(roty)],[0],[np.sin(roty)],
                      [0],[1],[0],
                      [-np.sin(roty)],[0],[np.cos(roty)]]).reshape(3,3)
        
        Rz = np.array([[np.cos(rotz)],[-np.sin(rotz)],[0],
                       [np.sin(rotz)],[np.cos(rotz)],[0],
                       [0],[0],[1]]).reshape(3,3)
        
        
        full_rot = np.dot(np.dot(Rz,Ry),Rx)
        
        for i in range(len(self.points_origin)):
            self.points[i] = np.dot(full_rot,self.points_origin[i])
        self.uppdate()
    def simulate(self,fps):
        self.fps = fps
        self.roll = self.df["roll"].tolist()
        self.pitch = self.df["pitch"].tolist()
        self.yaw = self.df["heading"].tolist()
        self.time = []
        self.timer = -60
        
        for i in range((len(self.roll)-1)*fps):
            self.time.append(i)
        self.roll_sim = []
        self.pitch_sim = []
        self.yaw_sim = []
        for i in range(1,len(self.roll)):
            temp1 = self.roll[i-1]
            temp2 = self.roll[i]
            dif = (temp2-temp1)/fps
            for p in range(fps):
                self.roll_sim.append(temp1+dif*p)
                
        for i in range(1,len(self.pitch)):
            temp1 = self.pitch[i-1]
            temp2 = self.pitch[i]
            dif = (temp2-temp1)/fps
            for p in range(fps):
                self.pitch_sim.append(temp1+dif*p)
                
        for i in range(1,len(self.yaw)):
            temp1 = self.yaw[i-1]
            temp2 = self.yaw[i]
            dif = (temp2-temp1)/fps
            for p in range(fps):
                self.yaw_sim.append(temp1+dif*p)
                
            
                
        self.end = len(self.time)

                
        
            
    
            