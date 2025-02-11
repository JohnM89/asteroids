import pygame
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        
        self.image = pygame.Surface((2*self.radius, 2*self.radius))
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect()
    def draw(self):
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        #canvas.blit(self.image,self.rect)
    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rect.center = self.position
