import pygame
import pymunk
from circleshape import *
from constants import *

#figure out how to apply collision handler for this in level1 class
class Bomb:
    def __init__(self, radius):
        self.radius = radius    
    def explode(self, x, y, space):
        explosion_check = space.point_query((x, y), 2*self.radius, pymunk.ShapeFilter(categories=PLAYER_CATEGORY,mask=PLAYER_MASK))
        explosion_center = (x , y)
        explosion_force = 7000000 # huge number but it works lol!
        for obj in explosion_check:
            if obj.distance:
                shape = obj.shape   
                body = shape.body


                direction = obj.point - explosion_center
                distance = direction.length 

                if distance == 0:
                    distance = 0.001  

                direction = direction.normalized()
                
                falloff = distance / (2*self.radius)
                
                impulse_magnitude = explosion_force * (falloff)
                impulse_vector = direction * impulse_magnitude
                body.apply_impulse_at_world_point(impulse_vector, obj.point)
    #def update(self, dt):
        #pass

