import pygame   
import pymunk   
from constants import *
from raycast import RayCast
from commonalien import *
from centipedebody import *
class CentipedeHead(CommonAlien):
    def __init__(self, x, y, radius, space, canvas, alien_count, colour=(0,0,0)):
        super().__init__(x , y, radius, space, colour)
        self.radius = self.radius
        self.canvas = canvas
        self.shape.friction = 7.0
        self.shape.elasticity = 0.2
        self.shape.collision_type = 5
        self.shape.mass = 40 * self.radius
        self.max_view_distance = 300
        self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter)
        self.alien_count = alien_count
        #self.shape.filter = pymunk.ShapeFilter(group=2)
        
    def draw(self):
        result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        if hasattr(result, "point"):
            if result.point != None:
                if hasattr(result, "shape") and hasattr(result.shape, "game_object"):
                    if result.shape.game_object.__class__.__name__ == "FuelDrop":
                        x , y = result.point
                        if x != 0 or y != 0:
                            self.rotate(x, y)
                            self.move()       
    def rotate(self,x, y):
        direction = (pymunk.Vec2d(x, y) - self.body.position).angle
        self.body.angle = direction
    def move(self):
        forward = pymunk.Vec2d(1, 0).rotated(self.body.angle)
        if self.body.velocity.length < PLAYER_SPEED:
            acceleration = forward * ACCELERATION
            accel = pymunk.Vec2d(acceleration.x, acceleration.y)
            self.body.velocity += accel
    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
