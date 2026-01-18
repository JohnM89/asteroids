import pygame
import pymunk
import math
from .circleshape import *
from game.constants import *
from effects.explosions.rocket_timeout_explosion import RocketTimeOut
from game.raycast import RayCast
from .enemies.commonalien import CommonAlien 

class Rocket(CircleShape):
    def __init__(self, x, y, space, rotation, canvas, updatable, drawable, assets):
        #set a rocket radius 
        super().__init__(x, y, 32, mass=0.75)
        self.canvas = canvas
        self.updatable = updatable
        self.drawable = drawable
        self.assets = assets
        ###
        self.x = x  
        self.y = y
        self.body.angle = rotation
        self.image = pygame.Surface((2*self.radius,2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect(center=(x,y))
        # self.base_image = pygame.image.load("./assets/source/Super Pixel Projectiles Pack 2/spritesheet/pj2_scifi_missile_large_red/spritesheet.png")
        # self.base_image = pygame.image.load("./local_assets/assets/source/Super Pixel Projectiles Pack 2/spritesheet/pj2_scifi_missile_large_red/spritesheet.png")
        self.base_image = self.assets.image("source/Super Pixel Projectiles Pack 2/spritesheet/pj2_scifi_missile_large_red/spritesheet.png") 
        self.sprite_image = self.base_image.copy()
        self.sprite_width = 64
        self.sprite_height = 32 
        self.frame_interval = 0.75   
        self.frame_timer = 0
        self.frame = 0
        self.max_frame = 9
        self.frame_y = 0    
        self.frame_x = 0
        self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.space = space
        self.shape.collision_type = 7
        self.max_view_distance = 150
        #
        self.shape.filter = pymunk.ShapeFilter(categories=PLAYER_BULLET_CATEGORY,mask=PLAYER_BULLET_MASK)
        ##
        self.shape.game_object = self
        self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter)
        self.time_to_live = 8
    def draw(self):
        self.image.fill((0,0,0,0))
        result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        if hasattr(result, "point"):
            if result.point != None:
                if hasattr(result, "shape") and hasattr(result.shape, "game_object"):
                    if isinstance(result.shape.game_object, CommonAlien): 
                        x , y = result.point    
                        if x != 0 or y != 0:
                            self.rotate(x , y)
                            self.move()

        self.image.blit(self.sprite_image,(0,0))
        #pygame.draw.circle(self.image, (255,255,255), (self.radius, self.radius), self.radius, 5)
        #pygame.draw.rect(self.image, (255,255,255), (self.rect), 4)
        
    def rotate(self, x, y):
        direction = (pymunk.Vec2d(x,y) - self.body.position).angle
        self.body.angle = direction

    def move(self):
        if self.body.velocity.length < PLAYER_SPEED:
            forward = pymunk.Vec2d(1, 0).rotated(self.body.angle)
            acceleration = forward * ACCELERATION
            accel = pymunk.Vec2d(acceleration.x, acceleration.y)
            self.body.velocity += accel
        

    def update(self, dt):

        if self.frame_timer > self.frame_interval:
            self.frame += 1
            if self.frame <= self.max_frame:
                self.frame_timer = 0
            else:
                self.frame = 0
        else:
            self.frame_timer += dt  
        
        self.frame_x = self.frame * self.sprite_width
        self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        sub_surf = self.base_image.subsurface(self.crop_rect)
        angle_degrees = -math.degrees(self.body.angle)
        self.sprite_image = pygame.transform.rotate(sub_surf, angle_degrees)
        self.rect = self.sprite_image.get_rect(center=(int(self.body.position.x),int(self.body.position.y)))

        self.body.velocity *= DRAG_COEFFICENT
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            explode = RocketTimeOut(int(self.body.position.x), int(self.body.position.y), self.assets)
            self.updatable.add(explode)
            self.drawable.add(explode)
            self.space.remove(self.body, self.shape)

