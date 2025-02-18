import pygame
import pymunk

class RayCast:
    def __init__(self, start_x, start_y, end_x, end_y, radius=0, shape_filter, space):
        self.x, self.y = start_x, start_y
        self.end_x, self.end_y = end_x, end_y
        self.radius = radius
        self.space = space
        #self.filter = pymunk.ShapeFilter(categories=shape_filter)
        self.filter = shape_filter

    def return_value(self):
        space.
