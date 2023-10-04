import math
import pygame

pygame.init()

#init variables
fov = 90
viewNear = 0.1
viewFar = 1000
fovRad = 1 / math.tan(fov * 0.5 / 180 * math.pi)
aspectRatio = aspectRatio = 720 / 1280
theta = 0
output = [0, 0, 0]
triRotatedZ = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
triRotatedZX = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
triTranslated = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
triProjected = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
test = 1

#██████  ███████  █████  ██████       ██   ██ ███████ ██████  ███████ 
#██   ██ ██      ██   ██ ██   ██      ██   ██ ██      ██   ██ ██      
#██████  █████   ███████ ██   ██      ███████ █████   ██████  █████   
#██   ██ ██      ██   ██ ██   ██      ██   ██ ██      ██   ██ ██      
#██   ██ ███████ ██   ██ ██████       ██   ██ ███████ ██   ██ ███████ 
#
#This is not my actual project file. This just has all the stuff necescary for the part that is acting up to work.
# The problem is down a the bottom of this page with more details down there.

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
    output[0] = input[0] * matrix[0][0] + input[1] * matrix[1][0] + input[2] * matrix[2][0] + matrix[3][0]
    output[1] = input[0] * matrix[0][1] + input[1] * matrix[1][1] + input[2] * matrix[2][1] + matrix[3][1]
    output[2] = input[0] * matrix[0][2] + input[1] * matrix[1][2] + input[2] * matrix[2][2] + matrix[3][2]
    w = input[0] * matrix[0][3] + input[1] * matrix[1][3] + input[2] * matrix[2][3] + matrix[3][3]

    if w != 0:
        output[0] /= w
        output[1] /= w
        output[2] /= w
    return(output)
    
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

#for tri in meshCube:

#hotfix to get rid of loop
tri = [[0, 0, 0],[0, 1, 0],[1, 1, 0]]

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
triTranslated[0][2] = triRotatedZX[0][2] + 10
triTranslated[1][2] = triRotatedZX[1][2] + 10
triTranslated[2][2] = triRotatedZX[2][2] + 10

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

#This will return a value of ~3 as it should          <<<<<<<
print(triProjected[0][0])

triProjected[0][0] *= 0.5 * 1280
triProjected[0][1] *= 0.5 * 720
triProjected[1][0] *= 0.5 * 1280
triProjected[1][1] *= 0.5 * 720
triProjected[2][0] *= 0.5 * 1280
triProjected[2][1] *= 0.5 * 720

#This should return a x and y value on the screen but is instead returning a value ~79,000,000      <<<<<<
print(triProjected[0][0])
