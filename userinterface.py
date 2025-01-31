import pygame
from squareshape import *
from constants import *
class UserInterface(SquareShape):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
    def draw(self, screen):
        #ui box, will hold score, lives and powerups etc...
        pygame.draw.rect(screen, (255, 255, 255), self.rect, width=2, border_radius=2)

    def update(self, dt):
        pass 
