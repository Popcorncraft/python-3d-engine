#import libraries
from sched import Event
import pygame
import math

#import files
from functions import *
from debugAssets import *
from settings import *
from vectorFunctions import *
from matrixFunctions import *

#settings
fov = 90
viewNear = 0.1
viewFar = 1000
screenWidth = 1280
screenHeight = 720
cameraPos = [0, 0, 0, 1]
cameraRot = [0, 0, 0, 1]
lightingDirection = [0, 0, -1, 1]

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
mesh = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]

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
    aspectRatio = screen.get_height() / screen.get_width()

    #define theta
    t = pygame.time.get_ticks()
    deltaTime = (t - lastFrameTicks) / 1000
    theta += 1 * deltaTime
    lastFrameTicks = t

    #set up basic matricies
    matProj = makeProjMatrix(fov, aspectRatio, viewNear, viewFar)
    matRotX = makeXRotMatrix(theta)
    matRotZ = makeZRotMatrix(theta)
    matTrans = makeTranslationMatrix(0, 0, 10)

    #set up world matrix
    matWorld = makeIdentityMatrix()
    matWorld = matrixMultiplyMatrix(matRotX, matRotZ)
    matWorld = matrixMultiplyMatrix(matWorld, matTrans)

    for tri in selectedModel:
        triTransformed = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
        triTransformed[0] = matrixMultiplyVector(matWorld, tri[0])
        triTransformed[1] = matrixMultiplyVector(matWorld, tri[1])
        triTransformed[2] = matrixMultiplyVector(matWorld, tri[2])

        #get normal
        normal = [0, 0, 0, 1]
        normalizedNormal = [0, 0, 0, 1]
        normal = calculateNormal(tri)
        normalizedNormal = normalizeVector(normal)

        #one direction light
        lightingDirection = normalizeVector(lightingDirection)
        shading = ((dotProduct(normalizedNormal, lightingDirection) + 1) / 2) * 255

        #camera ray
        cameraRay = subVec(triTransformed[0], cameraPos)

        if (dotProduct(normalizedNormal, cameraRay)) > 0:
            #project onto screen
            triProjected = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0]]
            triProjected[0] = matrixMultiplyVector(matProj, triTransformed[0])
            triProjected[1] = matrixMultiplyVector(matProj, triTransformed[1])
            triProjected[2] = matrixMultiplyVector(matProj, triTransformed[2])

            triProjected[0] = divVec(triProjected[0], triProjected[0][3])
            triProjected[1] = divVec(triProjected[1], triProjected[1][3])
            triProjected[2] = divVec(triProjected[2], triProjected[2][3])

            #scale into view
            offsetView = [1, 1, 0, 1]
            triProjected[0] = addVec(triProjected[0], offsetView)
            triProjected[1] = addVec(triProjected[1], offsetView)
            triProjected[2] = addVec(triProjected[2], offsetView)

            triProjected[0][0] *= 0.5 * screen.get_width()
            triProjected[0][1] *= 0.5 * screen.get_height()
            triProjected[1][0] *= 0.5 * screen.get_width()
            triProjected[1][1] *= 0.5 * screen.get_height()
            triProjected[2][0] *= 0.5 * screen.get_width()
            triProjected[2][1] *= 0.5 * screen.get_height()
            triProjected[3] = shading

            mesh.append(triProjected)

    mesh = mesh.sort(key=sortByAverageZ)

    for tri in mesh:
        pygame.draw.polygon(screen, (tri[3], tri[3], tri[3]), ((tri[0][0], tri[0][1]), (tri[1][0], tri[1][1]), (tri[2][0], tri[2][1])))

    #update entire display
    pygame.display.flip()

    #limit framerate
    clock.tick(60)
    
            
#close window when quit
pygame.quit()