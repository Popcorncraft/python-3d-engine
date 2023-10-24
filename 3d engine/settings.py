import math
import pygame
from debugAssets import *

#settings
fov = 90
viewNear = 0.1
viewFar = 1000
screenWidth = 1280
screenHeight = 720
cameraPos = [0, 0, 0]
cameraRot = [0, 0, 0]
lightingDirection = [0, 0, -360]