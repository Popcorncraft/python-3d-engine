from operationFunctions import *

def createMeshFromOBJ(path):
    file = open(path)
    vectors = []
    tris = []
    for line in file:
        if line[0] == "v":
            line = line.split()
            vectors.append(vec3d(float(line[1]), float(line[2]), float(line[3]), 1))
        elif line[0] == "f":
            line = line.split()
            tris.append([vectors[int(line[1])-1], vectors[int(line[2])-1], vectors[int(line[3])-1]])
    return(tris)

def sortByAverageZ(tri):
    return((tri[0][2] + tri[1][2] + tri[2][2]) / 3)

def vecIntersectPlane(planeP, planeN, lineStart, lineEnd):
    planeN = vecNormalize(planeN)
    planeD = -vecDotProduct(planeN, planeP)
    ad = vecDotProduct(lineStart, planeN)
    bd = vecDotProduct(lineEnd, planeN)
    t = (-planeD - ad) / (bd - ad)
    lineStartToEnd = vecSub(lineEnd, lineStart)
    lineToIntersect = vecMul(lineStartToEnd, t)
    return(vecAdd(lineStart, lineToIntersect))

def testClip(plane_p, plane_n, in_tri):
    plane_n = vecNormalize(plane_n)

    outsidePointCount = 0
    insidePointCount = 0
    inside_points = triangle()
    outside_points = triangle()
    out_tri1 = triangle()
    out_tri2 = triangle()
    

    if vecDotProduct(vecNormalize(vecSub(in_tri[0], plane_p)), plane_n) <= 0:
        inside_points[insidePointCount] = in_tri.v1
        insidePointCount += 1
    else:
        outside_points[outsidePointCount] = in_tri.v1
        outsidePointCount += 1
    if vecDotProduct(vecNormalize(vecSub(in_tri[1], plane_p)), plane_n) <= 0:
        inside_points[insidePointCount] = in_tri.v2
        insidePointCount += 1
    else:
        outside_points[outsidePointCount] = in_tri.v2
        outsidePointCount += 1
    if vecDotProduct(vecNormalize(vecSub(in_tri[2], plane_p)), plane_n) <= 0:
        inside_points[insidePointCount] = in_tri.v3
        insidePointCount += 1
    else:
        outside_points[outsidePointCount] = in_tri.v3
        outsidePointCount += 1

    if (insidePointCount == 0):
        return 0, None, None # No returned triangles are valid

    if (insidePointCount == 3):
        return 1, in_tri, None # Just the one returned original triangle is valid   

    if (insidePointCount == 1 and outsidePointCount == 2):
        out_tri1.v1 = inside_points[0]
        
        out_tri1.v2 = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        out_tri1.v3 = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[1])
        
        return 1, out_tri1, None # Return the newly formed single triangle

    if (insidePointCount == 2 and outsidePointCount == 1):
		# The first triangle consists of the two inside points and a new point determined by the location where one side of the triangle intersects with the plane
        out_tri1.v1 = inside_points[0]
        out_tri1.v2 = inside_points[1]
        out_tri1.v3 = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        
		# The second triangle is composed of one of he inside points, a new point determined by the intersection of the other side of the triangle and the plane, and the newly created point above
        out_tri2.v1 = inside_points[1]
        out_tri2.v2 = out_tri1[2]
        out_tri2.v3 = vecIntersectPlane(plane_p, plane_n, inside_points[1], outside_points[0])
        
        return 2, out_tri1, out_tri2 # Return two newly formed triangles which form a quad
    