from commonalien import *
from enemy_shot import EnemyShot
from constants import * 
import math
import pygame   
import pymunk.pygame_util
from raycast import RayCast
class FlyingSaucer(CommonAlien):
    def __init__(self, x, y, radius, updatable, drawable, space, canvas, colour=(0,0,0)):

        super().__init__(x , y, radius, space, colour)
        ##debug     
        self.canvas = canvas
        ## 
        self.rotation = 0
        self.updatable = updatable
        self.drawable = drawable    
        self.shape.friction = 9.0
        self.shape.elasticity = 0.6
        self.shape.collision_type = 5
        self.shape.mass = 40 * self.radius
        self.max_view_distance = 150
        self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter, self.radius)
        #add diagonal directions as well
        self.timer = 0

    def draw(self):
        result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        #for res in result:
        #if hasattr(result, "point"):
            #if result.point != None:
        if hasattr(result, "shape") and hasattr(result.shape, "game_object"):
            if result.shape.game_object.__class__.__name__ == "Player":
                x , y = result.point
                if x != 0 or y != 0:
                    towards = True
                    self.rotate(x, y, towards)
                    self.shoot(x, y)
            else:
                x , y = result.point 
                if x != 0 or y != 0:
                    self.rotate(x , y)
                    self.move()
        #pass
    def rotate(self, x, y, towards=False):
        if towards == True:
            direction = (pymunk.Vec2d(x, y) - self.body.position).angle
            self.body.angle = direction 
        else:
            direction = (pymunk.Vec2d(x , y) - self.body.position).angle
            self.body.angle = (direction - math.pi)
    def move(self):
        if self.body.velocity.length < (PLAYER_SPEED / 2):
            forward = pymunk.Vec2d(1, 0).rotated(self.body.angle)
            acceleration = forward * (ACCELERATION * .002)
            accel = pymunk.Vec2d(acceleration.x, acceleration.y)
            self.body.velocity += accel
        else:
            self.body.velocity *= DRAG_COEFFICENT

    def shoot(self, x, y):
        if self.timer <= 0:
            print(f"shooting{x}{y}")
            shot = EnemyShot(self.body.position.x, self.body.position.y, self.space)
            self.updatable.add(shot)
            self.drawable.add(shot)
            shot.body.velocity = pymunk.Vec2d(1,0).rotated(self.body.angle) * 300
            self.space.add(shot.body, shot.shape)
            self.timer = PLAYER_SHOOT_COOLDOWN * 2
    def shoot_timer(self, dt):
        if self.timer > 0:
            self.timer -= dt    
    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
        self.shoot_timer(dt)
