import pygame   
import pymunk   
from game.constants import *
from game.raycast import RayCast
from .commonalien import *
from .centipedebody import *
class CentipedeHead(CommonAlien):
    def __init__(self, x, y, radius, space, canvas, colour=(0,0,0)):
        super().__init__(x , y, radius, space, colour)
        self.radius = self.radius
        self.canvas = canvas
        self.shape.friction = 7.0
        self.shape.elasticity = 0.2 
        self.joints = []
        self.rotation_limit_list = []
        #self.shape.collision_type = 5
        self.shape.mass = 40 * self.radius
        self.max_view_distance = 200
        self.image = pygame.Surface((4*self.radius,4*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.base_image = pygame.image.load("./assets/source/Export/Enemies - Insectoids/0.5x/Insectoid_5_A_Small.png")
        self.base_image = pygame.transform.scale(self.base_image, (3*self.radius, 3*self.radius))
        self.sprite_image = self.base_image.copy()
        self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter, self.radius)
        #self.shape.filter = pymunk.ShapeFilter(group=2)
        
    def draw(self):
        self.image.fill((0,0,0,0))
        result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        #for res in result:
        #if hasattr(result, "point"):
            #if result.point != None:
        if hasattr(result, "shape") and hasattr(result.shape, "game_object"):
            if result.shape.game_object.__class__.__name__ == "FuelDrop":
                x , y = result.point
                if x != 0 or y != 0:
                    towards = True  
                    self.rotate(x, y, towards)
                    boost = True
                    self.move(boost)
                    #break
            else:
                x , y = result.point
                if x != 0 or y != 0:
                    self.rotate(x, y)
                    self.move()
                    #break
        self.image.blit(self.sprite_image,(0,0))
    def rotate(self,x, y, towards=False):
        if towards == True:
            direction = (pymunk.Vec2d(x, y) - self.body.position).angle
            self.body.angle = direction
        else:
            direction = (pymunk.Vec2d(x, y) - self.body.position).angle
            self.body.angle = (direction + math.pi)

    def move(self, boost=False):
        forward = pymunk.Vec2d(1, 0).rotated(self.body.angle)
        if boost == True:
            if self.body.velocity.length < (PLAYER_SPEED / 2):
                acceleration = forward * ACCELERATION
                accel = pymunk.Vec2d(acceleration.x, acceleration.y)
                self.body.velocity += accel
        else:
            if self.body.velocity.length < (PLAYER_SPEED / 2):
                acceleration = forward * (ACCELERATION * 0.002)
                accel = pymunk.Vec2d(acceleration.x, acceleration.y)
                self.body.velocity += accel
            else:
                self.body.velocity *= DRAG_COEFFICENT

    def bounds_check(self):
        super().bounds_check()
    def update(self, dt):
        super().update(dt)
        #if self.frame_timer > self.frame_interval:
         #   self.frame += 1
          #  if self.frame <= self.max_frame:
           #     self.frame_timer = 0
            #else:
             #   self.frame = 0
        #else:
         #   self.frame_timer += dt

        #self.frame_x = self.frame * self.sprite_width
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        #sub_surf = self.base_image.subsurface(self.crop_rect)
        angle_degrees = -math.degrees(self.body.angle)
        #self.sprite_image = pygame.transform.rotate(sub_surf, angle_degrees)
        self.sprite_image = pygame.transform.rotate(self.base_image, angle_degrees - 90)
        self.rect = self.sprite_image.get_rect(center=(int(self.body.position.x),int(self.body.position.y)))
