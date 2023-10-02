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

camPos = [0,0,-5]
camRot = [0,0,0]
displaySurfaceOffset = [0,0,300]


def projector(ax, ay, az):
    #Don't ask me what math this is
    x = -ax - camPos[0]
    y = -ay - camPos[1]
    z = -az - camPos[2]
    dx = np.cos(camRot[1]) * (np.sin(camRot[2]) * y + np.cos(camRot[2]) * x) - np.sin(camRot[1]) * z
    dy = np.sin(camRot[0]) * (np.cos(camRot[1]) * z + np.sin(camRot[1]) * (np.sin(camRot[2]) * y + np.cos(camRot[2]) * x)) + np.cos(camRot[0]) * (np.cos(camRot[2]) * y - np.sin(camRot[2]) * x)
    dz = np.cos(camRot[0]) * (np.cos(camRot[1]) * z + np.sin(camRot[1]) * (np.sin(camRot[2]) * y + np.cos(camRot[2]) * x)) - np.sin(camRot[0]) * (np.cos(camRot[2]) * y - np.sin(camRot[2]) * x)
    finalx = (((displaySurfaceOffset[2] / dz) * dx + displaySurfaceOffset[0]) + 1280 / 2) * 1
    finaly = (((displaySurfaceOffset[2] / dz) * dy + displaySurfaceOffset[1]) + 720 / 2) * 1
    return(finalx, finaly)


while running:
    #poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #key press detection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                camPos[0] = camPos[0] - 1
            if event.key == pygame.K_RIGHT:
                camPos[0] = camPos[0] + 1
            if event.key == pygame.K_UP:
                camPos[2] = camPos[2] + 1
            if event.key == pygame.K_DOWN:
                camPos[2] = camPos[2] - 1
            if event.key == pygame.K_SPACE:
                camPos[1] = camPos[1] - 1
            if event.key == pygame.K_LSHIFT:
                camPos[1] = camPos[1] + 1
            print(camPos)

    #clear previous frame
    screen.fill("gray")

    #generate frame
    pygame.draw.line(screen, "blue", projector(0, 0, 0), projector(1, 0, 0))
    pygame.draw.line(screen, "red", projector(0, 0, 0), projector(0, 1, 0))
    pygame.draw.line(screen, "green", projector(0, 0, 0), projector(0, 0, 1))

    #display generated frame
    pygame.display.flip()

    #frame rate cap
    clock.tick(60)


pygame.quit()