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
    return((tri[0][2] + tri[1][2] + tri[2][2]) / 3)
