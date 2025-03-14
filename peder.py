import pygame
import pygame_chart as pyc
import tkinter
from tkinter import filedialog
import glob, os
import pandas as pd
import time
import numpy as np
from numpy.linalg import inv


def text(skrift,x,y,z,color):
    font2 = pygame.font.Font('freesansbold.ttf', z)
    text = font2.render(skrift, True, color)
    textRect = text.get_rect()
    textRect.center = (x+textRect[2]/2, y+textRect[3]/2)
    ret = (text,textRect)
    return ret

class plot:
    def __init__(self,logfil,pltScreen,offset):
        self.logfil = logfil
        self.pltScreen = pltScreen
        self.pltScreenStart = [[offset,offset],[offset*2+self.pltScreen[0][0],offset]]
        self.pltR = [[self.pltScreen[0][0]+10,0]]
        self.pltP = [[self.pltScreen[0][0]+10,0]]
        self.pltH = [[180,10]]
        
        self.get_lastline()
        self.plt_lines()
        self.draw_plt_screen()

    def add_plt(self):
        self.pltR.append([int(self.pltScreen[0][0]),self.data[0][0]])
        self.pltP.append([int(self.pltScreen[0][0]),self.data[1][0]])
        self.pltH.append([self.data[2][0],0])

    def move_plot(self):
        if self.pltR[0][0] <= 0:
            self.pltR.pop(0)
        if self.pltP[0][0] <= 0:
            self.pltP.pop(0)
        if self.pltH[0][1] >= self.pltScreen[1][1]:
            self.pltH.pop(0)

        for i in self.pltR:
            i[0] -= 1
        for i in self.pltP:
            i[0] -= 1
        for i in self.pltH:
            i[1] += 1
            
        for i in range(len(self.plt1_lines)):
            if self.plt1_lines[i] <= 0:
                self.plt1_lines[i] = self.pltScreen[0][0]
            else:
                self.plt1_lines[i] -= 1
                
        for i in range(len(self.plt2_lines)):
            if self.plt2_lines[i] >= self.pltScreen[1][1]:
                self.plt2_lines[i] = 0
            else:
                self.plt2_lines[i] += 1

    def draw_plt_screen(self):
        self.plts = []
        self.plts.append(((self.pltScreenStart[0][0]-1, self.pltScreenStart[0][1]-1, self.pltScreen[0][0]+2,self.pltScreen[0][1]+2),(255, 0,0)))
        self.plts.append(((self.pltScreenStart[0][0], self.pltScreenStart[0][1], self.pltScreen[0][0],self.pltScreen[0][1]),(0, 0,50)))
        
        self.plts.append(((self.pltScreenStart[1][0]-1, self.pltScreenStart[1][1]-1, self.pltScreen[1][0]+2,self.pltScreen[1][1]+2),(255, 0,0)))
        self.plts.append(((self.pltScreenStart[1][0], self.pltScreenStart[1][1], self.pltScreen[1][0],self.pltScreen[1][1]),(0, 0,50)))
            
    def get_lastline(self): #gets last line of .csv file and extracts wanted data
        with open(self.logfil) as f:
            self.last_line = f.readlines()[-1].split(",")
        self.data = [[int(float(self.last_line[1]))],[int(float(self.last_line[2]))],[int(float(self.last_line[3]))]]
        self.x = self.data[0][0]*(np.pi/180)
        self.y = self.data[1][0]*(np.pi/180)
        self.z = (self.data[2][0]-90)*(np.pi/180)
    
    def plt_lines(self):
        d = int(self.pltScreen[0][0]/10)
        dC = int(self.pltScreen[1][1]/5)
        self.plt1_lines = [d*1,d*2,d*3,d*4,d*5,d*6,d*7,d*8,d*9,d*10]
        self.plt2_lines = [dC*1,dC*2,dC*3,dC*4,dC*5]
  
class menue:
    def __init__(self,location,folder):
        print("menue init:",end=" ")
        self.folder_path = folder
        self.location = location
        self.file_select = 0
        self.choice = 0
        self.options = []
        self.option_text = ["Live plot","Mission data","Settings","Test","controller"]
        
        for i in range(len(self.option_text)):
            self.options.append([0,text(self.option_text[i],10,50+50*i,30,"black"),text(self.option_text[i],9,49+50*i,32,"green"),i+1])
            
        self.select = 0
        self.got = 0
        self.file_Selected = ""
        print("done")
        print()
        
    def mtext(self,skrift,x,y,z,color):
        font2 = pygame.font.Font('freesansbold.ttf', z)
        text = font2.render(skrift, True, color)
        textRect = text.get_rect()
        textRect.center = (x+textRect[2]/2, y+textRect[3]/2)
        ret = (text,textRect)
        return ret
    
    
    def get_pos(self,pos,click):
        for i in self.options:
            i[0] = 0
            if i[1][1][0] <= pos[0] <= i[1][1][0]+i[1][1][2] and i[1][1][1] <= pos[1] <= i[1][1][1]+i[1][1][3]:
                i[0] = 1
                if click == True:
                    self.choice = i[3]
                    
        if self.choice == 1:
            self.location = "live plot"
        elif self.choice == 2:
            self.got = 0
            self.get_files()
            self.file_select = 1
        elif self.choice == 3:
            self.location = "settings"
        elif self.choice == 4:
            self.location = "test"
        elif self.choice == 5:
            self.location = "controller"
        self.choice = 0
            
        if self.file_select == 1:
            for i in range(len(self.log_fil)):
                if self.log_fil[i][1][0] <= pos[0] <= self.log_fil[i][1][0]+self.log_fil[i][1][2] and self.log_fil[i][1][1] <= pos[1] <= self.log_fil[i][1][1]+self.log_fil[i][1][3]:
                    self.select = i+1
                    if click == True:
                        self.location = "mission plot"
                        self.file_Selected = self.folder_path+"/"+self.filer[i]
                        
            self.get_files() 
    
    def get_pos_2(self,pos,click):
        pass
    
    def get_files(self):
        self.filer = []
        self.log_fil = []
        
        if self.got == 0:
            os.chdir(self.folder_path)
            self.got = 1
        
        for file in glob.glob("*.csv"):
            self.filer.append(file)
        for i in range(len(self.filer)):
            if i+1 == self.select:
                self.log_fil.append(self.mtext(str(self.filer[i]),260,50+50*i,30,"green"))
            else:
                self.log_fil.append(self.mtext(str(self.filer[i]),260,50+50*i,30,"black"))
        self.select = 0
        
class mission_Plot:
    def __init__(self,file,display,state):
        self.file = file
        self.options = [0,0,0]
        self.df = pd.read_csv(self.file,sep="," )
        self.delay = 0
        self.flight_time = self.df["flightTime"].tolist()
        self.missions = []
        self.break_points = [0]
        self.mission_select = []
        self.mission_selected = 1
        self.detect_arm()
        self.toggle = 0
        
        if state == 0:
            self.plot_points = [["roll",-1],["pitch",-1],["heading",-1],["groundSpeed",-1]]
        else:
            self.plot_points = state
            self.toggle = 1
        
        self.display = display
        self.save = 0
        self.plot()
        self.menue()
        
    def detect_arm(self):
        for i in range(2+self.break_points[self.mission_selected-1],len(self.flight_time)):
            if self.flight_time[i] == self.flight_time[i-1]:
                self.time = i
                break
            
    def plot(self):
        self.plot_time = []
        self.data = []
        for i in range(self.time-self.break_points[self.mission_selected-1]):
            self.plot_time.append(i)
        for i in range(len(self.plot_points)):
            data = self.df[self.plot_points[i][0]].tolist()
            temp = []
            for i in range(self.break_points[self.mission_selected-1],self.time):
                temp.append(data[i])
            self.data.append(temp)
            
    def mtext(self,skrift,x,y,z,color):
        font2 = pygame.font.Font('freesansbold.ttf', z)
        text = font2.render(skrift, True, color)
        textRect = text.get_rect()
        textRect.center = (x+textRect[2]/2, y+textRect[3]/2)
        ret = (text,textRect)
        return ret
        
    def menue(self):
        self.option_text = []
        for i in range(len(self.plot_points)):
            self.option_text.append(self.mtext(self.plot_points[i][0],50,30+40*i,30,"black"))
            
    def get_pos(self,pos,click):#26,36+40*i,18,18
        if self.delay <= 0:
            for i in range(len(self.plot_points)):
                if 25 <= pos[0] <= 25+20 and 35+40*i <= pos[1] <= 35+40*i+20 :
                    if click == True:
                        self.toggle = 1
                        self.plot_points[i][1] *= -1 
                        self.delay = 5
        else:
            self.delay -= 1
        if 19 <= pos[0] <= 19+22 and self.display[1]-41 <= pos[1] <= self.display[1]-41+22 :
            self.save = 1
        if 19 <= pos[0] <= 19+22 and self.display[1]-81 <= pos[1] <= self.display[1]-81+22 :
            self.save = 2
            
        for i in range(len(self.mission_select)):
            if 490+30*i <= pos[0] <= 520+30*i and self.display[1]-45 <= pos[1] <= self.display[1]-15 :
                self.mission_select[i] = 1
                if click == True:
                    self.mission_selected = i+1
                    self.toggle = 1
                    self.detect_arm()
                    self.plot()
            else:
                self.mission_select[i] = 0
    
    def get_arming(self):
        self.break_points = [0]
        for i in range(1,len(self.flight_time)):
            if self.flight_time[i] < self.flight_time[i-1] :
                self.break_points.append(i)
        return self.break_points

class save_file:
    def __init__(self):
        print("save file init:",end=" ")
        self.save_exist = 0
        self.path = str(__file__[:-8])+"savefile.txt"
        f = open(self.path, "a")
        f.close()
        f = open(self.path, "r")
        self.save_read = f.read()
        
        f.close()
        f.close()
        self.read_savefile()
        print("done")
        print()
    def read_savefile(self):
        self.save = []
        temp = []
        counter = 0
        save_exist = 0
        if self.save_read == "":
            tkinter.Tk().withdraw()
            self.folder_path = filedialog.askdirectory()
            time.sleep(1)
            self.save.append([1,self.folder_path])
            
        for i in range(len(self.save_read)):
            if self.save_read[i] == ",":
                temp.append(self.save_read[counter:i])
                counter = i+1
                save_exist = 1
            elif self.save_read[i] == ";":
                temp.append(self.save_read[counter:i])
                save_exist = 1
        if save_exist == 1:
            self.save_exist = 1
            if int(temp[0]) == 1:
                self.save.append([1,temp[1]])
        
    def write_save(self):
        f = open(self.path, "w")
        for i in range(len(self.save)):
            f.write(str(self.save[i][0]))
            f.write(",")
            f.write(self.save[i][1])
            f.write(";")
        f.close()
        f.close()
        
class settings:
    def __init__(self,display):
        self.display = display
        print("settings init:",end=" ")
        self.roll_pitch = None
        self.heading = None
        self.speed  = None
        self.boxes = [[250,35],[280,35]]
        self.upp = [0,0]
        self.delay = 0
        self.hold = 0
        
        
        
        self.path = str(__file__[:-8])+"/settings.txt"
        f = open(self.path, "a")
        f.close()
        f = open(self.path, "r")
        self.save_settings = f.read()
        f.close()
        f.close()
        self.read_settings()
        print("done")
        print()
    def read_settings(self):
        a = 0
        temp = []
        ttemp = []
        temp_data = []
        temp_data_start = 0
        for i in range(len(self.save_settings)):
            if self.save_settings[i] == ":":
                ttemp.append(self.save_settings[a:i])
                a = i+1
                
            elif self.save_settings[i] == "[":
                temp_data_start = i+1
                
            elif self.save_settings[i] == ",":
                temp_data.append(int(self.save_settings[temp_data_start:i]))
                temp_data_start = i+1
                
            elif self.save_settings[i] == "]":
                temp_data.append(int(self.save_settings[temp_data_start:i]))
                ttemp.append(temp_data)
                temp_data = []
            elif self.save_settings[i] == ";":
                temp.append(ttemp)
                ttemp = []
                a = i+1
                
        self.roll_pitch = [temp[0][0],temp[0][1]]
        self.heading = [temp[1][0],temp[1][1]]
        self.speed = [temp[2][0],temp[2][1]]
        
    def first_start(self):
        self.roll_pitch = ["roll_pitch",[-180,180]]
        self.heading = ["heading",[0,360]]
        self.speed = ["speed",[-10,10]]
        self.camera = ["camera",[-1,40]]
        
    def save_to_file(self):
        f = open(self.path,"w")
        temp = [self.roll_pitch,self.heading,self.speed]

        for i in temp:
            f.write(str(i[0]))
            f.write(":")
            f.write(str(i[1]))
            f.write(";")
    

        
        f.close()
        f.close()
    
    def menue(self):
        self.option_text = []
        self.config = [self.roll_pitch,self.heading,self.speed]
        for i in range(len(self.config)):
            self.option_text.append(text(self.config[i][0],50,30+40*i,30,"black"))    
    
    def pos(self,pos,click):
        if self.delay <= 0:
            if click == False:
                self.hold = 0
            for i in range(3):
                if self.boxes[0][0]<pos[0]<self.boxes[0][0]+20 and self.boxes[0][1]+i*40<pos[1]<self.boxes[0][1]+20+i*40:
                    if click == True:
                        self.delay = 4
                        self.upp = [i,1]
                        self.uppdate()
                        break
                        
                elif self.boxes[1][0]<pos[0]<self.boxes[1][0]+20 and self.boxes[1][1]+i*40<pos[1]<self.boxes[1][1]+20+i*40:
                    if click == True:
                        self.delay = 4
                        self.upp = [i,-1]
                        self.uppdate()
                        break
                
        else:

            self.delay -=1
            if click == True:
                self.hold += 1
                
        if 20 <pos[0]<40 and self.display[1]-40< pos[1] <self.display[1]-20:
            self.save = 1
            if click == True:
                self.save_to_file()
                time.sleep(1)
        else: 
            self.save = 0
    
    def uppdate(self): 
        if self.upp[0] == 0:
            self.roll_pitch[1][0] -= self.upp[1]
            self.roll_pitch[1][1] += self.upp[1]
                
        elif self.upp[0] == 1:
            self.heading[1][0] -= self.upp[1]
            self.heading[1][1] += self.upp[1]
                
        elif self.upp[0] == 2:
            self.speed[1][0] -= self.upp[1]
            self.speed[1][1] += self.upp[1]
        

        
        if self.hold >=4:
            self.delay = 0
            
class sprites:
    def __init__(self):
        self.plus = pygame.Surface((20,20))
        self.minus = pygame.Surface((20,20))
        self.draw()
        
    def draw(self):
        self.plus.fill("black")
        pygame.draw.rect(self.plus, (0,255,0), pygame.Rect(1,1,18,18))
        pygame.draw.rect(self.plus, (0,0,0), pygame.Rect(9,2,2,16))
        pygame.draw.rect(self.plus, (0,0,0), pygame.Rect(2,9,16,2))
        
        self.minus.fill("black")
        pygame.draw.rect(self.minus, (255,0,0), pygame.Rect(1,1,18,18))
        pygame.draw.rect(self.minus, (0,0,0), pygame.Rect(2,9,16,2))
        
class plot_surface:
    def __init__(self,sx,sy,name):
        self.name = name
        self.surface = pygame.Surface((sx,sy))
        self.surface.fill("white")
        self.plot_fig = pyc.Figure(self.surface, 0, 0, 360, 360)
        self.plot_fig.add_title(self.name)
    
    def limit(self,minus,plus):
        self.minus = minus
        self.plus = plus
        self.plot_fig.set_ylim((self.minus,self.plus))
    
    def uppdate(self):
        self.plot_fig.set_ylim((self.minus,self.plus))
        self.plot_fig.add_title(self.name)
        self.plot_fig.add_legend()
        self.plot_fig.draw()
        
    def clear(self):
        self.plot_fig = pyc.Figure(self.surface, 0, 0, 360, 360)
        
class cube:
    def __init__(self,wire_color,back_color):
        self.back_color = back_color
        self.wire_color = wire_color
        self.distance = 40
        self.paint_distance = 1
        self.camera = np.array([0,-self.distance,-4]).reshape(3,1)
        self.paint = self.distance-self.paint_distance
        # u = up, d = down, n = north, s = south, w = west, e = east
        self.rot = 0.523599
        self.Rx = np.array([[1],[0],[0],
                   [0],[np.cos(self.rot)],[-np.sin(self.rot)],
                   [0],[np.sin(self.rot)],[np.cos(self.rot)]]).reshape(3,3)
        self.Ry =np.array([[np.cos(self.rot)],[0],[np.sin(self.rot)],
                           [0],[1],[0],
                           [-np.sin(self.rot)],[0],[np.cos(self.rot)]]).reshape(3,3)
        
        self.origo = np.array([0,0,0]).reshape(3,1) #middle of shape
        self.unw = np.array([-4,1,1]).reshape(3,1)
        self.une = np.array([4,1,1]).reshape(3,1)
        self.usw = np.array([-4,-1,1]).reshape(3,1)
        self.use = np.array([4,-1,1]).reshape(3,1)
        self.dnw = np.array([-4,1,-1]).reshape(3,1)
        self.dne = np.array([4,1,-1]).reshape(3,1)
        self.dsw = np.array([-4,-1,-1]).reshape(3,1)
        self.dse = np.array([4,-1,-1]).reshape(3,1)
        self.front = np.array([6,0,0]).reshape(3,1)
        
        self.x = np.array([1,0,0]).reshape(3,1)
        self.y = np.array([0,1,0]).reshape(3,1)
        self.z = np.array([0,0,-1]).reshape(3,1)
        self.points_origin = [self.unw, self.une, self.usw, self.use, self.dnw, self.dne, self.dsw, self.dse,self.front,self.origo,self.x,self.y,self.z]
        self.points = [self.unw, self.une, self.usw, self.use, self.dnw, self.dne, self.dsw, self.dse,self.front,self.origo,self.x,self.y,self.z]
        self.edges = [[0,1],[1,3],[3,2],[2,0],
                      [0,4],[1,5],[2,6],[3,7],
                      [4,5],[5,7],[7,6],[6,4],
                      [1,8],[3,8],[5,8],[7,8],
                      [9,10],[9,11],[9,12]]
        self.board_dim = (600,400)
        self.scale = 40
        self.mid = (self.board_dim[0]/2,self.board_dim[1]/2)
        self.board = pygame.Surface(self.board_dim)
        self.uppdate()
        
    def rotate_y(self):
        
        rot = 0.1
        Ry = np.array([[1],[0],[0],
                   [0],[np.cos(rot)],[-np.sin(rot)],
                   [0],[np.sin(rot)],[np.cos(rot)]]).reshape(3,3)
        for i in range(len(self.points)):
            self.points[i] = np.dot(Ry, self.points[i])
        self.uppdate()
    
    def rotate_x(self):
        rot = 0.04
        Rx =np.array([[np.cos(rot)],[0],[np.sin(rot)],
                           [0],[1],[0],
                           [-np.sin(rot)],[0],[np.cos(rot)]]).reshape(3,3)
        for i in range(len(self.points)):
            self.points[i] = np.dot(Rx, self.points[i])
        self.uppdate()
    
    def rotate(self,x,y,z):
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
        
        
        full_rot = np.dot(np.dot(Rx,Ry),Rz)
        
        for i in range(len(self.points)):
            self.points[i] = np.dot(full_rot,self.points_origin[i])
        self.uppdate()
        
    def uppdate(self):
        self.fix()
        self.board.fill(self.back_color)
        color = self.wire_color
        for i in self.edges:
            if i[1] == 10:
                color = (255,0,0)
            elif i[1] == 11:
                color = (0,255,0)
            elif i[1] == 12:
                color = (0,0,255)
            else:
                color = self.wire_color
            
            # pygame.draw.line(self.board, (0,0,0),
            #                  (int(self.mid[0]+self.scale*self.points[i[0]][0][0]),int(self.mid[1]+self.scale*self.points[i[0]][2][0])),
            #                  (int(self.mid[0]+self.scale*self.points[i[1]][0][0]),int(self.mid[1]+self.scale*self.points[i[1]][2][0])),width=2)
            
            pygame.draw.line(self.board, color,
                             (int(self.mid[0]+self.scale*self.points[i[0]][0]),int(self.mid[1]+self.scale*self.points[i[0]][1]-180)),
                             (int(self.mid[0]+self.scale*self.points[i[1]][0]),int(self.mid[1]+self.scale*self.points[i[1]][1]-180)),width=2)
            
            
    def fix(self):
        temp = []
        temp2 = []
        for i in self.points:
            temp.append(i-self.camera)

        for i in temp:
            a = (np.arctan([i[0][0]/i[1][0],i[2][0]/i[1][0]]))
            temp2.append([a[0]*self.paint,a[1]*self.paint])
            
        self.points = temp2
