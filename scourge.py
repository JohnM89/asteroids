from commonalien import *
from constants import *
import pymunk.pygame_util
import math 
import pygame   
from raycast import RayCast
class Scourge(CommonAlien):
    def __init__(self, x, y, radius, space, canvas, colour=(255,255,0)):
        super().__init__(x , y, radius, space, colour)
        self.canvas = canvas
        self.shape.friction = 9.0
        self.shape.elasticity = 0.8
        self.shape.collision_type = 5
        self.max_view_distance = 100
        self.shape.mass = 30 * self.radius
        self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter, self.radius)
    def draw(self):
        result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        if hasattr(result, "point"):    
            if result.point != None:
                if hasattr(result, "shape") and hasattr(result.shape, "game_object"):
                    if result.shape.game_object.__class__.__name__ == "Player":
                        x , y = result.point  
                        if x != 0 or y != 0:
                            towards = True
                            self.rotate(x, y, towards)
                            boost = True
                            self.move(boost)
                    else:
                        x , y = result.point
                        if x != 0 or y != 0:
                            self.rotate(x, y)
                            self.move()
    def rotate(self,x, y, towards=False):
        if towards == True:
            direction = (pymunk.Vec2d(x, y) - self.body.position).angle
            self.body.angle = direction
        else:
            direction = (pymunk.Vec2d(x, y) - self.body.position).angle
            self.body.angle = (direction + math.pi)
    def move(self, boost=False):
        forward = pymunk.Vec2d(1, 0).rotated(self.body.angle)
        if boost == True:
            if self.body.velocity.length < PLAYER_SPEED:
                acceleration = forward * ACCELERATION  
                accel = pymunk.Vec2d(acceleration.x, acceleration.y)
                self.body.velocity += accel
        else:
            if self.body.velocity.length < PLAYER_SPEED:
                acceleration = forward * (ACCELERATION * 0.002)
                accel = pymunk.Vec2d(acceleration.x, acceleration.y)
                self.body.velocity += accel
            else:
                self.body.velocity *= DRAG_COEFFICENT

    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
