import pygame, sys
import glob, os
import peder
import time
import pygame_chart as pyc
import tkinter
from tkinter import filedialog
import random

if True:
    print()
    print("settup starting")
    print()
    save_file = peder.save_file()
    logfil = save_file.save[0][1]
    os.chdir(logfil)
    #variables for initialising
    display = (1224,800)
    filer = []
    pltScreen = [[800,360],[360,360]]
    offset = 10
    while True:#find last log file
        for file in glob.glob("*.csv"):
            filer.append(file)
        if len(filer) >= 1:
            break
        else:
            print("no log file available")
            time.sleep(1)
            
    logfil = logfil+"/"+filer[-1]
    
    #initialising
    
    pygame.init()
    screen = pygame.display.set_mode(display)
    clock = pygame.time.Clock()
    pygame.display.set_caption("AUV plot") 
    meny = peder.plot(logfil,pltScreen,offset)
    menue = peder.menue("menue",save_file.save[0][1])
    settings = peder.settings(display)
    sprites = peder.sprites()
    text_for_settings = peder.text("save settings",45,display[1]-45,30,"black")
    
    #other variables
    running = True
    text = [((30,400),(255,0,0),"Pitch: "),((130,400),(255,255,0),"Roll: "),((230,400),(0,0,255),"Heading: ")]
    counter = 0
    fps = 24
    font = pygame.font.Font('freesansbold.ttf', 12)
    ping = 0
    loc = 0
    global mission
    global plot_state
    plot_state = 0
    
    print("settup complete")
    
def polling():
    global running
    global counter
    global loc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            menue.location = "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if loc !=0:
                    menue.location = loc
                    loc = 0
                else:
                    menue.location = "menue"
                    menue.file_select = 0
                counter = 0
                
while running: # start of main code
    # poll for events (userinputs)
    #time execution time
    polling()
    
    while menue.location == "menue": #start menue
        polling()
        screen.fill("white")
        menue.get_pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
        
        screen.blit(menue.option1[0],menue.option1[1])
        screen.blit(menue.option2[0],menue.option2[1])
        screen.blit(menue.option3[0],menue.option3[1])
        screen.blit(menue.option4[0],menue.option4[1])
        if menue.file_select == 1 or menue.file_select == 2:
            pygame.draw.line(screen, (0,0,0),(250,0),(250,600), width=3)
            for i in menue.log_fil:
                screen.blit(i[0],i[1])
        pygame.display.flip()
        clock.tick(fps)
           
    while menue.location == "mission plot":
        ping=[0,0,0,0,0,0,0,0,0,0]
        screen.fill("white")
        draw = 0
        plts = [0,0,0]
        mission = peder.mission_Plot(menue.file_Selected,display,plot_state)
        plot_state = 0
        arming = peder.text("activations: ",300,display[1]-45,30,"black")
        start_points = mission.get_arming()
        for i in range(len(start_points)):
            mission.mission_select.append(0)
        print(start_points)
        
        
        figure1 = peder.plot_surface(360, 360, "Pitch, Roll")
        figure1.limit(settings.roll_pitch[1][0],settings.roll_pitch[1][1])
        
        figure2 = peder.plot_surface(360, 360, "Heading")
        figure2.limit(settings.heading[1][0],settings.heading[1][1])
        
        figure3 = peder.plot_surface(360, 360, "Speed")
        figure3.limit(settings.speed[1][0],settings.speed[1][1])
        
        for i in range(len(mission.option_text)): #plot poitns text
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(25,35+40*i,20,20))
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(26,36+40*i,18,18))
            if mission.plot_points[i][1] == 1:
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(25,35+40*i,20,20))
            screen.blit(mission.option_text[i][0],mission.option_text[i][1])
            
        while menue.location == "mission plot":
            start = time.time()
            screen.fill("white")
            polling()
            save_text = peder.text("save plots",45,display[1]-45,30,"black")
            settings_text = peder.text("settings",45,display[1]-85,30,"black")
            
            plot = 0# flagg to see if plots change
            
            mission.get_pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
            screen.blit(arming[0],arming[1])
            armings = []
            
            
            for i in range(1,len(start_points)+1):
                if mission.mission_select[i-1] == 1:
                    armings.append(peder.text(str(i), 460+30*i, display[1]-45, 30, "green"))
                else:
                    armings.append(peder.text(str(i), 460+30*i, display[1]-45, 30, "black"))
                
            for i in armings:
                screen.blit(i[0],i[1])
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(460+mission.mission_selected*30,display[1]-15,20,2))
  
            if mission.toggle == 1:
                plts = [0,0,0]
                for i in range(len(mission.plot_points)):#if any plot poitns are to be drawn draw them
                    if mission.plot_points[i][1] == 1:
                        plot = 1
                if plot == 1:#draw plot lines
                    
                    figure1.clear()
                    figure2.clear()
                    figure3.clear()
                    for i in range(len(mission.plot_points)):
                        
                        if i <=1:#plot pitch,roll
                            
                            plot = 1
                            if mission.plot_points[i][1] == 1:
                                figure1.plot_fig.line(mission.plot_points[i][0], mission.plot_time ,mission.data[i])
                                figure1.uppdate()
                                figure1.uppdate()
                                plts[0] = 1
                        if i ==2: #plot heading
                             if mission.plot_points[i][1] == 1:
                                 figure2.plot_fig.line(mission.plot_points[i][0], mission.plot_time ,mission.data[i])
                                 figure2.uppdate()
                                 figure2.uppdate()
                                 plts[1] = 1
                        if i >2:#plot speed
                             if mission.plot_points[i][1] == 1:
                                 figure3.plot_fig.line(mission.plot_points[i][0], mission.plot_time ,mission.data[i])
                                 figure3.uppdate()
                                 figure3.uppdate()
                                 plts[2] = 1
                mission.toggle = 0

            for i in range(len(mission.option_text)): #plot poitns text
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(25,35+40*i,20,20))
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(26,36+40*i,18,18))
                if mission.plot_points[i][1] == 1:
                    pygame.draw.rect(screen, (0,255,0), pygame.Rect(25,35+40*i,20,20))
                screen.blit(mission.option_text[i][0],mission.option_text[i][1])
            
            if plts[0] == 1:
                screen.blit(figure1.surface,(offset+300,offset))
            if plts[1] == 1:
                screen.blit(figure2.surface,(offset+300+360,offset))
            if plts[2] == 1:
                screen.blit(figure3.surface,(offset+300,offset+360))

            pygame.draw.rect(screen,(0,0,0),pygame.Rect(19,display[1]-41,22,22))
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(20,display[1]-40,20,20))
            screen.blit(save_text[0],save_text[1])
            
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(19,display[1]-81,22,22))
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(20,display[1]-80,20,20))
            screen.blit(settings_text[0],settings_text[1])
            
            pingAvg = 0
            for i in ping:
                pingAvg += i
            
            ms = peder.text("ms: "+str(int(pingAvg)), display[0]-100, 0, 20, "red")
            screen.blit(ms[0],ms[1])
            
            if mission.save == 1:
                pygame.draw.rect(screen,(0,255,0),pygame.Rect(20,display[1]-40,20,20))
                if pygame.mouse.get_pressed()[0]:
                    tkinter.Tk().withdraw()
                    location = filedialog.askdirectory()
                    if plts[0] == 1:
                        pygame.image.save(figure1.surface,location+"/"+"Pitch, Roll.png")
                    if plts[1] == 1:
                        pygame.image.save(figure2.surface,location+"/"+"Heading.png")
                    if plts[2] == 1:
                        pygame.image.save(figure3.surface,location+"/"+"Speed.png")
                        
            elif mission.save ==2:
                pygame.draw.rect(screen,(0,255,0),pygame.Rect(20,display[1]-80,20,20))
                if pygame.mouse.get_pressed()[0]:
                    plot_state = mission.plot_points
                    menue.location = "settings"
                    loc = "mission plot"
                    
            mission.save = 0
            end = time.time()
            ping.pop(0)
            ping.append((end-start)*100)
            pygame.display.flip()
            clock.tick(fps)
    
    while menue.location == "live plot":
        polling()
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
        pygame.display.flip()
        clock.tick(fps)
    
    while menue.location == "settings":
        settings.pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
        screen.fill("white")
        settings.menue()
        temp = []
        text = []
        temp.append(str(settings.roll_pitch[1][1]))
        temp.append(str(settings.heading[1][1]))
        temp.append(str(settings.speed[1][1]))
        
        for i in range(len(temp)):
            text.append(peder.text(temp[i], settings.boxes[0][0]+70, settings.boxes[0][1]+40*i, 30, "black"))
            
        for i in text:
            screen.blit(i[0],i[1])
        for i in settings.option_text:
            screen.blit(i[0],i[1])
        for i in range(len(settings.option_text)):
            pygame.draw.line(screen, (100,100,100),(0,64+40*i),(400,64+40*i), width=3)
            screen.blit(sprites.plus,(settings.boxes[0][0],settings.boxes[0][1]+40*i))
            screen.blit(sprites.minus,(settings.boxes[1][0],settings.boxes[1][1]+40*i))
            
        screen.blit(text_for_settings[0],text_for_settings[1])
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(19,display[1]-41,22,22))
        if settings.save == 0:
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(20,display[1]-40,20,20))
        elif settings.save == 1:
            pygame.draw.rect(screen,(0,255,0),pygame.Rect(20,display[1]-40,20,20))
        
        polling()
        pygame.display.flip()
        clock.tick(fps)
        
    while menue.location == "test":
        polling()
        counter += 1
        if counter == 1:
            color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        subliminal = peder.text("give A", random.randint(0,display[0]), random.randint(0,display[1]), 30, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            
        screen.fill(color)
        
        if counter == random.randint(0,fps):
            screen.blit(subliminal[0],subliminal[1])
        if counter >= fps:
            counter = 0
        pygame.display.flip()
        clock.tick(fps)
        
    pygame.display.flip()
    clock.tick(fps)  # limits FPS
    
save_file.write_save()
pygame.quit()
sys.exit()