from commonalien import *
import math
import pymunk.pygame_util
class FlyingSaucer(CommonAlien):
    def __init__(self, x, y, radius, space, colour=(0,0,0)):
        super().__init__(x , y, radius, space, colour)
        
        self.shape.friction = 9.0
        self.shape.elasticity = 0.6
        self.shape.collision_type = 5
        self.shape.mass = 40 * self.radius
        self.max_view_distance = 10
        self.shape.filter = pymunk.ShapeFilter(group=1)
        self.directions = [(1,0), (-1, 0), (0, 1), (0, -1)]
        #add diagonal directions as well
    def draw(self):
        pass
    def cast_ray(self):
        for direction in self.directions:
            #length = math.hypot(direction[0], direction[1])
            #if length == 0:
            #    return  
            dir_x = direction[0] #/ length
            dir_y = direction[1] #/ length
            end = ( self.body.position.x + dir_x * self.max_view_distance, self.body.position.y + dir_y * self.max_view_distance)
            result = self.space.segment_query_first((self.body.position.x, self.body.position.y), end, radius=0, shape_filter=self.shape.filter)
            if result != None:
                print(f"seen{result.shape}")
    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
        self.cast_ray()
