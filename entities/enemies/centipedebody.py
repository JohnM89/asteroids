from .commonalien import *
import pymunk
class CentipedeBody(CommonAlien):
    def __init__(self, x, y, radius, space, assets, colour=(255,255,255)):
        super().__init__(x , y, radius, space, colour)
        self.assets = assets
        self.shape.friction = 7.0
        self.shape.elasticity = 0.2
        self.shape.collision_type = 5
        self.joints = []
        self.rotation_limit_list = []
        self.image = pygame.Surface((4*self.radius,4*self.radius), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        # self.base_image = pygame.image.load("./assets/source/Export/Enemies - Insectoids/0.5x/Insectoid_Tail_2_B_Small.png")
        # self.base_image = pygame.image.load("./local_assets/assets/source/Export/Enemies - Insectoids/0.5x/Insectoid_Tail_2_B_Small.png")
        self.base_image = self.assets.image("source/Export/Enemies - Insectoids/0.5x/Insectoid_Tail_2_B_Small.png")
        self.base_image = pygame.transform.scale(self.base_image, (3*self.radius, 3*self.radius))
        self.sprite_image = self.base_image.copy()
        self.shape.filter = pymunk.ShapeFilter(categories=ENEMY_CENTIPEDE_BODY_CATEGORY, mask=ENEMY_CENTIPEDE_BODY_MASK)
        self.shape.mass = 5 * self.radius
    
    def draw(self):
        self.image.fill((0,0,0,0))
        self.image.blit(self.sprite_image,(0,0))
        pass
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
        #angle_degrees = -math.degrees(self.body.angle)
        #self.sprite_image = pygame.transform.rotate(sub_surf, angle_degrees)
        #self.sprite_image = pygame.transform.rotate(self.base_image, angle_degrees - 90)
        self.rect = self.sprite_image.get_rect(center=(int(self.body.position.x),int(self.body.position.y)))
