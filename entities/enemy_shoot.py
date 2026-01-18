import pygame
import pymunk
import math
import os
import random
from .circleshape import *
from game.constants import *
from effects.explosions.rocket_timeout_explosion import RocketTimeOut
#from game.raycast import RayCast
from .enemies.commonalien import CommonAlien 

class EnemyShoot(CircleShape):
    def __init__(self, x, y, space, rotation, assets):
        #set a rocket radius 
        super().__init__(x, y, 16, mass=0.75)
        #self.canvas = canvas
        self.assets = assets
        self.skins = []
        # for img in os.listdir('./assets/sprites/enemyshot'):
        #     self.skins.append(pygame.image.load(os.path.join('./assets/sprites/enemyshot', img)))
        # for img in os.listdir('./local_assets/assets/sprites/enemyshot'):
        #     self.skins.append(pygame.image.load(os.path.join('./local_assets/assets/sprites/enemyshot', img)))
        self.skins = self.assets.images_in('sprites/enemyshot')
        #self.updatable = updatable
        #self.drawable = drawable
        ###
        self.x = x  
        self.y = y
        self.body.angle = rotation
        self.image = pygame.Surface((2*self.radius,2*self.radius), pygame.SRCALPHA)
        #self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect(center=(x,y))
        self.base_image = random.choice(self.skins).convert_alpha()
        #self.base_image = pygame.image.load("./assets/source/Super Pixel Projectiles Pack 2/spritesheet/pj2_scifi_missile_large_red/spritesheet.png") 
        self.sprite_image = self.base_image.copy()
        self.sprite_width = 32
        self.sprite_height = 24 
        self.frame_interval = 0.1   
        self.frame_timer = 0
        self.frame = 0
        self.max_frame = 7
        self.frame_y = 0    
        self.frame_x = 0
        self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.space = space
        self.shape.collision_type = 6
        #self.max_view_distance = 150
        #
        self.shape.filter = pymunk.ShapeFilter(categories=ENEMY_BULLET_CATEGORY,mask=ENEMY_BULLET_MASK)
        ##
        self.shape.game_object = self
        #self.ray_cast = RayCast(self.space, self.canvas, self.max_view_distance, self.shape.filter)
        self.time_to_live = 2
    def draw(self):
        self.image.fill((0,0,0,0))
        #result = self.ray_cast.cast_ray(self.body.position.x, self.body.position.y)
        #if hasattr(result, "point"):
            #if result.point != None:
                #if hasattr(result, "shape") and hasattr(result.shape, "game_object"):
                    #if isinstance(result.shape.game_object, CommonAlien): 
                        #x , y = result.point    
                        #if x != 0 or y != 0:
                            #self.rotate(x , y)
                            #self.move()

        self.image.blit(self.sprite_image,(0,0))
        #pygame.draw.circle(self.image, (255,255,255), (self.radius, self.radius), self.radius, 5)
        #pygame.draw.rect(self.image, (255,255,255), (self.rect), 4)
        
    #def rotate(self, x, y):
        #direction = (pymunk.Vec2d(x,y) - self.body.position).angle
        #self.body.angle = direction
        

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

        #self.body.velocity *= DRAG_COEFFICENT
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            #explode = RocketTimeOut(int(self.body.position.x), int(self.body.position.y))
            #self.updatable.add(explode)
            #self.drawable.add(explode)
            self.space.remove(self.body, self.shape)

