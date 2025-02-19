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
        self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter)
         
    def draw(self):
        result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        if result != None:
            x , y = result  
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
