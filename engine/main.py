#import modules
import pygame
import math
import time

#import files
from matricies import *
from operationFunctions import *
from functions import *
from classes import *

#settings
cameraMoveVel = 10
cameraRotateVel = 1

#variable init
camera = [0, 0, 0, 1]
lookDir = [0, 0, 1, 1]
yaw = 0
theta = 0
mesh = createMeshFromOBJ("engine/assets/teapot.obj")

#pygame setup
pygame.init()
pygame.font.init
pygame.display.set_caption('3d Renderer')
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

#main loop
while running == True:
    for event in pygame.event.get():
        #quit detection
        if event.type == pygame.QUIT:
            running = False

        #toggle fullscreen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
    
    #clear screen
    screen.fill("black")

    #update variables
    dt = clock.tick(60) / 1000
    #uncomment to cause everything to spin
    #theta = pygame.time.get_ticks()
    aspectRatio = screen.get_height() / screen.get_width()

    #update camera vectors
    upVec = [0, 1, 0]
    target = [0, 0, 1]
    matCameraRot = makeYRotMatrix(yaw)
    lookDir = vecMultMatrix(matCameraRot, target)
    target = vecAdd(camera, lookDir)
    matCamera = makePointAtMatrix(camera, target, upVec)
    rightVec = vecCrossProduct(upVec, lookDir)

    #make view matrix from camera
    matView = invertMatrix(matCamera)

    #controls
    pressed = pygame.key.get_pressed()
    #movement
    if pressed[pygame.K_w]:
        camera = vecAdd(camera, vecMult(vecNormalize(lookDir), (cameraMoveVel * dt)))
    if pressed[pygame.K_s]:
        camera = vecAdd(camera, vecMult(vecNormalize(lookDir), -(cameraMoveVel * dt)))
    if pressed[pygame.K_d]:
        camera = vecAdd(camera, vecMult(vecNormalize(rightVec), (cameraMoveVel * dt)))
    if pressed[pygame.K_a]:
        camera = vecAdd(camera, vecMult(vecNormalize(rightVec), -(cameraMoveVel * dt)))
    if pressed[pygame.K_SPACE]:
        camera = vecAdd(camera, vecMult(vecNormalize(upVec), (cameraMoveVel * dt)))
    if pressed[pygame.K_LSHIFT]:
        camera = vecAdd(camera, vecMult(vecNormalize(upVec), -(cameraMoveVel * dt)))
    #rotation
    if pressed[pygame.K_LEFT]:
        yaw -= cameraRotateVel * dt
    if pressed[pygame.K_RIGHT]:
        yaw += cameraRotateVel * dt
    
    #setup matricies
    #these two don't do anything unless a line above in uncommented
    matRotZ = makeZRotMatrix(theta * 0.5)
    matRotX = makeXRotMatrix(theta)
    
    matTrans = makeTranslationMatrix(0, 0, 5)

    matWorld = makeIdentityMatrix()
    matWorld = matrixMultMatrix(matRotZ, matRotX)
    matWorld = matrixMultMatrix(matWorld, matTrans)

    




pygame.quit()