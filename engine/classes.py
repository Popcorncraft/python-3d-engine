class meshObject:
    def __init__(self, id: int, path: str, postition: list, rotation: list):
        from functions import createMeshFromOBJ
        self.id = id
        self.path = path
        self.position = postition
        self.rotation = rotation
        self.mesh = createMeshFromOBJ(path)

class vec3d:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, w: float = 1):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        elif index == 3:
            return self.w
        else:
            raise IndexError("index out of range")
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        elif index == 3:
            self.w = value
        else:
            raise IndexError("index out of range")

    #operations
    def __str__(self):
        return("[x:" + str(self.x) + ", y:" + str(self.y) + ", z:" + str(self.z) + ", w:" + str(self.w) + "]")
    def __add__(v1, v2):
        return(vec3d(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z))
    def __sub__(v1, v2):
        return(vec3d(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z))
    def __mul__(v, k):
        return(vec3d(v.x * k, v.y * k, v.z * k))
    def __tridiv__(v, k):
        return(vec3d(v.x / k, v.y / k, v.z / k))

class triangle:
    def __init__(self, v1: vec3d = vec3d(), v2: vec3d = vec3d(), v3: vec3d = vec3d(), color = [0, 0, 0]):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.col = color
    def __getitem__(self, index):
        if index == 0:
            return self.v1
        elif index == 1:
            return self.v2
        elif index == 2:
            return self.v3
        elif index == 3:
            return self.col
        else:
            raise IndexError("index out of range")
    def __setitem__(self, index, value):
        if index == 0:
            self.v1 = value
        elif index == 1:
            self.v2 = value
        elif index == 2:
            self.v3 = value
        elif index == 3:
            self.col = value
        else:
            raise IndexError("index out of range")
    def __repr__(self) -> str:
        return("[v1:" + str(self.v1) + ", v2:" + str(self.v2) + ", v3:" + str(self.v3) + ", col:" + str(self.col) + "]")