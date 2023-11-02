import math
from variableClasses import *
from vectorFunctions import *

def createMeshFromOBJ(path):
    file = open(path)
    vectors = [[0, 0, 0, 1]]
    mesh = []
    for line in file:
        if line[0] == "v":
            tempLine = line.split()
            tempVector = [0, 0, 0, 1]
            tempVector[0] = float(tempLine[1])
            tempVector[1] = float(tempLine[2])
            tempVector[2] = float(tempLine[3])
            vectors.append(tempVector)
        elif line[0] == "f":
            tempLine = line.split()
            tempTri = [0.0, 0.0, 0.0]
            tempTri[0] = vectors[int(tempLine[1])]
            tempTri[1] = vectors[int(tempLine[2])]
            tempTri[2] = vectors[int(tempLine[3])]
            mesh.append(tempTri)
    return(mesh)

def sortByAverageZ(tri):
    sum = tri[0][2] + tri[1][2] + tri[2][2]
    average = sum / 3
    return(average)