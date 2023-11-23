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

def triClipAgainstPlane(plane_p, plane_n, in_tri):
    #define global variable
    global clipped
    from main import clipped

    # Make sure plane normal is indeed normal
    plane_n = vecNormalize(plane_n)

    # Return signed shortest distance from point to plane, plane normal must be normalised
    def dist(p):
        n = vecNormalize(p)
        return (plane_n.x * n.x + plane_n.x * n.x + plane_n.x * n.x - vecDotProduct(plane_n, plane_p))
        
	# Create two temporary storage arrays to classify points either side of plane
    # If distance sign is positive, point lies on "inside" of plane
    inside_points = triangle()
    nInsidePointCount = 0
    outside_points = triangle()
    nOutsidePointCount = 0
    
    # Get signed distance of each point in triangle to plane
    d0 = dist(in_tri.v1)
    d1 = dist(in_tri.v2)
    d2 = dist(in_tri.v3)
    

    if (d0 >= 0):
        inside_points[nInsidePointCount] = in_tri.v1
        nInsidePointCount += 1
    else:
        outside_points[nOutsidePointCount] = in_tri.v1
        nOutsidePointCount += 1
    if (d1 >= 0):
        inside_points[nInsidePointCount] = in_tri.v2
        nInsidePointCount += 1
    else:
        outside_points[nOutsidePointCount] = in_tri.v2
        nOutsidePointCount += 1
    if (d2 >= 0):
        inside_points[nInsidePointCount] = in_tri.v3
        nInsidePointCount += 1
    else:
        outside_points[nOutsidePointCount] = in_tri.v3
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
        clipped[0] = in_tri
        return 1 # Just the one returned original triangle is valid   

    if (nInsidePointCount == 1 and nOutsidePointCount == 2):
		# Triangle should be clipped. As two points lie outside the plane, the triangle simply becomes a smaller triangle

		# The inside point is valid, so keep that...
        clipped[0].v1 = inside_points[0]
        
		# but the two new points are at the locations where the 
		# original sides of the triangle (lines) intersect with the plane
        clipped[0].v2 = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        clipped[0].v3 = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[1])
        
        return 1 # Return the newly formed single triangle


    if (nInsidePointCount == 2 and nOutsidePointCount == 1):
		# Triangle should be clipped. As two points lie inside the plane, the clipped triangle becomes a "quad".
        
		# The first triangle consists of the two inside points and a new point determined by the location where one side of the triangle intersects with the plane
        clipped[0].x = inside_points[0]
        clipped[0].y = inside_points[1]
        clipped[0].z = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        
		# The second triangle is composed of one of he inside points, a
		# new point determined by the intersection of the other side of the 
		# triangle and the plane, and the newly created point above
        clipped[1][0] = inside_points[1]
        clipped[1][1] = clipped[0][2]
        clipped[1][2] = vecIntersectPlane(plane_p, plane_n, inside_points[1], outside_points[0])
        
        return 2 # Return two newly formed triangles which form a quad

def testClip(plane_p, plane_n, in_tri):
    global clipped
    from main import clipped
    plane_n = vecNormalize(plane_n)

    outsidePointCount = 0
    insidePointCount = 0

    inside_points = triangle()
    outside_points = triangle()
    

    if vecDotProduct((vecSub(in_tri[0], plane_p)), plane_n) <= 0:
        inside_points[insidePointCount] = in_tri.v1
        insidePointCount += 1
    else:
        outside_points[outsidePointCount] = in_tri.v1
        outsidePointCount += 1
    if vecDotProduct((vecSub(in_tri[1], plane_p)), plane_n) <= 0:
        inside_points[insidePointCount] = in_tri.v2
        insidePointCount += 1
    else:
        outside_points[outsidePointCount] = in_tri.v2
        outsidePointCount += 1
    if vecDotProduct((vecSub(in_tri[2], plane_p)), plane_n) <= 0:
        inside_points[insidePointCount] = in_tri.v3
        insidePointCount += 1
    else:
        outside_points[outsidePointCount] = in_tri.v3
        outsidePointCount += 1

    # Now classify triangle points, and break the input triangle into 
	# smaller output triangles if required. There are four possible
	# outcomes...
    if (insidePointCount == 0):
		# All points lie on the outside of plane, so clip whole triangle
		# It ceases to exist
        return 0 # No returned triangles are valid

    if (insidePointCount == 3):
		# All points lie on the inside of plane, so do nothing
		# and allow the triangle to simply pass through
        clipped[0] = in_tri
        return 1 # Just the one returned original triangle is valid   

    if (insidePointCount == 1 and outsidePointCount == 2):
		# Triangle should be clipped. As two points lie outside the plane, the triangle simply becomes a smaller triangle

		# The inside point is valid, so keep that...
        clipped[0].v1 = inside_points[0]
        
		# but the two new points are at the locations where the 
		# original sides of the triangle (lines) intersect with the plane
        clipped[0].v2 = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        clipped[0].v3 = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[1])
        
        return 1 # Return the newly formed single triangle


    if (insidePointCount == 2 and outsidePointCount == 1):
		# Triangle should be clipped. As two points lie inside the plane, the clipped triangle becomes a "quad".
        
		# The first triangle consists of the two inside points and a new point determined by the location where one side of the triangle intersects with the plane
        clipped[0].x = inside_points[0]
        clipped[0].y = inside_points[1]
        clipped[0].z = vecIntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        
		# The second triangle is composed of one of he inside points, a
		# new point determined by the intersection of the other side of the 
		# triangle and the plane, and the newly created point above
        clipped[1][0] = inside_points[1]
        clipped[1][1] = clipped[0][2]
        clipped[1][2] = vecIntersectPlane(plane_p, plane_n, inside_points[1], outside_points[0])
        
        return 2 # Return two newly formed triangles which form a quad
    