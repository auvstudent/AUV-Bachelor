import pygame
class plot():
    def __init__(self,logfil,pltScreen,offset):
        self.options = [["Live plot"],["Plot mission"]]
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
    def __init__(self,location):
        self.location = location
        self.option1 = self.mtext("Live plot",100,50,30,"black")
        self.option2 = self.mtext("Mission plot",120,100,30,"black")
        
    def mtext(self,skrift,x,y,z,color):
        font2 = pygame.font.Font('freesansbold.ttf', z)
        text = font2.render(skrift, True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        ret = (text,textRect,)
        return ret
    def get_pos(self,pos,click):
        self.option1 = self.mtext("Live plot",100,50,30,"black")
        self.option2 = self.mtext("Mission plot",120,100,30,"black")
        if self.option1[1][0] <= pos[0] <= self.option1[1][0]+self.option1[1][2] and self.option1[1][1] <= pos[1] <= self.option1[1][1]+self.option1[1][3]:
            self.option1 = self.mtext("Live plot",100,50,30,"green")
            if click[0] == True:
                self.location = "live plot"
        elif self.option2[1][0] <= pos[0] <= self.option2[1][0]+self.option2[1][2] and self.option2[1][1] <= pos[1] <= self.option2[1][1]+self.option2[1][3]:
            
            self.option2 = self.mtext("Mission plot",120,100,30,"green")
            if click[0] == True:
                self.location = "mission plot"

            
        
        

            
            