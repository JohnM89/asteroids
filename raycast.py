import pymunk
import pygame
import math
class RayCast:
    def __init__(self, position_x, position_y, space, canvas, max_distance=1000, shape_filter=pymunk.ShapeFilter(), directions=[(1,0),(-1,0),(0,1),(0,-1)]):
        self.start_pos = (position_x, position_y)
        self.colour = (255,255,0)
        self.max_distance = max_distance
        self.shape_filter = shape_filter
        self.space = space
        self.canvas = canvas
        self.directions = directions

    def cast_ray(self):
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
            start_pos = self.start_pos
            end = (start_pos.x + dir_x * self.max_distance, start_pos.y + dir_y * self.max_distance)
            result = self.space.segment_query_first(start_pos, end, radius=0, shape_filter=self.shape_filter)
            if result != None:
                ##debug 
                pygame.draw.line(self.canvas, self.colour, start_pos, result.point, width=5)
