import XInput as x
import pygame
import time
import numpy as np

user_index = None
white = (255, 255, 255)
black = (0,0,0)
red = (255,0,0)
green = (0,150,0)

bg = pygame.image.load("bgctv47vttm51.png")

class rov:
    def __init__(self,mass,time):
        self.resistance = [0,0,0]
        self.pos = [100,100,0]
        self.time = time
        self.mass = mass
        self.speed = 0
        self.acceleration = 0
        self.pitch = 0
        self.yaw = np.pi/2
        self.roll = 0
        
    def atos(self):
        self.speed += self.acceleration*self.time
        self.speed -= (self.speed/50)
        if self.speed < 0.05:
            self.speed = 0

    def uppdate_pos(self):
        self.atos()
        sx = self.speed*np.cos(self.yaw)
        sy = self.speed*np.sin(self.yaw)
        if self.pos[0] + sx >= 200:
            self.pos[0] += sx-200
        elif self.pos[0] + sx <= 0:
            self.pos[0] += sx+200
        else:
            self.pos[0] += sx
            
        if self.pos[1] + sy >= 200:
            self.pos[1] += sy-200
        elif self.pos[1] + sy <= 0:
            self.pos[1] += sy+200
        else:
            self.pos[1] += sy
        
        
    def sped(self,x):
        self.uppdate_pos()
        self.acceleration = x


while True:
    controller = x.get_connected()
    for i in range(len(controller)):
        if controller[i]:
            user_index = i
    if user_index != None:
        break

    
def find_key(input_dict, value):
    return {k for k, v in input_dict.items() if v == value}

def poll():
    global thumb
    global trigger
    state = x.get_state(user_index)
    trigger = x.get_trigger_values(state)
    thumb = x.get_thumb_values(state)
    buttons = x.get_button_values(state)
    a = find_key(buttons,True)
    return a


def collor(col):
    if col < 0:
        ret = ((int(col*255)*-1),0,0)
    elif col > 0:
        ret = (0,int(col*255),0)
    return ret

def mtext(skrift,x,y,z,color):
    font2 = pygame.font.Font('freesansbold.ttf', z)
    text = font2.render(skrift, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    ret = (text,textRect)
    return ret

pygame.init()
screen = pygame.display.set_mode((640, 397))
pygame.display.set_caption('Controller mapping')
font = pygame.font.Font('freesansbold.ttf', 12)

clock = pygame.time.Clock()
running = True


back = 0


location = "menue"

first = 1
fps = 60
sim = rov(10,1/fps)
while back == 0:
    if first == 1:
        first = 0
        click = 0
        frames = 0
        tid = time.time()
        delay = int((time.time()-tid)*1000)
        location = "menue"
        save = 0
        bot = 4
        pointer = 0
        move = 0
        a = [320,200]
        
    
    if frames >= 60:
        frames = 0
    else:
        frames +=1
    tid = time.time()
    b = poll()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            back = 1
    #if True:
        if 'DPAD_UP' in b:
            a[1] -= 1
        elif 'DPAD_DOWN' in b:
            a[1] += 1
        if 'DPAD_LEFT' in b:
            a[0] -= 1
        elif 'DPAD_RIGHT' in b:
            a[0] += 1
        if "A" in b:
            print(a)
        
    if "START" in b:
        location = "menue"
        pointer = 0
        
        
    if location == "menue":
        if "A" in b:
            if pointer == 1:
                location = "show"
                move = 0
                a = [320,200]
            elif pointer == bot:
                back = 1
            elif pointer == 2:
                location = "bot"
                a = [320,200]
                
        option1 = mtext("Controller",320,100,30,black)
        option2 = mtext("Simulation",320,150,30,black)
        option3 = mtext("hello",320,200,30,black)
        option4 = mtext("Exit",320,250,30,black)
        if len(b)!= 0 and click == 0:
            if 'DPAD_UP' in b:
                click = 1
            elif 'DPAD_DOWN' in b:
                click = 2

            
        if click != 0:
            if save == 0:
                if click == 1:
                    if pointer <= 1:
                        pointer = bot
                    else:
                        pointer -= 1
                elif click == 2:
                    if pointer >= bot:
                        pointer = 1
                    else:
                        pointer += 1
            save += 1

            if save >= 10:
                save = 0
                click = 0


            
        if pointer == 1:
            option1 = mtext("Controller",320,100,33,green)
        elif pointer == 2:
            option2 = mtext("Simulation",320,150,33,green)
        elif pointer == 3:
            option3 = mtext("hello",320,200,33,green)
        elif pointer == 4:
            option4 = mtext("Exit",320,250,33,red)

        
        screen.fill(white)
        screen.blit(option1[0],option1[1])
        screen.blit(option2[0],option2[1])
        screen.blit(option3[0],option3[1])
        screen.blit(option4[0],option4[1])
        
    if location == "show":
        screen.blit(bg, (0, 0))
        if 'DPAD_UP' not in b:
            screen.blit(font.render("False", True, black), [130,283])
        if 'DPAD_LEFT' not in b:
            screen.blit(font.render("False", True, black), [130,311])
        if 'DPAD_DOWN' not in b:
            screen.blit(font.render("False", True, black), [130,337])
        if 'DPAD_RIGHT' not in b:
            screen.blit(font.render("False", True, black), [130,368])
        if "LEFT_THUMB" not in b:
            screen.blit(font.render("False", True, black), [130,181])
        if "RIGHT_THUMB" not in b:
            screen.blit(font.render("False", True, black), [487, 368])
        if "LEFT_SHOULDER" not in b:
            screen.blit(font.render("False", True, black), [130, 53])
        if "RIGHT_SHOULDER" not in b:
            screen.blit(font.render("False", True, black), [487, 51])
        if 'A' not in b:
            screen.blit(font.render("False", True, black), [487, 267])
        if 'Y' not in b:
            screen.blit(font.render("False", True, black), [487, 113])
        if 'X' not in b:
            screen.blit(font.render("False", True, black), [487, 177])
        if'B' not in b:
            screen.blit(font.render("False", True, black), [487, 155])
        
        
        if len(b)!= 0:
            if frames % 10 == 0 and move == 1:
                print(b)
            if 'DPAD_UP' in b:
                pygame.draw.rect(screen, red, pygame.Rect(285, 165, 10, 10))
                screen.blit(font.render("True", True, green), [130,283])
            elif 'DPAD_DOWN' in b:
                pygame.draw.rect(screen, red, pygame.Rect(285, 189, 10, 10))
            if 'DPAD_LEFT' in b:
                pygame.draw.rect(screen, red, pygame.Rect(273, 177, 10, 10))
                screen.blit(font.render("True", True, green), [130,311])
            elif 'DPAD_RIGHT' in b:
                pygame.draw.rect(screen, red, pygame.Rect(297, 177, 10, 10))
                screen.blit(font.render("True", True, green), [130,368])
            if 'A' in b:
                pygame.draw.circle(screen,red,[389,159], 9, 3)
                screen.blit(font.render("True", True, green), [487, 267])
            if 'Y' in b:
                pygame.draw.circle(screen,red,[389,125], 9, 3)
                screen.blit(font.render("True", True, green), [487, 113])
            if 'X' in b:
                pygame.draw.circle(screen,red,[371,141], 9, 3)
                screen.blit(font.render("True", True, green), [487, 177])
            if'B' in b:
                pygame.draw.circle(screen,red,[407,141], 9, 3)
                screen.blit(font.render("True", True, green), [487, 155])
            if "LEFT_THUMB" in b:
                screen.blit(font.render("True", True, green), [130,181])
            if "RIGHT_THUMB" in b:
                screen.blit(font.render("True", True, green), [487, 368])
            if "LEFT_SHOULDER" in b:
                screen.blit(font.render("True", True, green), [130,53])
            if "RIGHT_SHOULDER" in b:
                screen.blit(font.render("True", True, green), [487,51])
            if "BACK" in b:
                move = 1
                    
    
        for i in range(len(thumb)):
            if thumb[0][1]!=0:
                screen.blit(font.render(str(int(thumb[0][1]*100)), True, collor(thumb[0][1])), [140,124])
            else:
                screen.blit(font.render("0", True, black), [140,124])
            
            if thumb[0][0]!=0:
                screen.blit(font.render(str(int(thumb[0][0]*100)), True, collor(thumb[0][0])), [140,152])
            else:
                screen.blit(font.render("0", True, black), [140,152])
            
            if thumb[1][1]!=0:
                screen.blit(font.render(str(int(thumb[1][1]*100)), True, collor(thumb[1][1])), [481,315])
            else:
                screen.blit(font.render("0", True, black), [481,315])
            
            if thumb[1][0]!=0:
                screen.blit(font.render(str(int(thumb[1][0]*100)), True, collor(thumb[1][0])), [481,339])
            else:
                screen.blit(font.render("0", True, black), [481,339])


        screen.blit(font.render(str(int(trigger[0]*100)), True, (0,int(trigger[0]*255),0)), [140,87])
        screen.blit(font.render(str(int(trigger[1]*100)), True, (0,int(trigger[1]*255),0)), [486,78])
        screen.blit(font.render(str(delay), True, black), (600,3))
    
        if thumb[0][0] > 0.5:
            a[0] += 1
        elif thumb[0][0] < -0.5:
            a[0] -= 1
        if thumb[0][1]> 0.5:
            a[1] -= 1
        elif thumb[0][1] < -0.5:
            a[1] += 1
        if move == 1:
            if 'A' in b:
                print(a)
            #pygame.draw.circle(screen,red,a, 9, 3)
            #pygame.draw.rect(screen, red, pygame.Rect(a[0], a[1], 10, 10))
            screen.blit(font.render("0", True, black), a)
            move = 1

    if location == "bot":
        sim.sped(trigger[0]*5)
        sim.yaw += thumb[0][0]*(np.pi/90)*-1
        
        screen.fill(white)
        
        pygame.draw.aaline(screen,black,(20,20),(20,220))
        pygame.draw.aaline(screen,black,(20,220),(220,220))
        screen.blit(font.render("0", True, black), [9,216])
        screen.blit(font.render("200", True, black), [230,214])
        screen.blit(font.render("200", True, black), [10,6])
        pygame.draw.rect(screen, red, pygame.Rect(21+int(sim.pos[0]), 217-int(sim.pos[1]), 3, 3))
        #screen.blit(font.render("200", True, black), a)
        


    pygame.display.flip()
    delay = int((time.time()-tid)*1000)
    clock.tick(fps)
    
pygame.quit()