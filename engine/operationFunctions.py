import math

#Vector Operations
def vecAdd(v1, v2):
    return([v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]])

def vecSub(v1, v2):
    return([v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]])

def vecMult(v, k):
    return([v[0] * k, v[1] * k, v[2] * k])

def vecdiv(v, k):
    return([v[0] / k, v[1] / k, v[2] / k])

def vecDotProduct(v1, v2):
    return(v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2])

def vecLength(v):
    return(math.sqrt(vecDotProduct(v, v)))

def vecNormalize(v):
    l = vecLength(v)
    if l == 0:
        l = 1
    return([v[0] / l, v[1] / l, v[2] / l])

def vecCrossProduct(v1, v2):
    v = [0, 0, 0, 1]
    v[0] = v1[1] * v2[2] - v1[2] * v2[1]
    v[1] = v1[2] * v2[0] - v1[0] * v2[2]
    v[2] = v1[0] * v2[1] - v1[1] * v2[0]
    return(v)

#Matrix Operations
def vecMultMatrix(m, v):
    o = [0, 0, 0, 1]
    o[0] = v[0] * m[0][0] + v[1] * m[1][0] + v[2] * m[2][0] + v[3] * m[3][0]
    o[1] = v[0] * m[0][1] + v[1] * m[1][1] + v[2] * m[2][1] + v[3] * m[3][1]
    o[2] = v[0] * m[0][2] + v[1] * m[1][2] + v[2] * m[2][2] + v[3] * m[3][2]
    o[3] = v[0] * m[0][3] + v[1] * m[1][3] + v[2] * m[2][3] + v[3] * m[3][3]
    return(o)

def matrixMultMatrix(m1, m2):
    matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for c in range(0, 4):
        for r in range(0, 4):
            matrix[r][c] = m1[r][0] * m2[0][c] + m1[r][1] * m2[1][c] + m1[r][2] * m2[2][c] + m1[r][3] * m2[3][c]
    return(matrix)