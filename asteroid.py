import pygame
from circleshape import *
from constants import *
#created in AsteroidField class
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x , y, radius)
    #draw as circle with white colouring
    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255), self.position, self.radius, width=2)

    def update(self, dt):
        self.position += (self.velocity * dt)

