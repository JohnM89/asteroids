import pygame
import pymunk
from circleshape import *
from constants import *
from raycast import RayCast
from commonalien import CommonAlien 

class Rocket(CircleShape):
    def __init__(self, x, y, space, canvas):
        #set a rocket radius 
        super().__init__(x, y, 15, mass=0.5)
        self.canvas = canvas
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect()
        self.space = space
        self.shape.collision_type = 7
        self.max_view_distance = 100
        self.shape.filter = pymunk.ShapeFilter(categories=PLAYER_BULLET_CATEGORY,mask=PLAYER_BULLET_MASK)
        self.shape.game_object = self
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter)
        self.time_to_live = 3.5
    def draw(self):
        result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        if hasattr(result, "point"):
            if result.point != None:
                if hasattr(result, "shape") and hasattr(result.shape, "game_object"):
                    if isinstance(result.shape.game_object, CommonAlien): 
                        x , y = result.point    
                        if x != 0 or y != 0:
                            self.rotate(x , y)
                            self.move()

        #self.image.fill((0,0,0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
    def rotate(self, x, y):
        direction = (pymunk.Vec2d(x,y) - self.body.position).angle
        self.body.angle = direction
    def move(self):
        forward = pymunk.Vec2d(1 , 0).rotated(self.body.angle)
        acceleration = forward * ACCELERATION
        accel = pymunk.Vec2d(acceleration.x, acceleration.y)
        self.body.velocity += accel 

    def update(self, dt):
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        else:
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))
