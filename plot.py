import pygame, sys
import glob, os
import AUV_F
import time
import pygame_chart as pyc
import tkinter
from tkinter import filedialog
import random
import numpy as np

if True: #initialising variables and functions
    print()
    print("settup starting")
    print()
    save_file = AUV_F.save_file()#save file containing location of log files
    logfil = save_file.save[0][1]#variable containing logfile location
    os.chdir(logfil)#open logfile location
    
    #variables for initialising
    display = (1224,800)#how big is the display window
    filer = []
    pltScreen = [[800,360],[360,360]]#live plot values
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
    #pygame initialising
    pygame.init()
    pygame.joystick.init()
    screen = pygame.display.set_mode(display)
    clock = pygame.time.Clock()
    pygame.display.set_caption("AUV plot") 
    # initialising objects
    meny = AUV_F.plot(logfil,pltScreen,offset)          #liveplot object
    menue = AUV_F.menue("menue",save_file.save[0][1])   #menue object
    settings = AUV_F.settings(display)                  #settings object
    sprites = AUV_F.sprites()                           #sprites for settings
    color_sprite = [AUV_F.color_sprites(settings.color[1][0]),AUV_F.color_sprites(settings.color[1][1]),AUV_F.color_sprites(settings.color[1][2])] #object for selecting color in settings
    cube = AUV_F.cube("black","white",settings.color[1])        #wire cube for visualising
       #wire cube for visualising
    #text
    text_for_settings = AUV_F.text("save settings",45,display[1]-45,30,"black")
    controller_text = AUV_F.text("Connect Controller to continiue",display[0]/2,display[1]/2,30,"black")
    controller_text = AUV_F.text("Connect Controller to continiue",(display[0]-controller_text[1][2])/2,display[1]/4-15,30,"black")
    text = [((30,400),(255,0,0),"Pitch: "),((130,400),(255,255,0),"Roll: "),((230,400),(0,0,255),"Heading: ")]
    mission_text_min = AUV_F.text("start:",250,display[1]-50,30,"black")
    mission_text_max = AUV_F.text("stop:",700,display[1]-50,30,"black")
    #other variables
    running = True #variable to keep the program running
    
    counter = 0 #counter to do stuff
    fps = 24 # frames per second
    font = pygame.font.Font('freesansbold.ttf', 12)# font for text in program
    ping = 0#variable for timing purpuses
    loc = 0# location used to know from where settings was accesed(from menue or from mission plot)
    
    global mission4
    global plot_state
    global down
    global data_flag
    data_flag = 0
    down = 0
    plot_state = 0
    rot_count = 0
    rot_count_complete = np.pi*2
    
    live_cube = AUV_F.cube("green","black",settings.color[1])
    print("settup complete")
    
def polling():#get user input keyboard
    global running
    global counter
    global loc
    global down
    global data_flag
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            menue.location = "quit"
            data_flag = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if loc !=0:
                    menue.location = loc
                    loc = 0
                elif data_flag == 1:
                    data_flag = 0
                else:
                    menue.location = "menue"
                    #menue.location = "dev1"
                    menue.file_select = 0
                counter = 0
        elif event.type == pygame.MOUSEMOTION:
            pass
def controller():#get user input controller
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            menue.location = "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                
                menue.location = "menue"
                menue.file_select = 0 
                
while running: # start of main code
    # poll for events (userinputs)
    #time execution time
    polling()
    
    while menue.location == "menue": #start menue
        polling()
        screen.fill("white")
        menue.get_pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])#get posision of mouse
        
        for i in menue.options:#draw optiosn on screen
            if i[0] ==  0:
                screen.blit(i[1][0],i[1][1])
            elif i[0] == 1:
                screen.blit(i[2][0],i[2][1])
        
        if menue.file_select == 1:# if mission plot selected draw dividing line and show logfiles available
            pygame.draw.line(screen, (0,0,0),(250,0),(250,600), width=3)
            for i in menue.log_fil:
                screen.blit(i[0],i[1])
        pygame.display.flip()
        clock.tick(fps)
           
    while menue.location == "mission plot":#initialising of showing mission plots
        ping=[0,0,0,0,0,0,0,0,0,0]#timing variable
        screen.fill("white")
        draw = 0#flag to see if plots needs uppdating
        plts = [0,0,0]#variable to see witch plot needs uppdating
        mission = AUV_F.mission_Plot(menue.file_Selected,display,plot_state)#object for plotting
        plot_state = 0
        
        set_min = AUV_F.plot_start_stop(0,mission.time,mission.start_time)
        set_max = AUV_F.plot_start_stop(mission.start_time,mission.max,mission.time)
        
        #plotting
        figure1 = AUV_F.plot_surface(360, 360, "Pitch, Roll")
        figure1.limit(settings.roll_pitch[1][0],settings.roll_pitch[1][1])
        
        figure2 = AUV_F.plot_surface(360, 360, "Heading")
        figure2.limit(settings.heading[1][0],settings.heading[1][1])
        
        figure3 = AUV_F.plot_surface(360, 360, "Speed")
        figure3.limit(settings.speed[1][0],settings.speed[1][1])
        
        for i in range(len(mission.option_text)): #plot poitns text
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(25,35+40*i,20,20))
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(26,36+40*i,18,18))
            if mission.plot_points[i][1] == 1:
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(25,35+40*i,20,20))
            screen.blit(mission.option_text[i][0],mission.option_text[i][1])
        
        screen.blit(mission_text_min[0],mission_text_min[1])
        while menue.location == "mission plot":#main section of mission plotting
            start = time.time()#timing variable
            screen.fill("white")
            polling()
            save_text = AUV_F.text("save plots",45,display[1]-45,30,"black")
            settings_text = AUV_F.text("settings",45,display[1]-85,30,"black")
            plot = 0# flagg to see if plots change

            mission.get_pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])#get mouse posision

            

  
            if mission.toggle == 1:
                plts = [0,0,0]
                for i in range(len(mission.plot_points)):#if any plot poitns are to be drawn draw them
                    if mission.plot_points[i][1] == 1:
                        plot = 1
                if plot == 1:#draw plot 
                    figure1.clear()
                    figure2.clear()
                    figure3.clear()
                    for i in range(len(mission.plot_points)):
                        if i <=1:#plot pitch,roll
                            if mission.plot_points[i][1] == 1:
                                figure1.plot_fig.line(mission.plot_points[i][0], mission.plot_time ,mission.data[i],color = settings.color[1][i])
                                figure1.uppdate()
                                figure1.uppdate()
                                plts[0] = 1
                        if i ==2: #plot heading
                             if mission.plot_points[i][1] == 1:
                                 figure2.plot_fig.line(mission.plot_points[i][0], mission.plot_time ,mission.data[i],color = settings.color[1][i])
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
            
            ms = AUV_F.text("ms: "+str(int(pingAvg)), display[0]-100, 0, 20, "red")
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
                    
            screen.blit(mission_text_min[0],mission_text_min[1])
            screen.blit(mission_text_max[0],mission_text_max[1])
            
            set_min.draw(0,mission.time,mission.start_time)
            set_max.draw(mission.start_time,mission.max,mission.time)
            
            screen.blit(set_min.surface,(330,display[1]-65))
            screen.blit(set_max.surface,(830,display[1]-65))
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
        
        live_cube.rotate(meny.x,meny.y,meny.z,240)
        #live_cube.rotate(meny.x,meny.y,0)
        
        screen.blit(live_cube.board,(100,400))
        meny.move_plot()
        pygame.display.flip()
        clock.tick(fps)
    
    while menue.location == "settings":
        polling()
        settings.pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0],down)
        screen.fill("white")
        settings.menue()
        temp = []
        text = []
        temp.append(str(settings.roll_pitch[1][1]))
        temp.append(str(settings.heading[1][1]))
        temp.append(str(settings.speed[1][1]))
        
        for i in range(len(temp)):
            text.append(AUV_F.text(temp[i], settings.boxes[0][0]+70, settings.boxes[0][1]+40*i, 30, "black"))
        
        for i in text:
            screen.blit(i[0],i[1])
        for i in settings.option_text:
            screen.blit(i[0],i[1])
        for i in range(len(settings.option_text)-1):
            pygame.draw.line(screen, (100,100,100),(0,64+40*i),(400,64+40*i), width=3)
            screen.blit(sprites.plus,(settings.boxes[0][0],settings.boxes[0][1]+40*i))
            screen.blit(sprites.minus,(settings.boxes[1][0],settings.boxes[1][1]+40*i))
            
        for i in settings.color_options:
            screen.blit(i[0],i[1])
            
        for i in range(len(color_sprite)):
            screen.blit(color_sprite[i].option,(250,195+i*40))
            
        if settings.color_change != 0:
            screen.blit(color_sprite[settings.color_change-1].select,(500,190))
            if settings.new_color != 0:
                color_sprite[settings.color_change-1].uppdate(settings.new_color)
            settings.color[1][settings.color_change-1] = list(color_sprite[settings.color_change-1].color)
            cube.new_color(settings.color[1])
            live_cube.new_color(settings.color[1])
            
        screen.blit(text_for_settings[0],text_for_settings[1])
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(19,display[1]-41,22,22))
        if settings.save == 0:
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(20,display[1]-40,20,20))
        elif settings.save == 1:
            pygame.draw.rect(screen,(255,255,0),pygame.Rect(20,display[1]-40,20,20))
        
        polling()
        pygame.display.flip()
        clock.tick(fps)
        
    while menue.location == "dev1":
        rot_count += np.pi/180
        rot_count = 1
        polling()
        screen.fill("white")
        screen.blit(cube.board,(50,50))
        cube.rotate(0,0,0,150)
        
        if rot_count >= rot_count_complete:
            rot_count = 0
        
        pygame.display.flip()
        clock.tick(fps)
        
    while menue.location == "controller":
        
        while pygame.joystick.get_count() == 0 and running == True and menue.location == "controller":
            screen.fill("white")
            screen.blit(controller_text[0],controller_text[1])
            pygame.display.flip()
            clock.tick(fps)
            controller()
            
        while menue.location == "controller":
            controller()
            screen.fill("white")
            pygame.display.flip()
            clock.tick(fps)
    
    while menue.location == "test":
        data = AUV_F.new_plot(menue.file_Selected,display)
        data_flag = 0
        a = 1
        xtext = AUV_F.text("X:", 10, 10, 30, "black")
        ytext = AUV_F.text("Y:", 100, 10, 30, "black")
        big_plot = AUV_F.big_plot()
        while menue.location == "test":
            polling()
            screen.fill("white")
            data.get_pos(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
            
            
            for i in range(len(data.text)):
                screen.blit(data.text[i][data.text[i][0]][0],data.text[i][data.text[i][0]][1])
                
            pygame.draw.line(screen, (0,0,0),(370,0),(370,display[1]-10), width=3)
            if len(data.save) > 0:
                screen.blit(data.plot_text[data.plot_text[0]][0],data.plot_text[data.plot_text[0]][1])
            if data.next > 0:
                
                pygame.draw.line(screen, (0,0,0),(data.text[data.next-1][1][1][0],data.text[data.next-1][1][1][1]+32),(data.text[data.next-1][1][1][0]+data.text[data.next-1][1][1][2],data.text[data.next-1][1][1][1]+32), width=3)
                for i in range(len(data.next_data)):
                    pygame.draw.rect(screen,(0,0,0),pygame.Rect(390,14+50*i,22,22))
                    set_color = (255,255,255)
                    for p in data.save:
                        if p[0] == data.next-1 and p[1] == i:
                            set_color = (0,255,0)
                    pygame.draw.rect(screen,set_color,pygame.Rect(391,15+50*i,20,20))
                    screen.blit(data.next_data[i][data.next_data[i][0]][0],data.next_data[i][data.next_data[i][0]][1])
            if data.plot == True:
                data_flag = 1
                data.plot = False
                data.plot_data()
                while data_flag == 1:
                    polling()
                    data.get_pos_2(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
                    screen.fill("white")
                    screen.blit(xtext[0],xtext[1])
                    screen.blit(ytext[0],ytext[1])
                    pygame.draw.rect(screen,(0,0,0),pygame.Rect(42,8,30,30))
                    pygame.draw.rect(screen,(0,0,0),pygame.Rect(132,8,30,30))
                    
                    pygame.draw.rect(screen,(255,255,255),pygame.Rect(44,10,26,26))
                    pygame.draw.rect(screen,(255,255,255),pygame.Rect(134,10,26,26))
                    if data.chose != 0:
                        pygame.draw.rect(screen,(0+255*(data.chose-1),255,0),pygame.Rect(44+90*(data.chose-1),10,26,26))
                        
                    for i in range(len(data.data_to_plot)):
                        screen.blit(data.data_to_plot[i][0][0],data.data_to_plot[i][0][1])
                        pygame.draw.rect(screen,(0,0,0),pygame.Rect(20,62+50*i,22,22))
                        if data.data_to_plot[i][1] == 1:
                            pygame.draw.rect(screen,(0,255,0),pygame.Rect(21,63+50*i,20,20))
                        elif data.data_to_plot[i][1] == 2:
                            pygame.draw.rect(screen,(255,255,0),pygame.Rect(21,63+50*i,20,20))
                        else:
                            pygame.draw.rect(screen,(255,255,255),pygame.Rect(21,63+50*i,20,20))
                        if data.data_to_plot[i][2] != 0:
                            screen.blit(data.data_to_plot[i][3][0],data.data_to_plot[i][3][1])
                    
                    screen.blit(data.plot_text2[data.plot_text2[0]][0],data.plot_text2[data.plot_text2[0]][1])
                    if data.start_plot == 1:
                        data.a = 1
                        data.start_plot = 0
                        for i in range(3):
                            if data.chosen[0][i] == 0 or data.chosen[0][i] == 1:
                                data.x[i] = data.time_plot
                            else:
                                pass
                                data.x[i] = data.df[data.data[data.save[data.chosen[0][i]-2][0]][1][data.save[data.chosen[0][i]-2][1]]].tolist()
                            
                            if data.chosen[1][i] == 0:
                                data.y[i] = data.time_plot
                            else:
                                data.y[i] = data.df[data.data[data.save[data.chosen[1][i]-2][0]][1][data.save[data.chosen[1][i]-2][1]]].tolist()
                        
                    if data.a == 1:
                        for i in range(len(data.plot_text3)):
                            screen.blit(data.plot_text3[i][0],data.plot_text3[i][1])
                            
                    if data.b[1] == 1:
                        pygame.draw.line(screen, (0,0,0),(80+30*data.b[2],display[1]-18),(100+30*data.b[2],display[1]-18), width=3)
                        print(data.df["altitudeAboveTerr"][0])
                    if data.b[0] == 1:
                        data.b[0] = 0
                        
                        big_plot.clear()
                        try:
                            big_plot.plot_fig.line(str(data.b), data.x[data.b[2]] , data.y[data.b[2]] ,color = (0,0,0))
                        except:
                            big_plot.error()
                        big_plot.uppdate()

                        
                            

                                    


                    
                    screen.blit(big_plot.surface,(400,10))
                        
                    
                    pygame.display.flip()
                    clock.tick(fps)
            
            
            pygame.display.flip()
            clock.tick(fps)
        
    pygame.display.flip()
    clock.tick(fps)  # limits FPS
    
pygame.joystick.quit()
save_file.write_save()
pygame.quit()
sys.exit()