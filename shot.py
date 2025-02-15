import pygame
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, space):
        super().__init__(x, y, SHOT_RADIUS, mass=0.1)
        
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect()
        self.space = space
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.time_to_live = 1
    def draw(self):
        #self.image.fill((0,0,0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        pass
    def update(self, dt):
        #self.position = pygame.Vector2(self.body.position.x, self.body.position.y)
        #self.position += (self.velocity * dt)
        #self.rect.center = (int(self.body.position.x), int(self.body.position.y))
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        else:
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))
