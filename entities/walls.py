import pymunk
import pygame
from game.constants import *

class Walls:
    def __init__(self, game_width, game_height, space):
        self.width = game_width
        self.height = game_height

        self.space = space  

    def draw_walls(self):
        static_lines = [
            pymunk.Segment(self.space.static_body, (0,0), (self.width, 0), 1.0),
            pymunk.Segment(self.space.static_body, (0,0), (0, self.height), 1.0),
            pymunk.Segment(self.space.static_body, (0, self.height), (self.width, self.height), 1.0),
            pymunk.Segment(self.space.static_body, (self.width, 0), (self.width, self.height), 1.0)
        ]
        for line in static_lines:
            line.elasticity = 0.7
            line.filter = pymunk.ShapeFilter(categories=WALL_CATEGORY, mask=WALL_MASK)
            line.game_object = self
            self.space.add(line)

    def remove_walls(self):
        self.space.remove(static_lines)

