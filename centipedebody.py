from commonalien import *
import pymunk
class CentipedeBody(CommonAlien):
    def __init__(self, x, y, radius, space, colour=(255,255,255)):
        super().__init__(x , y, radius, space, colour)
        self.shape.friction = 7.0
        self.shape.elasticity = 0.2
        self.shape.collision_type = 5
        #self.shape.filter = pymunk.ShapeFilter()
        self.shape.mass = 5 * self.radius
    
    def draw(self):
        pass
    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
