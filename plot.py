import pygame, sys
import glob, os
import peder
import time
import pygame_chart as pyc
import pandas as pd
import tkinter
from tkinter import filedialog
# variables
save_file = peder.save_file()
running = True
pltScreen = [[800,360],[360,360]]
display = (1224,800)
text = [((30,400),(255,0,0),"Pitch: "),((130,400),(255,255,0),"Roll: "),((230,400),(0,0,255),"Heading: ")]
counter = 0
logfil = save_file.save[0][1]

filer = []
fps = 24
offset = 10


# setup
os.chdir(logfil)
pygame.init()
screen = pygame.display.set_mode(display)
clock = pygame.time.Clock()
pygame.display.set_caption("AUV plot") 
while True:#find last log file
    
    for file in glob.glob("*.csv"):
        filer.append(file)
    if len(filer) >= 1:
        break
    else:
        print(filer)
        time.sleep(1)

logfil = logfil+"/"+filer[-1]


font = pygame.font.Font('freesansbold.ttf', 12)
meny = peder.plot(logfil,pltScreen,offset)
menue = peder.menue("menue",save_file.save[0][1])


counter = 0
ping = 0
settings = peder.settings()


while running: # start of main code
    # poll for events (userinputs)
    start = time.time()#time execution time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menue.location = "menue"
                menue.file_select = 0
                counter = 0
    
    if menue.location == "menue": #start menue
        screen.fill("white")
        menue.get_pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
        
        screen.blit(menue.option1[0],menue.option1[1])
        screen.blit(menue.option2[0],menue.option2[1])
        screen.blit(menue.option3[0],menue.option3[1])
        if menue.file_select == 1:
            pygame.draw.line(screen, (0,0,0),(250,0),(250,600), width=3)
            for i in menue.log_fil:
                screen.blit(i[0],i[1])
        
    elif menue.location == "mission plot":# initialising plotting of missions
        draw = 0
        global mission
        mission = peder.mission_Plot(menue.file_Selected,display)
        
        figure = pyc.Figure(screen, offset+200, offset, 360, 360)
        
        
        
        #figure2 = pyc.Figure(screen, offset+600, offset, 360, 360)
        #figure.line('Chart1', mission.plot_time ,mission.data)
        
        #figure.line('Chart2', [0,1,2] ,[1,1,1])
        #figure2.line('Chart2', [0,1,2] ,[0,1,2])
        
        menue.location = "mission plot start"
        screen.fill("white")
        figure1 = pyc.Figure(screen, offset+200, offset, 360, 360)
        figure2 = pyc.Figure(screen, offset+200+360, offset, 360, 360)
        figure3 = pyc.Figure(screen, offset+200, offset+360, 360, 360)
        plts = [0,0,0]
        
        for i in range(len(mission.option_text)): #plot poitns text
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(25,35+40*i,20,20))
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(26,36+40*i,18,18))
            if mission.plot_points[i][1] == 1:
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(25,35+40*i,20,20))
            screen.blit(mission.option_text[i][0],mission.option_text[i][1])
             
    elif menue.location == "mission plot start": #plot past missions
        save_text = peder.text("save plots",45,display[1]-45,30,"black")
        
        plot = 0# flagg to see if plots change

        
        mission.get_pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])

        if mission.toggle == 2:
            
            for i in range(len(mission.plot_points)):#if any plot poitns are to be drawn draw them
                if mission.plot_points[i][1] == 1:
                    plot = 1
            if plot == 1:#draw plot lines
                
                for i in range(len(mission.plot_points)):
                    if i <=1:#plot pitch,roll
                        if mission.plot_points[i][1] == 1:
                            figure1.line(str(i), mission.plot_time ,mission.data[i])
                            plts[0] = 1
                            
                    if i ==2: #plot heading
                         if mission.plot_points[i][1] == 1:
                             figure2.line(str(i), mission.plot_time ,mission.data[i])
                             plts[1] = 1
                             
                    if i >2:#plot speed
                         if mission.plot_points[i][1] == 1:
                             figure3.line(str(i), mission.plot_time ,mission.data[i])
                             plts[2] = 1

                
            draw = 2
            mission.toggle = 0
                    
        elif mission.toggle == 1:#is plots points clicked
            screen.fill("white")
            figure1 = pyc.Figure(screen, offset+300, offset, 360, 360)
            figure2 = pyc.Figure(screen, offset+300+360, offset, 360, 360)
            figure3 = pyc.Figure(screen, offset+300, offset+360, 360, 360)
            figure1.set_ylim((settings.roll_pitch[1][0],settings.roll_pitch[1][1]))
            figure2.set_ylim((0,360))
            figure3.set_ylim((-10,10))
            plts = [0,0,0]
            for i in range(len(mission.option_text)): #plot poitns text
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(25,35+40*i,20,20))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(26,36+40*i,18,18))
                if mission.plot_points[i][1] == 1:
                    pygame.draw.rect(screen, (0,255,0), pygame.Rect(25,35+40*i,20,20))
                screen.blit(mission.option_text[i][0],mission.option_text[i][1])
            mission.toggle = 2
        
        if draw > 0:
            if plts[0] == 1:
                figure1.draw()
            if plts[1] == 1:
                figure2.draw()
            if plts[2] == 1:
                figure3.draw()
            draw -= 1 
  
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(0,display[1]-100,300,100))
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(19,display[1]-41,22,22))
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(20,display[1]-40,20,20))
        screen.blit(save_text[0],save_text[1])
        
        if mission.save == 1:
            ok = 0
            pygame.draw.rect(screen,(0,255,0),pygame.Rect(20,display[1]-40,20,20))
            
            if pygame.mouse.get_pressed()[0]:
                tkinter.Tk().withdraw()
                location = filedialog.askdirectory()
                plot_save1 = pygame.Surface((400,400))
                plot_save2 = pygame.Surface((400,400))
                plot_save3 = pygame.Surface((400,400))
                
                plot_fig1 = pyc.Figure(plot_save1, 0, 40, 360, 360)
                plot_fig2 = pyc.Figure(plot_save2, 0, 40, 360, 360)
                plot_fig3 = pyc.Figure(plot_save3, 0, 40, 360, 360)
                
                plot_fig1.set_ylim((-180,180))
                plot_fig2.set_ylim((0,360))
                plot_fig3.set_ylim((-10,10))
                
                for i in range(len(mission.plot_points)):#if any plot poitns are to be drawn draw them
                    if mission.plot_points[i][1] == 1:
                        plot = 1
                        
                if plot == 1:#draw plot lines
                    
                    for i in range(len(mission.plot_points)):
                        if i <=1:#plot pitch,roll
                            if mission.plot_points[i][1] == 1:
                                plot_fig1.line(str(i), mission.plot_time ,mission.data[i])
                                
                        if i ==2: #plot heading
                             if mission.plot_points[i][1] == 1:
                                 plot_fig2.line(str(i), mission.plot_time ,mission.data[i])
                                 
                        if i >2:#plot speed
                             if mission.plot_points[i][1] == 1:
                                 plot_fig3.line(str(i), mission.plot_time ,mission.data[i])
                
                if plts[0] == 1:

                    plot_save1.fill("white")
                    plot_fig1.draw()
                    plot_fig1.draw()
                    pygame.image.save(plot_save1,location+"/"+"test1.png")
                    
                if plts[1] == 1:

                    plot_save2.fill("white")
                    plot_fig2.draw()
                    plot_fig2.draw()
                    pygame.image.save(plot_save2,location+"/"+"test2.png")
                    
                if plts[2] == 1:

                    plot_save3.fill("white")
                    plot_fig3.draw()
                    plot_fig3.draw()
                    pygame.image.save(plot_save3,location+"/"+"test3.png")
                    
                
                

            mission.save = 0
                
    elif menue.location == "live plot":
        
        if counter >= fps:
            meny.get_lastline()
            meny.add_plt()
            counter = 0
        else:
            counter += 1
        screen.fill("black")
        
        for i in meny.plts:
            pygame.draw.rect(screen, i[1], pygame.Rect(i[0]))
            
        for i in meny.plt1_lines:
            pygame.draw.line(screen, (255,255,255), (meny.pltScreenStart[0][0]+i,meny.pltScreenStart[0][1]), (meny.pltScreenStart[0][0]+i, meny.pltScreenStart[0][1]+meny.pltScreen[0][1]), width=1)
        for i in meny.plt2_lines:
            pygame.draw.line(screen, (255,255,255), (meny.pltScreenStart[1][0], meny.pltScreenStart[1][1]+i), (meny.pltScreenStart[1][0]+meny.pltScreen[1][0], meny.pltScreenStart[1][1]+i), width=1)
            
        for i in range(len(meny.pltR)-1):
            pygame.draw.line(screen, (255,0,0), (meny.pltScreenStart[0][0]+meny.pltR[i][0], meny.pltScreenStart[0][1]+180+meny.pltR[i][1]), (meny.pltScreenStart[0][0]+meny.pltR[i+1][0], meny.pltScreenStart[0][1]+180+meny.pltR[i+1][1]), width=1)
        for i in range(len(meny.pltP)-1):
            pygame.draw.line(screen, (0,255,0), (meny.pltScreenStart[0][0]+meny.pltP[i][0], meny.pltScreenStart[0][1]+180+meny.pltP[i][1]), (meny.pltScreenStart[0][0]+meny.pltP[i+1][0], meny.pltScreenStart[0][1]+180+meny.pltP[i+1][1]), width=1)
        for i in range(len(meny.pltH)-1):
            pygame.draw.line(screen, (0,0,255), (meny.pltScreenStart[1][0]+meny.pltH[i][0], meny.pltScreenStart[1][1]+meny.pltH[i][1]), (meny.pltScreenStart[1][0]+meny.pltH[i+1][0], meny.pltScreenStart[1][1]+meny.pltH[i+1][1]), width=1)
        
        meny.move_plot()
    
    elif menue.location == "settings":
        screen.fill("white")
    
    pygame.display.flip()
    end = time.time()
    ping = int((end-start)/(1/fps)*100)/100
    clock.tick(fps)  # limits FPS
    
    
save_file.write_save()
pygame.quit()
sys.exit()