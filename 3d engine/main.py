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
lightingDirection = [0, 1, -1, 1]
cameraVelocity = 10
rotationVelocity = 1

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
mesh = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], 0]]
objectpath = ["3d engine/assets/axis.obj", "3d engine/assets/ship.obj"]
objectposition = [[0, 0, 10], [20, 10, 10]]
objectrotation = [[0, 0, 0], [0, 0, 0]]
objectid = [0, 1]

moveMap = {pygame.K_w: [0, 0, 1], pygame.K_s: [0, 0, -1], 
            pygame.K_SPACE: [0, 1, 0], pygame.K_LSHIFT: [0, -1, 0], 
            pygame.K_a: [1, 0, 0], pygame.K_d: [-1, 0, 0]}

rotMap = {pygame.K_UP: [3.14159 / 180, 0, 0], pygame.K_DOWN: [-3.14159 / 180, 0, 0],
    pygame.K_LEFT: [0, 3.14159 / 180, 0], pygame.K_RIGHT: [0, -3.14159 / 180, 0]}

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
    
    move = [0, 0, 0]
    rotate = [0, 0, 0]
    pressed = pygame.key.get_pressed()
    #move and rotate keybindings
    for key in moveMap:
        if pressed[key]:
            move = addVec(move, moveMap[key])

    for key in rotMap:
        if pressed[key]:
            rotate = addVec(rotate, rotMap[key])

    #calculate deltaTime
    t = pygame.time.get_ticks()
    deltaTime = (t - lastFrameTicks) / 1000
    lastFrameTicks = t

    #update camera position and rotation
    cameraPos = addVec(cameraPos, multVec(normalizeVector(move), cameraVelocity * deltaTime))
    cameraRot = addVec(cameraRot, multVec(normalizeVector(rotate), rotationVelocity * deltaTime))

    #clear screen
    screen.fill("black")

    #clear mesh
    mesh = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], 0]]

    #update relavent variables
    aspectRatio = screen.get_height() / screen.get_width()

    for model in objectid:
        #load object file
        selectedModel = createMeshFromOBJ(objectpath[model])

        #set up basic matricies
        matProj = makeProjMatrix(fov, aspectRatio, viewNear, viewFar)
        matRotX = makeXRotMatrix(cameraRot[0] + objectrotation[model][0])
        matRotY = makeYRotMatrix(cameraRot[1] + objectrotation[model][1])
        matRotZ = makeZRotMatrix(cameraRot[2] + objectrotation[model][2])
        matTrans = makeTranslationMatrix(subVec(cameraPos, objectposition[model]))

        #set up world matrix
        matWorld = makeIdentityMatrix()
        matWorld = matTrans
        matWorld = matrixMultiplyMatrix(matWorld, matRotX)
        matWorld = matrixMultiplyMatrix(matWorld, matRotY)
        matWorld = matrixMultiplyMatrix(matWorld, matRotZ)

        for tri in selectedModel:
            triTransformed = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
            triTransformed[0] = matrixMultiplyVector(matWorld, tri[0])
            triTransformed[1] = matrixMultiplyVector(matWorld, tri[1])
            triTransformed[2] = matrixMultiplyVector(matWorld, tri[2])

            #get normal
            normal = [0, 0, 0, 1]

            line1 = subVec(triTransformed[1], triTransformed[0])
            line2 = subVec(triTransformed[2], triTransformed[0])

            normal = crossProduct(line1, line2)

            normal = normalizeVector(normal)

            #one direction light
            lightingDirection = normalizeVector(lightingDirection)
            shading = ((dotProduct(normal, lightingDirection) + 1) / 2) * 255

            #camera ray
            cameraRay = subVec(triTransformed[0], cameraPos)

            if (dotProduct(normal, normalizeVector(cameraRay))) < 0:
                #project onto screen
                triProjected = [[0, 0, 0], [0, 0, 0], [0, 0, 0], 0]
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

                triProjected[0][0] = -triProjected[0][0] * (0.5 * screen.get_width()) + screen.get_width()
                triProjected[0][1] = -triProjected[0][1] * (0.5 * screen.get_height()) + screen.get_height()
                triProjected[1][0] = -triProjected[1][0] * (0.5 * screen.get_width()) + screen.get_width()
                triProjected[1][1] = -triProjected[1][1] * (0.5 * screen.get_height()) + screen.get_height()
                triProjected[2][0] = -triProjected[2][0] * (0.5 * screen.get_width()) + screen.get_width()
                triProjected[2][1] = -triProjected[2][1] * (0.5 * screen.get_height()) + screen.get_height()
                triProjected[3] = shading

                mesh.append(triProjected)

        mesh.sort(key=sortByAverageZ, reverse=True)

    for tri in mesh:
        pygame.draw.polygon(screen, (tri[3], tri[3], tri[3]), ((tri[0][0], tri[0][1]), (tri[1][0], tri[1][1]), (tri[2][0], tri[2][1])))

        #draw as mesh outline
        #pygame.draw.line(screen, (255, 255, 255), (tri[0][0], tri[0][1]), (tri[1][0], tri[1][1]))
        #pygame.draw.line(screen, (255, 255, 255), (tri[1][0], tri[1][1]), (tri[2][0], tri[2][1]))
        #pygame.draw.line(screen, (255, 255, 255), (tri[2][0], tri[2][1]), (tri[0][0], tri[0][1]))

    #update entire display
    pygame.display.flip()

    #limit framerate
    clock.tick(60)
    
            
#close window when quit
pygame.quit()