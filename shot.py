import pygame
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
       
    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255), self.position, self.radius, width=2)
    
    def update(self, dt):
        self.position += (self.velocity * dt)
