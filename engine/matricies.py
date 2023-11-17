import math
from operationFunctions import *

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
    newForward = vecNormalize(vecSub(target, position))

    #calculate new up
    a = vecMult(newForward, vecDotProduct(upVec, newForward))
    newUp = vecNormalize(vecSub(upVec, a))

    #calculate new right direction
    newRight = vecCrossProduct(newUp, newForward)

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