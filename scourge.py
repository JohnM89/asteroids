from commonalien import *
class Scourge(CommonAlien):
    def __init__(self, x, y, radius, space, colour=(255,255,255)):
        super().__init__(x , y, radius, space, colour)
        self.shape.friction = 9.0
        self.shape.elasticity = 0.8
        self.shape.collision_type = 6
        self.shape.mass = 10 * self.radius
    
    def draw(self):
        pass
    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
