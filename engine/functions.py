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

def triClipAgainstPlane(plane_p, plane_n, in_tri, out_tri1, out_tri2):
    # Make sure plane normal is indeed normal
    plane_n = vecNormalize(plane_n)

    # Return signed shortest distance from point to plane, plane normal must be normalised
    def dist(p):
        n = vecNormalize(p)
        return (plane_n[0] * p[0] + plane_n[1] * p[1] + plane_n[2] * p[2] - vecDotProduct(plane_n, plane_p))
        
	# Create two temporary storage arrays to classify points either side of plane
    # If distance sign is positive, point lies on "inside" of plane
    inside_points = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    nInsidePointCount = 0
    outside_points = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
    nOutsidePointCount = 0
    
    # Get signed distance of each point in triangle to plane
    d0 = dist(in_tri[0])
    d1 = dist(in_tri[1])
    d2 = dist(in_tri[2])
    

    if (d0 >= 0):
        inside_points[nInsidePointCount] = in_tri[0] 
        nInsidePointCount += 1
    else:
        outside_points[nOutsidePointCount] = in_tri[0] 
        nOutsidePointCount += 1
    if (d1 >= 0):
        inside_points[nInsidePointCount] = in_tri[1] 
        nInsidePointCount += 1
    else:
        outside_points[nOutsidePointCount] = in_tri[1] 
        nOutsidePointCount += 1
    if (d2 >= 0):
        inside_points[nInsidePointCount] = in_tri[2] 
        nInsidePointCount += 1
    else:
        outside_points[nOutsidePointCount] = in_tri[2] 
        nOutsidePointCount += 1
    
	# Now classify triangle points, and break the input triangle into 
	# smaller output triangles if required. There are four possible
	# outcomes...
    if (nInsidePointCount == 0):
		# All points lie on the outside of plane, so clip whole triangle
		# It ceases to exist
        return 0 # No returned triangles are valid

    if (nInsidePointCount == 3):
		# All points lie on the inside of plane, so do nothing
		# and allow the triangle to simply pass through
        out_tri1 = in_tri
        return 1 # Just the one returned original triangle is valid   

    if (nInsidePointCount == 1 and nOutsidePointCount == 2):
		# Triangle should be clipped. As two points lie outside the plane, the triangle simply becomes a smaller triangle

		# The inside point is valid, so keep that...
        out_tri1.p[0] = inside_points[0]
        
		# but the two new points are at the locations where the 
		# original sides of the triangle (lines) intersect with the plane
        out_tri1.p[1] = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        out_tri1.p[2] = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[1])
        
        return 1 # Return the newly formed single triangle


    if (nInsidePointCount == 2 and nOutsidePointCount == 1):
		# Triangle should be clipped. As two points lie inside the plane, the clipped triangle becomes a "quad".
        
		# The first triangle consists of the two inside points and a new point determined by the location where one side of the triangle intersects with the plane
        out_tri1[0] = inside_points[0]
        out_tri1[1] = inside_points[1]
        out_tri1[2] = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        
		# The second triangle is composed of one of he inside points, a
		# new point determined by the intersection of the other side of the 
		# triangle and the plane, and the newly created point above
        out_tri2[0] = inside_points[1]
        out_tri2[1] = out_tri1[2]
        out_tri2[2] = vecIntersectPlane(plane_p, plane_n, inside_points[1], outside_points[0])
        
        return 2 # Return two newly formed triangles which form a quad

