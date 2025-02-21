import pygame
import pymunk
import random
import math
from circleshape import *
from constants import *
class CommonAlien(CircleShape):
    def __init__(self, x, y, radius, space, colour=(0,0,0)):
        super().__init__(x , y, radius)
        
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.body.position))
        self.enemy_colour = colour
        self.rect.center = (int(self.body.position.x), int(self.body.position.y))
        pygame.draw.circle(self.image, (self.enemy_colour), (self.radius, self.radius), self.radius, width=2)
        self.space = space
        self.shape.filter = pymunk.ShapeFilter(categories=ENEMY_CATEGORY, mask=ENEMY_MASK)

        #self.shape.friction = 9.0
        #self.shape.elasticity = 0.2
        #self.health = 1000
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
        if hasattr(self, "body"):
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))
        self.time_to_live -= dt 
        if self.time_to_live <= dt and self.bounds_check() == True:
            if hasattr(self, "joints"):
                for joint in joints:
                    self.space.remove(joint.body, joint.shape)
            if hasattr(self, "rotation_limit_list"):
                for rotation in rotation_limit_list:
                    self.space.remove(rotation.body, rotation.shape)
            self.kill()
            self.space.remove(self.body, self.shape)
        #self.rect.center = (int(self.body.position.x), int(self.body.position.y))
