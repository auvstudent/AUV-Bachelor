import pygame, sys
import glob, os
import peder
import time
import pygame_chart as pyc
import pandas as pd
# variables
running = True
pltScreen = [[800,360],[360,360]]

text = [((30,400),(255,0,0),"Pitch: "),((130,400),(255,255,0),"Roll: "),((230,400),(0,0,255),"Heading: ")]
counter = 0
logfil = "C:/Users/Peder/Documents/QGroundControl/Telemetry"

filer = []
fps = 24
offset = 10


# setup
os.chdir(logfil)
pygame.init()
screen = pygame.display.set_mode((1224, 600))
clock = pygame.time.Clock()
while True:
    
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
menue = peder.menue("menue")

counter = 0
#draw plots


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menue.location = "menue"
                menue.file_select = 0
    
    if menue.location == "menue":
        screen.fill("white")
        menue.get_pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
        
        screen.blit(menue.option1[0],menue.option1[1])
        screen.blit(menue.option2[0],menue.option2[1])
        if menue.file_select == 1:
            pygame.draw.line(screen, (0,0,0),(250,0),(250,600), width=3)
            for i in menue.log_fil:
                screen.blit(i[0],i[1])
        
        
    
        
    elif menue.location == "mission plot":
        global mission
        mission = peder.mission_Plot(menue.file_Selected)
        
        figure = pyc.Figure(screen, offset+200, offset, 360, 360)
        
        
        
        #figure2 = pyc.Figure(screen, offset+600, offset, 360, 360)
        #figure.line('Chart1', mission.plot_time ,mission.data)
        
        #figure.line('Chart2', [0,1,2] ,[1,1,1])
        #figure2.line('Chart2', [0,1,2] ,[0,1,2])
        
        menue.location = "mission plot start"
        
    elif menue.location == "mission plot start":
        plot = 0
        screen.fill("white")
        mission.get_pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
        if mission.toggle == 1:
            figure = pyc.Figure(screen, offset+200, offset, 360, 360)
            mission.toggle = 0
        
        
        
        for i in range(len(mission.option_text)):
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(35,33+30*i,12,12))
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(36,34+30*i,10,10))
            if mission.plot_points[i][1] == 1:
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(35,33+30*i,12,12))
            screen.blit(mission.option_text[i][0],mission.option_text[i][1])
            
        for i in range(len(mission.plot_points)):
            if mission.plot_points[i][1] == 1:
                plot = 1
        if plot == 1:
            
            for i in range(len(mission.plot_points)):
                if mission.plot_points[i][1] == 1:

                    figure.line(str(i), mission.plot_time ,mission.data[i])
            
            figure.draw()

            
            
            
        
        #figure2.draw()
        
    elif menue.location == "live plot":
        
        if counter >= fps:
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
    pygame.display.flip()
    
    clock.tick(fps)  # limits FPS

pygame.quit()
sys.exit()