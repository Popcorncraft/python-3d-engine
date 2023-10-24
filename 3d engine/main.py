#import libraries
from sched import Event
import pygame
import math

#import files
from functions import *
from debugAssets import *
from settings import *

#pygame setup
pygame.init()
pygame.font.init
pygame.display.set_caption('3d Renderer')
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

#init variables
theta = 0
lastFrameTicks = 1
selectedModel = createMeshFromOBJ("3d engine/assets/teapot.obj")

#main loop
while running == True:
    #test for events
    for event in pygame.event.get():
        #quit detection
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # Toggle Fullscreen with F11
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
    #clear screen
    screen.fill("black")

    #update relavent variables
    fovRad = 1 / math.tan(fov * 0.5 / 180 * math.pi)
    aspectRatio = screen.get_height() / screen.get_width()

    #define theta
    t = pygame.time.get_ticks()
    deltaTime = (t - lastFrameTicks) / 1000
    theta += 1 * deltaTime
    lastFrameTicks = t

    #set up and update matricies
    matProj = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]
    matProj[0][0] = aspectRatio * fovRad
    matProj[1][1] = fovRad
    matProj[2][2] = viewFar / (viewFar - viewNear)
    matProj[3][2] = (-viewFar * viewNear) / (viewFar - viewNear)
    matProj[2][3] = 1.0
    matProj[3][3] = 0.0

    matRotZ = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]
    matRotZ[0][0] = math.cos(theta)
    matRotZ[0][1] = math.sin(theta)
    matRotZ[1][0] = -math.sin(theta)
    matRotZ[1][1] = math.cos(theta)
    matRotZ[2][2] = 1
    matRotZ[3][3] = 1

    matRotX = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]
    matRotX[0][0] = 1
    matRotX[1][1] = math.cos(theta * 0.5)
    matRotX[1][2] = math.sin(theta * 0.5)
    matRotX[2][1] = -math.sin(theta * 0.5)
    matRotX[2][2] = math.cos(theta * 0.5)
    matRotX[3][3] = 1

    projectedMesh = []

    for tri in selectedModel:
        #rotate z-axis
        triRotatedZ = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        triRotatedZ[0] = MultiplyMatrixVector(tri[0], matRotZ)
        triRotatedZ[1] = MultiplyMatrixVector(tri[1], matRotZ)
        triRotatedZ[2] = MultiplyMatrixVector(tri[2], matRotZ)

        #rotate x-axis
        triRotatedZX = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        triRotatedZX[0] = MultiplyMatrixVector(triRotatedZ[0], matRotX)
        triRotatedZX[1] = MultiplyMatrixVector(triRotatedZ[1], matRotX)
        triRotatedZX[2] = MultiplyMatrixVector(triRotatedZ[2], matRotX)

        #offset into screen
        triTranslated = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        triTranslated = triRotatedZX
        triTranslated[0][2] = triRotatedZX[0][2] + 10
        triTranslated[1][2] = triRotatedZX[1][2] + 10
        triTranslated[2][2] = triRotatedZX[2][2] + 10
        
        #add triangles to mesh
        projectedMesh.append(triTranslated)
    
    #sort triangles in mesh by z depth
    projectedMesh.sort(reverse=True, key=sortByAverageZ)

    for tri in projectedMesh:
        #get normal
        normal = [0, 0, 0]
        normalizedNormal = [0, 0, 0]
        normal = calculateNormal(tri)
        normalizedNormal = normalizeVector(normal)

        if (
            normalizedNormal[0] * (tri[0][0]) + 
            normalizedNormal[1] * (tri[0][1]) + 
            normalizedNormal[2] * (tri[0][2])
            ) < 0:
            #one direction light
            lightingDirection = normalizeVector(lightingDirection)
            shading = ((dotProduct(normalizedNormal, lightingDirection) + 1) / 2) * 255

            #project onto screen
            triProjected = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            triProjected[0] = MultiplyMatrixVector(tri[0], matProj)
            triProjected[1] = MultiplyMatrixVector(tri[1], matProj)
            triProjected[2] = MultiplyMatrixVector(tri[2], matProj)

            #scale into view
            triProjected[0][0] += 1
            triProjected[1][0] += 1
            triProjected[2][0] += 1
            triProjected[0][1] += 1
            triProjected[1][1] += 1
            triProjected[2][1] += 1

            triProjected[0][0] *= 0.5 * screen.get_width()
            triProjected[0][1] *= 0.5 * screen.get_height()
            triProjected[1][0] *= 0.5 * screen.get_width()
            triProjected[1][1] *= 0.5 * screen.get_height()
            triProjected[2][0] *= 0.5 * screen.get_width()
            triProjected[2][1] *= 0.5 * screen.get_height()

            #convert to 2d points
            screenCoords = [[0, 0],[0, 0],[0, 0]]
            screenCoords[0][0] = triProjected[0][0]
            screenCoords[0][1] = triProjected[0][1]
            screenCoords[1][0] = triProjected[1][0]
            screenCoords[1][1] = triProjected[1][1]
            screenCoords[2][0] = triProjected[2][0]
            screenCoords[2][1] = triProjected[2][1]

            #draw wire-frame
            pygame.draw.polygon(screen, (shading, shading, shading), (screenCoords[0], screenCoords[1], screenCoords[2]))
            #pygame.draw.line(screen, "white", screenCoords[0], screenCoords[1])
            #pygame.draw.line(screen, "white", screenCoords[1], screenCoords[2])
            #pygame.draw.line(screen, "white", screenCoords[2], screenCoords[0])

    #update entire display
    pygame.display.flip()

    #limit framerate
    clock.tick(60)
    
            
#close window when quit
pygame.quit()