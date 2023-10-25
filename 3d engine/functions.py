import math
from variableClasses import *
from vectorFunctions import *

def calculateNormal(input):
    
    output = vector()
    line1 = vector()
    line2 = vector()

    #calculate lines
    line1.x = input[1].x - input[0].x
    line1.y = input[1].y - input[0].y
    line1.z = input[1].z - input[0].z
    
    line2.x = input[2].x - input[0].x
    line2.y = input[2].y - input[0].y
    line2.z = input[2].z - input[0].z

    #cross product
    output = crossProduct(line1, line2)

    return(output)

def createMeshFromOBJ(path):
    file = open(path)
    vectors = [vector()]
    mesh = []
    for line in file:
        if line[0] == "v":
            tempLine = line.split()
            tempVector = vector()
            tempVector.x = float(tempLine[1])
            tempVector.y = float(tempLine[2])
            tempVector.z = float(tempLine[3])
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
    sum = tri[0].z + tri[1].z + tri[2].z
    average = sum / 3
    return(average)