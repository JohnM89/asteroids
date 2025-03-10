import pygame
import pymunk
from .circleshape import *
from game.constants import *

class Yamato(CircleShape):
    def __init__(self, x, y, space):
        super().__init__(x, y, SHOT_RADIUS * 2, mass=0.1)
        
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect()
        self.space = space
        self.shape.collision_type = 3
        self.shape.filter = pymunk.ShapeFilter(categories=PLAYER_BULLET_CATEGORY,mask=PLAYER_BULLET_MASK)
        self.shape.game_object = self
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.time_to_live = 7
    def draw(self):
        #self.image.fill((0,0,0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        pass
    #def charge(self, dt):


    def update(self, dt):
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        else:
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))
