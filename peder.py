import pygame
import tkinter
from tkinter import filedialog
import glob, os
import pandas as pd
import time

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
    
    def plt_lines(self):
        d = int(self.pltScreen[0][0]/10)
        dC = int(self.pltScreen[1][1]/5)
        self.plt1_lines = [d*1,d*2,d*3,d*4,d*5,d*6,d*7,d*8,d*9,d*10]
        self.plt2_lines = [dC*1,dC*2,dC*3,dC*4,dC*5]
  
class menue:
    def __init__(self,location,folder):
        self.folder_path = folder
        self.location = location
        self.file_select = 0

        
        self.option1 = self.mtext("Live plot",10,50,30,"black")
        self.option2 = self.mtext("Mission plot",10,100,30,"black")
        self.select = 0
        self.got = 0
        self.file_Selected = ""
        
    def mtext(self,skrift,x,y,z,color):
        font2 = pygame.font.Font('freesansbold.ttf', z)
        text = font2.render(skrift, True, color)
        textRect = text.get_rect()
        textRect.center = (x+textRect[2]/2, y+textRect[3]/2)
        ret = (text,textRect)
        return ret
    
    
    def get_pos(self,pos,click):
        
        self.option1 = self.mtext("Live plot",20,50,30,"black")
        self.option2 = self.mtext("Mission data",20,100,30,"black")
        
        if self.option1[1][0] <= pos[0] <= self.option1[1][0]+self.option1[1][2] and self.option1[1][1] <= pos[1] <= self.option1[1][1]+self.option1[1][3]:
            self.option1 = self.mtext("Live plot",20,50,30,"green")
            if click == True:
                self.location = "live plot"
        elif self.option2[1][0] <= pos[0] <= self.option2[1][0]+self.option2[1][2] and self.option2[1][1] <= pos[1] <= self.option2[1][1]+self.option2[1][3]:
            
            self.option2 = self.mtext("Mission data",20,100,30,"green")
            if click == True:
                self.got = 0
                self.get_files()
                self.file_select = 1
                
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
    def __init__(self,file,display):
        self.file = file
        self.options = [0,0,0]
        self.df = pd.read_csv(self.file,sep="," )
        self.delay = 0
        self.flight_time = self.df["flightTime"].tolist()
        self.missions = []
        self.detect_arm()
        self.plot_points = [["roll",-1],["pitch",-1],["heading",-1],["groundSpeed",-1]]
        self.toggle = 0
        self.display = display
        self.save = 0
        self.plot()
        self.menue()
        
    def detect_arm(self):
        for i in range(2,len(self.flight_time)):
            if self.flight_time[i] == self.flight_time[i-1]:
                self.time = i
                break
    def plot(self):
        self.plot_time = []
        self.data = []
        for i in range(self.time):
            self.plot_time.append(i)
        for i in range(len(self.plot_points)):
            data = self.df[self.plot_points[i][0]].tolist()
            temp = []
            for i in range(self.time):
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

class save_file:
    def __init__(self): 
        self.save_exist = 0
        self.path = str(__file__[:-8])+"savefile.txt"
        f = open(self.path, "a")
        f.close()
        f = open(self.path, "r")
        self.save_read = f.read()
        f.close()
        f.close()
        self.read_savefile()
        
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
        print("done")

            
            