from sched import Event
import pygame
import math
import numpy as np

#pygame setup
pygame.init()
pygame.font.init
pygame.display.set_caption('3d Renderer')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

matProj = [
    [],
    [],
    [],
    []
    ]

def MultMatrixVector(x, y, z):
    print()

#main loop
while running:
    #test for events
    for event in pygame.event.get():
        #quit detection
        if event.type == pygame.QUIT:
            running = False
    
            
#close window when quit
pygame.quit()