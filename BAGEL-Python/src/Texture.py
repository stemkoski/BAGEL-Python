import pygame
from Rectangle import *

class Texture(object):

    def __init__(self):
        self.image = None
        self.width = 0
        self.height = 0
        
        # self.region = Rectangle()

    @staticmethod 
    def load(filename):
        tex = Texture()
        tex.image = pygame.image.load(filename)
        tex.width  = tex.image.get_width()
        tex.height = tex.image.get_height()
        return tex

    def clone(self):
        tex = Texture()
        tex.image  = self.image
        tex.width  = self.width
        tex.height = self.height
        return tex
