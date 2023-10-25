import math
from variableClasses import *
from vectorFunctions import *

def calculateNormal(input):
    
    output = [0, 0, 0, 1]
    line1 = [0, 0, 0, 1]
    line2 = [0, 0, 0, 1]

    #calculate lines
    line1[0] = input[1][0] - input[0][0]
    line1[1] = input[1][1] - input[0][1]
    line1[2] = input[1][2] - input[0][2]
    
    line2[0] = input[2][0] - input[0][0]
    line2[1] = input[2][1] - input[0][1]
    line2[2] = input[2][2] - input[0][2]

    #cross product
    output = crossProduct(line1, line2)

    return(output)

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