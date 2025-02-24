import pymunk
import pygame
import math
class RayCast:
    def __init__(self,space, canvas, max_distance=1000, shape_filter=pymunk.ShapeFilter(), radius=6, directions=[(1,0),(-1,0),(0,1),(0,-1), (0.3827, -0.9239), (0.7071, -0.7071), (0.9239, -0.3827),
    (0.9239,  0.3827), (0.7071,  0.7071), (0.3827,  0.9239),
    (-0.3827,  0.9239), (-0.7071,  0.7071), (-0.9239,  0.3827),
    (-0.9239, -0.3827), (-0.7071, -0.7071), (-0.3827, -0.9239)]):
        self.colour = (255,255,0)
        self.max_distance = max_distance
        self.shape_filter = shape_filter
        self.all_results = []
        self.radius = radius
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
            result = self.space.segment_query((pos_x, pos_y), end, radius=self.radius, shape_filter=self.shape_filter)
            if result != None:
                result.sort(key=lambda r: r.alpha)
                self.all_results.extend(result)
                for res in result:
                    if hasattr(res, "point"):
                        if hasattr(res, "shape") and hasattr(res.shape, "game_object"):
                ##debug 
                            pygame.draw.line(self.canvas, self.colour, (pos_x, pos_y), (res.point), 5)
        if self.all_results != None:
            self.all_results.sort(key=lambda r: r.alpha)
            return self.all_results
            

        return None
