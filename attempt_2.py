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

#init variables
fov = 90
viewNear = 0.1
viewFar = 1000
fovRad = 1 / math.tan(fov * 0.5 / 180 * math.pi)
aspectRatio = aspectRatio = screen.get_height() / screen.get_width()
theta = 0
output = [0, 0, 0]
triRotatedZ = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
triRotatedZX = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
triTranslated = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
triProjected = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
test = 1

meshCube = [
    #south
    [[0, 0, 0],[0, 1, 0],[1, 1, 0]],
    [[0, 0, 0],[1, 1, 0],[1, 0, 0]],
    #east
    [[1, 0, 0],[1, 1, 0],[1, 1, 1]],
    [[1, 0, 0],[1, 1, 1],[1, 0, 1]],
    #north
    [[1, 0, 1],[1, 1, 1],[0, 1, 1]],
    [[1, 0, 1],[0, 1, 1],[0, 0, 1]],
    #west
    [[0, 0, 1],[0, 1, 1],[0, 1, 0]],
    [[0, 0, 1],[0, 1, 0],[0, 0, 0]],
    #top
    [[0, 1, 0],[0, 1, 1],[1, 1, 1]],
    [[0, 1, 0],[1, 1, 1],[1, 1, 0]],
    #bottom
    [[1, 0, 1],[0, 0, 1],[0, 0, 0]],
    [[1, 0, 1],[0, 0, 0],[1, 0, 0]],
    ]

#init projection matrix
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

#multiply 3D vector by 4x4 matrix
def MultiplyMatrixVector(input, matrix):
    output = [0, 0, 0]
    output[0] = input[0] * matrix[0][0] + input[1] * matrix[1][0] + input[2] * matrix[2][0] + matrix[3][0]
    output[1] = input[0] * matrix[0][1] + input[1] * matrix[1][1] + input[2] * matrix[2][1] + matrix[3][1]
    output[2] = input[0] * matrix[0][2] + input[1] * matrix[1][2] + input[2] * matrix[2][2] + matrix[3][2]
    w = input[0] * matrix[0][3] + input[1] * matrix[1][3] + input[2] * matrix[2][3] + matrix[3][3]

    if w != 0:
        output[0] /= w
        output[1] /= w
        output[2] /= w
    return(output)

#main loop
while running == True:
    #test for events
    for event in pygame.event.get():
        #quit detection
        if event.type == pygame.QUIT:
            running = False
    
    #clear screen
    screen.fill("black")

    pygame.draw.circle(screen, "white", (0, 0), 100)

    #set up rotation matricies
    theta += 1 * pygame.time.get_ticks()

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

    for tri in meshCube:

        #rotate z-axis
        triRotatedZ[0] = MultiplyMatrixVector(tri[0], matRotZ)
        triRotatedZ[1] = MultiplyMatrixVector(tri[1], matRotZ)
        triRotatedZ[2] = MultiplyMatrixVector(tri[2], matRotZ)

        #rotate x-axis
        triRotatedZX[0] = MultiplyMatrixVector(triRotatedZ[0], matRotX)
        triRotatedZX[1] = MultiplyMatrixVector(triRotatedZ[1], matRotX)
        triRotatedZX[2] = MultiplyMatrixVector(triRotatedZ[2], matRotX)

        #offset into screen
        triTranslated = triRotatedZX
        triTranslated[0][2] = triRotatedZX[0][2] + 3
        triTranslated[1][2] = triRotatedZX[1][2] + 3
        triTranslated[2][2] = triRotatedZX[2][2] + 3

        #project onto screen
        triProjected[0] = MultiplyMatrixVector(triTranslated[0], matProj)
        triProjected[1] = MultiplyMatrixVector(triTranslated[1], matProj)
        triProjected[2] = MultiplyMatrixVector(triTranslated[2], matProj)

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

        #draw wire-frame
        #pygame.draw.line(screen, "white", (triProjected[0][0], triProjected[0][1]), (triProjected[1][0], triProjected[1][1]))
        #pygame.draw.line(screen, "white", (triProjected[1][0], triProjected[1][1]), (triProjected[2][0], triProjected[2][1]))
        #pygame.draw.line(screen, "white", (triProjected[2][0], triProjected[2][1]), (triProjected[0][0], triProjected[0][1]))

    #limit framerate
    clock.tick(60)
    
            
#close window when quit
pygame.quit()