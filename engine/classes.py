from functions import createMeshFromOBJ

class meshObject:
    def __init__(self, id: int, path: str, postition: list, rotation: list):
        self.id = id
        self.path = path
        self.position = postition
        self.rotation = rotation
        self.mesh = createMeshFromOBJ(path)