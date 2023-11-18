from operationFunctions import *

def createMeshFromOBJ(path):
    file = open(path)
    vectors = []
    tris = []
    for line in file:
        if line[0] == "v":
            line = line.split()
            vectors.append([float(line[1]), float(line[2]), float(line[3]), 1])
        elif line[0] == "f":
            line = line.split()
            tris.append([vectors[int(line[1])-1], vectors[int(line[2])-1], vectors[int(line[3])-1]])
    return(tris)

def sortByAverageZ(tri):
    return((tri[0][0][2] + tri[0][1][2] + tri[0][2][2]) / 3)

def vecIntersectPlane(planeP, planeN, lineStart, lineEnd):
    planeN = vecNormalize(planeN)
    planeD = -vecDotProduct(planeN, planeP)
    ad = vecDotProduct(lineStart, planeN)
    bd = vecDotProduct(lineEnd, planeN)
    t = (-planeD - ad) / (bd - ad)
    lineStartToEnd = vecSub(lineEnd, lineStart)
    lineToIntersect = vecMult(lineStartToEnd, t)
    return(vecAdd(lineStart, lineToIntersect))

def triClipAgainstPlane(planeP, planeN, inTri):
    #reset output values
    outTri = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    outTri2 = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]

    #Make sure plane normal is normalized
    planeN = vecNormalize(planeN)

    #return shortest distance from point to plane
    def dist(p):
        n = vecNormalize(p)
        return(planeN[0] * p[0] + planeN[1] * p[1] + planeN[2] * p[2] - vecDotProduct(planeN, planeP))
    
    #create two temporary storage arrays to classify points either side of plane
    #if distance sign in positive, point lies on "insed" of plane
    insidePoints = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    outsidePoints = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    insidePointCount = 0
    outsidePointCount = 0

    d0 = dist(inTri[0])
    d1 = dist(inTri[1])
    d2 = dist(inTri[2])

    if (d0 >= 0):
        insidePoints[insidePointCount] = inTri[0]
        insidePointCount += 1
    else:
        outsidePoints[outsidePointCount] = inTri[0]
        outsidePointCount += 1
    if (d1 >= 0):
        insidePoints[insidePointCount] = inTri[1]
        insidePointCount += 1
    else:
        outsidePoints[outsidePointCount] = inTri[1]
        outsidePointCount += 1
    if (d2 >= 0):
        insidePoints[insidePointCount] = inTri[2]
        insidePointCount += 1
    else:
        outsidePoints[outsidePointCount] = inTri[2]
        outsidePointCount += 1

    #classify triangle point and break triangle into smaller triangles if required
    if insidePointCount == 0:
        #all points lie outside of plane so clip it all
        return(0, 0)
    elif insidePointCount == 3:
        #all points lie inside of plane so no clipping
        outTri = inTri
        return(1, outTri)
    elif insidePointCount == 1 and outsidePointCount == 2:
        #triangle should be clipped
        #triangle simply becomes smaller

        #inside point
        outTri[0] = insidePoints[0]

        #outside points
        outTri[1] = vecIntersectPlane(planeP, planeN, insidePoints[0], outsidePoints[0])
        outTri[2] = vecIntersectPlane(planeP, planeN, insidePoints[0], outsidePoints[1])

        return(1, outTri)
    elif insidePointCount == 2 and outsidePointCount == 1:
        #triangle should be clipped
        #triangle becomes two smaller triangles

        #first triangle is two inside points and a new point determined by the location where one side instersects with plane
        outTri[0] = insidePoints[0]
        outTri[1] = insidePoints[1]
        outTri[2] = vecIntersectPlane(planeP, planeN, insidePoints[0], outsidePoints[0])

        #second triangle is one inside point a new point determined by the intersection of the other side of the triangle and plane and the newly created point above
        outTri2[0] = insidePoints[1]
        outTri2[1] = outTri[2]
        outTri2[2] = vecIntersectPlane(planeP, planeN, insidePoints[1], outsidePoints[0])

        return(2, outTri, outTri2)

