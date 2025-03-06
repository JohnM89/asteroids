import pygame
from .circleshape import *
from game.constants import *

class FuelDrop(CircleShape):
    def __init__(self, x, y, space):
        super().__init__(x, y, SHOT_RADIUS, mass=0.1)
        self.radius = self.radius * 3
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()  
        self.rect = self.image.get_rect()
        self.base_image = pygame.image.load("./assets/source/Export/Pickups/0.5x/Pickup_HealthPack_Small.png")
        self.base_image = pygame.transform.scale(self.base_image, (2*self.radius, 2*self.radius))
        self.sprite_image = self.base_image.copy()
        #self.sprite_width = 64
        #self.sprite_height = 32
        #self.frame_interval = 0.75
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 9
        #self.frame_y = 0
        #self.frame_x = 0
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.space = space
        self.shape.collision_type = 4
        self.shape.game_object = self
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.time_to_live = 10.5
        ## make this amount random 
        self.fuel = 5.0
    def draw(self):
        self.image.fill((0,0,0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.image.blit(self.sprite_image,(0,0))
        pass
    def update(self, dt):
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        else:
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))

class BombDrop(CircleShape):
    def __init__(self, x, y, space):
        super().__init__(x, y, SHOT_RADIUS, mass=0.1)
        self.radius = self.radius * 3
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.base_image = pygame.image.load("./assets/source/Export/Pickups/0.5x/Pickup_Crate_1_Small.png")
        self.base_image = pygame.transform.scale(self.base_image, (2*self.radius, 2*self.radius))
        self.sprite_image = self.base_image.copy()
        #self.sprite_width = 64
        #self.sprite_height = 32
        #self.frame_interval = 0.75
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 9
        #self.frame_y = 0
        #self.frame_x = 0
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.space = space
        self.shape.collision_type = 4
        self.shape.game_object = self
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.time_to_live = 10.5
        ## make this amount random
        self.bomb = 1
    def draw(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.sprite_image,(0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        #pass
    def update(self, dt):
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        else:
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))

class SheildDrop(CircleShape):
    def __init__(self, x, y, space):
        super().__init__(x, y, SHOT_RADIUS, mass=0.1)
        self.radius = self.radius * 3
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.base_image = pygame.image.load("./assets/source/Export/Pickups/0.5x/Pickup_Crate_2_Small.png")
        self.base_image = pygame.transform.scale(self.base_image, (2*self.radius, 2*self.radius))
        self.sprite_image = self.base_image.copy()
        #self.sprite_width = 64
        #self.sprite_height = 32
        #self.frame_interval = 0.75
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 9
        #self.frame_y = 0
        #self.frame_x = 0
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.space = space
        self.shape.collision_type = 4
        self.shape.game_object = self
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.time_to_live = 10.5
        self.sheild = 1
    def draw(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.sprite_image,(0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        pass
    def update(self, dt):
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        else:
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))

class RocketDrop(CircleShape):
    def __init__(self, x, y, space):
        super().__init__(x, y, SHOT_RADIUS, mass=0.1)
        self.radius = self.radius * 3
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.base_image = pygame.image.load("./assets/source/Export/Ships - Missiles/Variation_B/0.5x/Missile_4_B_Small.png")
        self.base_image = pygame.transform.scale(self.base_image, (2*self.radius, 2*self.radius))
        self.sprite_image = self.base_image.copy()
        #self.sprite_width = 64
        #self.sprite_height = 32
        #self.frame_interval = 0.75
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 9
        #self.frame_y = 0
        #self.frame_x = 0
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.space = space
        self.shape.collision_type = 4
        self.shape.game_object = self
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.time_to_live = 10.5
        ## make this amount random
        self.rockets = 5
    def draw(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.sprite_image,(0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        pass
    def update(self, dt):
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        else:
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))
class YamatoCannon(CircleShape):
    def __init__(self, x, y, space):
        super().__init__(x, y, SHOT_RADIUS, mass=0.1)
        self.radius = self.radius * 3
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.base_image = pygame.image.load("./assets/source/Export/Pickups/0.5x/Pickup_Crate_3_Small.png")
        self.base_image = pygame.transform.scale(self.base_image, (2*self.radius, 2*self.radius))
        self.sprite_image = self.base_image.copy()
        #self.sprite_width = 64
        #self.sprite_height = 32
        #self.frame_interval = 0.75
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 9
        #self.frame_y = 0
        #self.frame_x = 0
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.space = space
        self.shape.collision_type = 4
        self.shape.game_object = self
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.time_to_live = 10.5
        ## make this amount random
        self.yamato = 1
    def draw(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.sprite_image,(0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        pass
    def update(self, dt):
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        else:
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))

class MultiShot(CircleShape):
    def __init__(self, x, y, space):
        super().__init__(x, y, SHOT_RADIUS, mass=0.1)
        self.radius = self.radius * 3
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.base_image = pygame.image.load("./assets/source/Export/Pickups/0.5x/Pickup_Crate_4_Small.png")
        self.base_image = pygame.transform.scale(self.base_image, (2*self.radius, 2*self.radius))
        self.sprite_image = self.base_image.copy()
        #self.sprite_width = 64
        #self.sprite_height = 32
        #self.frame_interval = 0.75
        #self.frame_timer = 0
        #self.frame = 0
        #self.max_frame = 9
        #self.frame_y = 0
        #self.frame_x = 0
        #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        self.space = space
        self.shape.collision_type = 4
        self.shape.game_object = self
        pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        self.time_to_live = 10.5
        ## make this amount random
        self.multishot = 50
    def draw(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.sprite_image,(0,0))
        #pygame.draw.circle(self.image,(255,255,255), (self.radius, self.radius), self.radius, width=2)
        pass
    def update(self, dt):
        self.time_to_live -= dt
        if self.time_to_live < dt:
            self.kill()
            self.space.remove(self.body, self.shape)
        else:
            self.rect.center = (int(self.body.position.x), int(self.body.position.y))

#class SomeOtherWeapon(CircleShape):
