import pygame
import pymunk
from .circleshape import *
from game.constants import *
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
                damage = max(min(impulse_magnitude * IMPACT_NORMALIZER, MAX_IMPACT_DAMAGE),MIN_IMPACT_DAMAGE)
                body.apply_impulse_at_world_point(impulse_vector, obj.point)
                if hasattr(shape.game_object, "damage_accumulated"):
                    shape.game_object.damage_accumulated += damage
                    if shape.game_object.damage_accumulated >= shape.game_object.split_threshold:
                        if hasattr(shape.game_object, "joints") and hasattr(shape.game_object, "rotation_limit_list"):
                            for joint in shape.game_object.joints:
                                if joint in space.constraints:
                                    space.remove(joint)
                            for rotation in shape.game_object.rotation_limit_list:
                                if rotation in space.constraints:
                                    space.remove(rotation)
                #self.commonenemyspawns.current_alien_count -= 1
                #contact = arbiter.contact_point_set.points[0]
                            #contact_point = obj.point
                        shape.game_object.kill()
                        space.remove(shape.body, shape)
                            #self.create_drop(contact_point.x, contact_point.y, self.space, self.updatable, self.drawable)
    #def update(self, dt):
        #pass

