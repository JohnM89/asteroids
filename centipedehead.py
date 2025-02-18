import pygame   
import pymunk   
#import pymunk.constraints as pc
from commonalien import *
from centipedebody import *
class CentipedeHead(CommonAlien):
    def __init__(self, x, y, radius, space, colour=(0,0,0)):
        super().__init__(x , y, radius, space, colour)
        self.radius = self.radius
        self.shape.friction = 7.0
        self.shape.elasticity = 0.6
        self.shape.collision_type = 5
        self.shape.mass = 40 * self.radius
        #self.shape.filter = pymunk.ShapeFilter(group=1)
        
    def draw(self):
        pass        
    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
