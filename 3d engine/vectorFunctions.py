import math
from variableClasses import *

def addVec(v1, v2):
    return(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def subVec(v1, v2):
    return(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def multVec(v, k):
    return(v.x * k, v.y * k, v.z * k)

def divVec(v, k):
    return(v.x / k, v.y / k, v.z / k)

def dotProduct(v1, v2):
    print(v1)
    return(v1.x * v2.x + v1.y * v2.y + v1.z * v2.z)

def vecLength(v):
    return(math.sqrt(dotProduct(v, v)))

def normalizeVector(v):
    l = vecLength(v)
    return(v.x / l, v.y / l, v.z / l)

def crossProduct(v1, v2):
    v = vector()
    v.x = v1.y * v2.z - v1.z * v2.y
    v.y = v1.z * v2.x - v1.x * v2.z
    v.z = v1.x * v2.y - v1.y * v2.x
    return(v)

