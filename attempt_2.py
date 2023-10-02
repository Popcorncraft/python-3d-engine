import pygame
import math
import numpy as np

#pygame setup
pygame.init()
pygame.font.init
pygame.display.set_caption('3d Renderer')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#3D vector variable type
class vec3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

#2D vector variable type
class vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

