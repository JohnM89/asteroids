import pygame
from entities.squareshape import *
from game.constants import *
from .font import FontManager
class UserInterface(SquareShape):
    def __init__(self, x, y, w, h, font=None, path=None, ui_text='', key=None, hudd=None, sprite_array=None, font_colour=(255,255,255), overlay=None, overlay_offset_w=0, overlay_offset_h=0,  overlay_active=False):
        super().__init__(x, y, w, h)
        self.font_size = 16
        self.font = font
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.__path = path
        self.sprite = sprite_array
        self.overlay = overlay
        self.font_colour = font_colour
        self.overlay_active = overlay_active
        self.overlay_offset_w = overlay_offset_w
        self.overlay_offset_h = overlay_offset_h
        if self.sprite != None:
            self.image = pygame.Surface((w,h), pygame.SRCALPHA)
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect(center=(x,y))
            self.base_image = self.sprite[0]
            self.sprite_image = self.base_image.copy()
            self.sprite_image = pygame.transform.scale(self.sprite_image, (self.w, self.h))
            #self.sprite_width = 64
            #self.sprite_height = 32
            #self.frame_interval = 0.75
            #self.frame_timer = 0
            #self.frame = 0
            #self.max_frame = 9
            #self.frame_y = 0
            #self.frame_x = 0
            #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
        
        if self.overlay != None:
            #self.overlay_image = pygame.Surface((w,h), pygame.SRCALPHA)
            #self.rect = self.overlay_image.get_rect(center=(x,y))
            self.base_overlay_image = self.overlay
            self.overlay_sprite_image = self.base_overlay_image.copy()
            self.overlay_sprite_image = pygame.transform.scale(self.overlay_sprite_image, (self.w, self.h))
                

        self.hudd = hudd
        self.key = key
        self.ui_text = ui_text
        self.font_manager = FontManager()
        self.font_manager.load_font(self.font, self.__path, self.font_size)
        if self.hudd != None:
            self.text = f"{self.ui_text}{self.hudd[self.key]}"
        elif self.hudd == None:
            self.text = f"{self.ui_text}"
        
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()      
        #self.w = self.font_manager.text_surface.get_width()

    def draw(self, screen=None):
        self.image.fill((0,0,0,0))
        #ui box, will hold score, lives and powerups etc...
        if screen:

            
            self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
            self.rect.center = (self.x,self.y)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, width=2, border_radius=2)
            #self.image.blit(self.sprite_image, (0,0))
            #self.screen.blit(self.image, self.rect)
            #box_x = self.rect.x + (self.rect.w / 100) * 6
            #box_y = self.rect.y + self.rect.h - (self.rect.h / 1.5)
            self.font_manager.render_text(screen, self.text, self.font, self.font_colour, self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        else:
            

            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            if hasattr(self, 'sprite_image'):
            #pygame.draw.rect(self.image, (255,255,255), (0, 0, self.w, self.h), width=2, border_radius=2)
                self.image.blit(self.sprite_image, (0,0))
            if hasattr(self, 'overlay_sprite_image') and self.overlay_active:
                self.image.blit(self.overlay_sprite_image, (0,0))
            else:
                pass
                #pygame.draw.rect(self.image, (255, 255, 255), (0 , 0, self.w, self.h), width=2, border_radius=2)
            #self.screen.blit(self.image, self.rect)
            self.font_manager.render_text(self.image, self.text , self.font, self.font_colour, 0, 0, self.rect.width, self.rect.height)
    def update(self, dt):
        self.overlay_active = self.overlay_active
        #if self.sprite != None:
            #if self.frame_timer > self.frame_interval:
                #self.frame += 1
                #if self.frame <= self.max_frame:
                #    self.frame_timer = 0
                #else:
                    #self.frame = 0
            #else:
                #self.frame_timer += dt

            #self.frame_x = self.frame * self.sprite_width
            #self.crop_rect = pygame.Rect(self.frame_x, self.frame_y, self.sprite_width, self.sprite_height)
            #sub_surf = self.base_image.subsurface(self.crop_rect)
            #angle_degrees = -math.degrees(self.body.angle)
            #self.sprite_image = pygame.transform.rotate(sub_surf, angle_degrees)
            #self.rect = self.sprite_image.get_rect(center=(int(self.body.position.x),int(self.body.position.y)))
        pass
    #heads up display data 
    def get_hudd(self, hudd=None, text=None):
        if hudd != None:
            self.text = f"{self.ui_text}{hudd[self.key]}"
        if text != None:
            self.text = f"{text}"
