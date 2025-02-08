import pygame
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  # Ensure it supports alpha channel for transparency

        # Set the rect attribute based on the surface
        #self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255), self.position, self.radius, width=2)
    
    def update(self, dt):
        self.position += (self.velocity * dt)
