import pygame
import random
import math
from commonalien import *
from constants import *
class SpaceCentipede(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, space, colour=(255,255,255)):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.body.position))
        self.enemy_colour = colour
        self.rect.center = (int(self.body.position.x), int(self.body.position.y))
        pygame.draw.circle(self.image, (self.enemy_colour), (self.radius, self.radius), self.radius, width=2)
        self.space = space
        self.shape.friction = 9.0
        self.shape.elasticity = 0.2
        self.shape.collision_type = 5
        self.shape.mass = 100 * self.radius
        self.shape.game_object = self
        self.time_to_live = ALIEN_TTL
        self.damage_accumulated = 0
        self.split_threshold = 10 * self.radius
    
    def draw(self):
        pass

    def bounds_check(self):
        if self.body.position.x > GAME_WIDTH or self.body.position.x < 0 or self.body.position.y > GAME_HEIGHT or self.body.position.y < 0:
            return True
    def update(self, dt):
        self.time_to_live -= dt 
        if self.time_to_live <= dt and self.bounds_check() == True:
            self.kill()
            self.space.remove(self.body, self.shape)
        self.rect.center = (int(self.body.position.x), int(self.body.position.y))
