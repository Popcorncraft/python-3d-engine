import math
from variableClasses import *

def addVec(v1, v2):
    return([v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]])

def subVec(v1, v2):
    return([v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]])

def multVec(v, k):
    return([v[0] * k, v[1] * k, v[2] * k])

def divVec(v, k):
    return([v[0] / k, v[1] / k, v[2] / k])

def dotProduct(v1, v2):
    return(v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2])

def vecLength(v):
    return(math.sqrt(dotProduct(v, v)))

def normalizeVector(v):
    l = vecLength(v)
    return([v[0] / l, v[1] / l, v[2] / l])

def crossProduct(v1, v2):
    v = [0, 0, 0, 1]
    v[0] = v1[1] * v2[2] - v1[2] * v2[1]
    v[1] = v1[2] * v2[0] - v1[0] * v2[2]
    v[2] = v1[0] * v2[1] - v1[1] * v2[0]
    return(v)

