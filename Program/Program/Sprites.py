import pygame, sys
import glob, os
import AUV_F
import time
import pygame_chart as pyc
import tkinter
from tkinter import filedialog
import random
import numpy as np

def text(skrift,x,y,z,color):
    font2 = pygame.font.Font('freesansbold.ttf', z)
    text = font2.render(skrift, True, color)
    textRect = text.get_rect()
    textRect.center = (x+textRect[2]/2, y+textRect[3]/2)
    ret = (text,textRect)
    return ret

def text_mid(skrift,x,y,z,color):
    font2 = pygame.font.Font('freesansbold.ttf', z)
    text = font2.render(skrift, True, color)
    textRect = text.get_rect()
    textRect.center = (x,y)
    ret = (text,textRect)
    return ret

def text_end(skrift,x,y,z,color):
    font2 = pygame.font.Font('freesansbold.ttf', z)
    text = font2.render(skrift, True, color)
    textRect = text.get_rect()
    textRect.center = (x-textRect[2]/2, y)
    ret = (text,textRect)
    return ret

class button:
    def __init__(self):
        pass
    
class slider:
    def __init__(self,text,color,x,y,val_min,val_max,val_now):
        self.location = (x,y)
        self.box = [[x,y,350,80],[120,20,200,50]]
        self.color = color
        self.surface = pygame.Surface((self.box[0][2],self.box[0][3]))
        self.write = text
        
        
        self.draw(val_min,val_max,val_now)
        
    def draw(self,minv,maxv,curv):
        self.val_max = maxv
        self.val_min = minv
        self.val_now = curv
        
        self.min = text_mid(str(self.val_min), 120, 12, 20, "black")
        self.max = text_mid(str(self.val_max), 320, 12, 20, "black")
        self.cur = text_end(str(self.val_now), 115, 45, 30, "black")
        self.text = text(self.write, 5, 30, 30, "black")
        self.liste = [self.min,self.max,self.cur,self.text]
        self.point = (self.val_now-self.val_min)/((self.val_max-self.val_min)/200)
        
        self.surface.fill("black")
        pygame.draw.rect(self.surface, self.color, pygame.Rect(1,1,348,78))
        
        for i in range(len(self.liste)):
            self.surface.blit(self.liste[i][0],self.liste[i][1])
            
        pygame.draw.rect(self.surface, "black", pygame.Rect(119,19,202,52))
        pygame.draw.rect(self.surface, self.color, pygame.Rect(120,20,200,50))
        pygame.draw.line(self.surface,"black",(self.box[1][0]+self.point,self.box[1][1]),(self.box[1][0]+self.point,self.box[1][1]+self.box[1][3]), width=3)

