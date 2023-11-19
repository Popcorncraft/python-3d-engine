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
fov = 90
triToRaster = []
listTriangles = []
tester = False

#object init
#axis = meshObject(0, "engine/assets/axis.obj", [0, 0, 5, 1], [0, 0, 0, 1])
#objectList = [axis]
mesh = createMeshFromOBJ("engine/assets/axis.obj")

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
    upVec = [0, 1, 0, 1]
    target = [0, 0, 1, 1]
    matCameraRot = makeYRotMatrix(yaw)
    lookDir = vecMultMatrix(matCameraRot, target)
    target = vecAdd(camera, lookDir)
    matCamera = makePointAtMatrix(camera, target, upVec)

    #make view matrix from camera
    matView = invertMatrix(matCamera)

    #controls
    pressed = pygame.key.get_pressed()
    #movement
    #if pressed[pygame.K_w]:
    #    camera = vecAdd(camera, vecMult(vecNormalize(lookDir), (cameraMoveVel * dt)))
    #if pressed[pygame.K_s]:
    #    camera = vecAdd(camera, vecMult(vecNormalize(lookDir), -(cameraMoveVel * dt)))
    #if pressed[pygame.K_d]:
    #    camera = vecAdd(camera, vecMult(vecNormalize(rightVec), (cameraMoveVel * dt)))
    #if pressed[pygame.K_a]:
    #    camera = vecAdd(camera, vecMult(vecNormalize(rightVec), -(cameraMoveVel * dt)))
    #if pressed[pygame.K_SPACE]:
    #    camera = vecAdd(camera, vecMult(vecNormalize(upVec), (cameraMoveVel * dt)))
    #if pressed[pygame.K_LSHIFT]:
    #    camera = vecAdd(camera, vecMult(vecNormalize(upVec), -(cameraMoveVel * dt)))
    #rotation
    #if pressed[pygame.K_LEFT]:
    #    yaw -= cameraRotateVel * dt
    #if pressed[pygame.K_RIGHT]:
    #    yaw += cameraRotateVel * dt

    triToRaster = []
    

    #make basic matricies
    matRotX = makeXRotMatrix(0)
    matRotY = makeYRotMatrix(0)
    matRotZ = makeZRotMatrix(0)
    matTrans = makeTranslationMatrix([0, 0, 5])
    matProj = makeProjMatrix(fov, (screen.get_height() / screen.get_width()), 0.1, 1000)
        
    #create world matrix
    matWorld = makeIdentityMatrix()
    matWorld = matrixMultMatrix(matRotZ, matRotX)
    #matWorld = matrixMultMatrix(matWorld, matRotY)
    matWorld = matrixMultMatrix(matWorld, matTrans)

    for tri in mesh:
        #clear vectors
        triProjected = [0, 0, 0, 1]
        triTransformed = [0, 0, 0, 1]
        triViewed = [0, 0, 0, 1]

        #world matrix transform
        triTransformed[0] = vecMultMatrix(matWorld, tri[0])
        triTransformed[1] = vecMultMatrix(matWorld, tri[1])
        triTransformed[2] = vecMultMatrix(matWorld, tri[2])

        #calculate tri normal
        normal = [0, 0, 0, 1]
        line1 = [0, 0, 0, 1]
        line2 = [0, 0, 0, 1]

        #calculate sides of triangle
        line1 = vecSub(triTransformed[1], triTransformed[0])
        line2 = vecSub(triTransformed[2], triTransformed[0])

        #cross product of lines to get normal of triangle
        normal = vecCrossProduct(line1, line2)

        #normalize the normal
        normal = vecNormalize(normal)

        #get ray from triangle to camera
        cameraRay = vecSub(triTransformed[0], camera)

        #if ray is aligned with normal the triangle is visible
        if vecDotProduct(normal, cameraRay) < 0:
            #illumination
            lightDirection = [0, 1, -1]
            lightDirection = vecNormalize(lightDirection)

            #how aligned the lightDirection and normal
            dp = max(0.1, vecDotProduct(lightDirection, normal))

            #set color
            color = [dp, dp, dp]

            #convert world space to view space
            triViewed[0] = vecMultMatrix(matView, triTransformed[0])
            triViewed[1] = vecMultMatrix(matView, triTransformed[1])
            triViewed[2] = vecMultMatrix(matView, triTransformed[2])

            #clip viewed triangles angainst near plane
            clippedTriangles = 0
            clipResults = triClipAgainstPlane([0, 0, 0.1], [0, 0, 1], triViewed)

            #loop over all triangles since some might have been created during clipping
            for n in range(0, clipResults[0]):

                #project tris
                triProjected[0] = vecMultMatrix(matProj, clipResults[n+1][0])
                triProjected[1] = vecMultMatrix(matProj, clipResults[n+1][1])
                triProjected[2] = vecMultMatrix(matProj, clipResults[n+1][2])

                #scale into view
                triProjected[0] = vecDiv(triProjected[0], triProjected[0][3])
                triProjected[1] = vecDiv(triProjected[1], triProjected[1][3])                
                triProjected[2] = vecDiv(triProjected[2], triProjected[2][3])

                #invert x and y
                triProjected[0][0] *= 1
                triProjected[1][0] *= 1
                triProjected[2][0] *= 1
                triProjected[0][1] *= 1
                triProjected[1][1] *= 1
                triProjected[2][1] *= 1

                #offset view
                offsetView = [1, 1, 0]
                triProjected[0] = vecAdd(triProjected[0], offsetView)
                triProjected[1] = vecAdd(triProjected[1], offsetView)
                triProjected[2] = vecAdd(triProjected[2], offsetView)
                triProjected[0][0] *= 0.5 * screen.get_width()
                triProjected[0][1] *= 0.5 * screen.get_height()
                triProjected[1][0] *= 0.5 * screen.get_width()
                triProjected[1][1] *= 0.5 * screen.get_height()
                triProjected[2][0] *= 0.5 * screen.get_width()
                triProjected[2][1] *= 0.5 * screen.get_height()

                #add tri to list for sorting
                triToRaster.append([triProjected, color])

    
    triToRaster.sort(key=sortByAverageZ)
    
    for tri in triToRaster:
        #queue for generated triangles
        listTriangles = []

        #add inital triangle
        listTriangles.append(tri)
        newTriangles = 1

        for p in range(0, 4):
            clipResults = []
            while newTriangles > 0:
                #grab triangle from front of queue
                test = listTriangles.pop(0)
                newTriangles -= 1
                print(test)

                #clip tri against a plane.
                match p:
                    case 0:
                        clipResults = triClipAgainstPlane([0, 0, 0], [0, 0, 0], test[0])
                    case 1:
                        clipResults = triClipAgainstPlane([0, screen.get_height() - 1, 0], [0, -1, 0], test)
                    case 2:
                        clipResults = triClipAgainstPlane([0, 0, 0], [1, 0, 0], test)
                    case 3:
                        clipResults = triClipAgainstPlane([screen.get_width() - 1, 0, 0], [-1, 0, 0], test)

                for i in range(0, clipResults[0]):
                    listTriangles.append(clipResults[i+1])
            newTriangles = len(listTriangles)
        
    
    for tri in listTriangles:
        #print(((tri[0][0], tri[0][1]), (tri[1][0], tri[1][1]), (tri[2][0], tri[2][1])))
        pygame.draw.polygon(screen, "white", ((tri[0][0], tri[0][1]), (tri[1][0], tri[1][1]), (tri[2][0], tri[2][1])))

    pygame.display.flip()

pygame.quit()