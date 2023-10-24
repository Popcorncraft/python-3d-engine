import math

matProj = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]

matRotZ = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]

matRotX = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]

def updateMatricies():
    from main import (aspectRatio, fovRad, viewFar, viewNear, theta)
    matProj = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]
    matProj[0][0] = aspectRatio * fovRad
    matProj[1][1] = fovRad
    matProj[2][2] = viewFar / (viewFar - viewNear)
    matProj[3][2] = (-viewFar * viewNear) / (viewFar - viewNear)
    matProj[2][3] = 1.0
    matProj[3][3] = 0.0

    matRotZ = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]
    matRotZ[0][0] = math.cos(theta)
    matRotZ[0][1] = math.sin(theta)
    matRotZ[1][0] = -math.sin(theta)
    matRotZ[1][1] = math.cos(theta)
    matRotZ[2][2] = 1
    matRotZ[3][3] = 1

    matRotX = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]
    matRotX[0][0] = 1
    matRotX[1][1] = math.cos(theta * 0.5)
    matRotX[1][2] = math.sin(theta * 0.5)
    matRotX[2][1] = -math.sin(theta * 0.5)
    matRotX[2][2] = math.cos(theta * 0.5)
    matRotX[3][3] = 1

updateMatricies()