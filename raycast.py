import pymunk
import pygame
import math
class RayCast:
    def __init__(self,space, canvas, max_distance=1000, shape_filter=pymunk.ShapeFilter(), directions=[(1,0),(-1,0),(0,1),(0,-1)]):
        self.colour = (255,255,0)
        self.max_distance = max_distance
        self.shape_filter = shape_filter
        self.space = space
        self.canvas = canvas
        self.directions = directions

    def cast_ray(self, pos_x, pos_y):
        for direction in self.directions:
            if len(self.directions) > 4:
                length = math.hypot(direction[0], direction[1])
                if length == 0:
                    return
                dir_x = direction[0] / length
                dir_y = direction[1] / length
            else:
                dir_x = direction[0]
                dir_y = direction[1]
            end = (pos_x + dir_x * self.max_distance, pos_y + dir_y * self.max_distance)
            result = self.space.segment_query_first((pos_x, pos_y), end, radius=0, shape_filter=self.shape_filter)
            if result != None:
                ##debug 
                pygame.draw.line(self.canvas, self.colour, (pos_x, pos_y), (result.point), 5)
                return result.point
        return None
