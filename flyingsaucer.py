from commonalien import *
import math
import pygame   
import pymunk.pygame_util
#from raycast import RayCast
class FlyingSaucer(CommonAlien):
    def __init__(self, x, y, radius, space, canvas, colour=(0,0,0)):
        super().__init__(x , y, radius, space, colour)
        ##debug     
        self.canvas = canvas
        ##
        self.shape.friction = 9.0
        self.shape.elasticity = 0.6
        self.shape.collision_type = 5
        self.shape.mass = 40 * self.radius
        self.max_view_distance = 150
        self.shape.filter = pymunk.ShapeFilter(group=1)
        self.directions = [(1,0), (-1, 0), (0, 1), (0, -1)]
        #self.ray_cast = RayCast(self.body.position.x, self.body.position.y, self.space, self.canvas, self.max_view_distance, self.shape.filter)
        #add diagonal directions as well

    def draw(self):
        self.cast_ray()
        #self.ray_cast.cast_ray
        #pass
    def cast_ray(self):
        for direction in self.directions:
            #there is no need to normalize cardinal directions 
            #length = math.hypot(direction[0], direction[1])
            #if length == 0:
            #    return 
            start_pos = self.body.position 
            dir_x = direction[0] #/ length
            dir_y = direction[1] #/ length
            end = ( self.body.position.x + dir_x * self.max_view_distance, self.body.position.y + dir_y * self.max_view_distance)
            result = self.space.segment_query_first((self.body.position.x, self.body.position.y), end, radius=0, shape_filter=self.shape.filter)
            if result != None:
                pygame.draw.line(self.canvas, (255,255,0), (start_pos), (result.point), 5)
                #print(f"at {start_pos} seen{result.point}")
            

    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
