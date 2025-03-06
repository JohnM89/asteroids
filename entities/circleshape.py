import pygame
import pymunk
import math
from game.constants import *

#base class for game objects
#extends the pygame Sprite class to also store a position, velocity and radius
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, mass=1.0):
        #check if has class variable containers
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        #set variables for CircleShape class
        #self.position = pygame.Vector2(x, y)
        #self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.mass = mass
        self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = (x, y)
        self.body.velocity = pymunk.Vec2d(0, 0)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        #self.space.add(self.body, self.shape)

    def draw(self, canvas):
             #sub class to override
        pass
    
    #rewrite for single function to return true or false & keep game logic in main.py game loop
    def collisions(self, obj):
        #distance = pygame.math.Vector2.distance_to(self.position, obj.position)
        #distance = self.body.position.get_distance(obj.body.position)
        #return distance <= (self.radius + obj.radius)
        pass
    
    def apply_gravity(self, obj2, dt):
        p1 = pymunk.Vec2d(self.body.position.x, self.body.position.y)
        p2 = pymunk.Vec2d(obj2.body.position.x, obj2.body.position.y)

        direction = p2 - p1 
        distance_sq = direction.get_length_sqrd()
        
        if distance_sq == 0:
            return
        
        force_magnitude = (GRAVITY_CONSTANT * self.mass * obj2.mass) / distance_sq
        force = direction.normalized() * force_magnitude * dt
        #force = direction.normalized() * force_magnitude

        self.body.apply_force_at_local_point(force)
        obj2.body.apply_force_at_local_point(-force)

    def update(self, dt):
        #sub class to override
        #self.position = pygame.Vector2(self.body.position.x, self.body.position.y)
        pass
