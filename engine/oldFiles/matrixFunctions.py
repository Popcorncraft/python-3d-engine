import math
from vectorFunctions import *

def makeIdentityMatrix():
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matrix[0][0] = 1
    matrix[1][1] = 1
    matrix[2][2] = 1
    matrix[3][3] = 1
    return(matrix)

def makeXRotMatrix(angleRad):
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matrix[0][0] = 1
    matrix[1][1] = math.cos(angleRad)
    matrix[1][2] = math.sin(angleRad)
    matrix[2][1] = -math.sin(angleRad)
    matrix[2][2] = math.cos(angleRad)
    matrix[3][3] = 1
    return(matrix)

def makeYRotMatrix(angleRad):
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matrix[0][0] = math.cos(angleRad)
    matrix[0][2] = math.sin(angleRad)
    matrix[2][0] = -math.sin(angleRad)
    matrix[1][1] = 1
    matrix[2][2] = math.cos(angleRad)
    matrix[3][3] = 1
    return(matrix)

def makeZRotMatrix(angleRad):
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matrix[0][0] = math.cos(angleRad)
    matrix[0][1] = math.sin(angleRad)
    matrix[1][0] = -math.sin(angleRad)
    matrix[1][1] = math.cos(angleRad)
    matrix[2][2] = 1
    matrix[3][3] = 1
    return(matrix)

def makeTranslationMatrix(v = [0, 0, 0]):
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matrix[0][0] = 1
    matrix[1][1] = 1
    matrix[2][2] = 1
    matrix[3][3] = 1
    matrix[3][0] = -v[0]
    matrix[3][1] = -v[1]
    matrix[3][2] = -v[2]
    return(matrix)

def makeProjMatrix(fovDeg, aspectRatio, viewNear, viewFar):
    fovRad = 1 / math.tan(fovDeg * 0.5 / 180 * 3.14159)
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matrix[0][0] = aspectRatio * fovRad
    matrix[1][1] = fovRad
    matrix[2][2] = viewFar / (viewFar - viewNear)
    matrix[3][2] = (-viewFar * viewNear) / (viewFar - viewNear)
    matrix[2][3] = 1
    matrix[3][3] = 0
    return(matrix)

def makePointAtMatrix(position, target, upVec):
    #calculate new forward
    newForward = normalizeVector(subVec(target, position))

    #calculate new up
    a = multVec(newForward, dotProduct(upVec, newForward))
    newUp = normalizeVector(subVec(upVec, a))

    #calculate new right direction
    newRight = crossProduct(newUp, newForward)

    #set up matrix
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matrix[0][0] = newRight[0]
    matrix[0][1] = newRight[1]
    matrix[0][2] = newRight[2]
    matrix[0][3] = 0
    matrix[1][0] = newUp[0]
    matrix[1][1] = newUp[1]
    matrix[1][2] = newUp[2]
    matrix[1][3] = 0
    matrix[2][0] = newForward[0]
    matrix[2][1] = newForward[1]
    matrix[2][2] = newForward[2]
    matrix[2][3] = 0
    matrix[3][0] = position[0]
    matrix[3][1] = position[1]
    matrix[3][2] = position[2]
    matrix[3][3] = 1
    return(matrix)

def invertMatrix(m): #ONLY FOR POINT AT MATRIX
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    matrix[0][0] = m[0][0]
    matrix[0][1] = m[1][0]
    matrix[0][2] = m[2][0]
    matrix[0][3] = 0
    matrix[1][0] = m[0][1]
    matrix[1][1] = m[1][1]
    matrix[1][2] = m[2][1]
    matrix[1][3] = 0
    matrix[2][0] = m[0][2]
    matrix[2][1] = m[1][2]
    matrix[2][2] = m[2][2]
    matrix[2][3] = 0
    matrix[3][0] = -(m[3][0] * matrix[0][0] + m[3][1] * matrix[1][0] + m[3][2] * matrix[2][0])
    matrix[3][1] = -(m[3][0] * matrix[0][1] + m[3][1] * matrix[1][1] + m[3][2] * matrix[2][1])
    matrix[3][2] = -(m[3][0] * matrix[0][2] + m[3][1] * matrix[1][2] + m[3][2] * matrix[2][2])
    matrix[3][3] = 1
    return(matrix)

def matrixMultiplyVector(m, v):
    o = [0, 0, 0, 1]
    o[0] = v[0] * m[0][0] + v[1] * m[1][0] + v[2] * m[2][0] + v[3] * m[3][0]
    o[1] = v[0] * m[0][1] + v[1] * m[1][1] + v[2] * m[2][1] + v[3] * m[3][1]
    o[2] = v[0] * m[0][2] + v[1] * m[1][2] + v[2] * m[2][2] + v[3] * m[3][2]
    o[3] = v[0] * m[0][3] + v[1] * m[1][3] + v[2] * m[2][3] + v[3] * m[3][3]
    return(o)

def matrixMultiplyMatrix(m1, m2):
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for c in range(0, 4):
        for r in range(0, 4):
            matrix[r][c] = m1[r][0] * m2[0][c] + m1[r][1] * m2[1][c] + m1[r][2] * m2[2][c] + m1[r][3] * m2[3][c]
    return(matrix)