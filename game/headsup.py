import pygame
from entities.squareshape import *
from .constants import *
from .font import FontManager
class HeadsUp(SquareShape):
    def __init__(self, x, y, w, h, ui_text=None, key=None, hudd=None, sprite=None):
        super().__init__(x, y, w, h)
        self.font_size = 16
        self.font = "GravityRegular5"
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.__path = './assets/fonts/Fonts/GravityRegular5.ttf'
        self.hudd = hudd
        self.max_health = 100
        self.health_ratio = self.hudd["health"] / self.max_health
        self.key = key
        self.ui_text = ui_text
        self.font_manager = FontManager()
        self.font_manager.load_font(self.font, self.__path, self.font_size)


        #if self.hudd != None:
        #    self.text = f"{self.ui_text}{self.hudd[self.key]}"
        #elif self.hudd == None:
        #    self.text = f"{self.ui_text}"
        
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.healthbarbackground = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Red/RoundBarBackground.png')
        #self.sheildbackground = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Blue/RoundBarBackground.png')
        self.healthbarfill = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Red/RoundBarFill.png')
        self.healthbarfollowfill = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Red/RoundBarFollowFill.png')
        #self.healthbarfollowfill = pygame.transform.scale_by(self.healthbarfollowfill, (1, 4))

        #self.fuel
        #self.sheildbar
        #self.rockets
        #self.bombs
        #self.character_panel
        #self.character_sprite

        self.image = self.image.convert_alpha()      
        #self.w = self.font_manager.text_surface.get_width()

    def draw(self, screen=None):
        self.image.fill((0,0,0,0))
        #ui box, will hold score, lives and powerups etc...
        #if screen:

            
            #self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
            #self.rect.center = (self.x,self.y)
        #    self.font_manager.render_text(screen, self.text, self.font, (255,255,255), self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        #else:
            

        #    self.rect = self.image.get_rect()
        #    self.rect.center = (self.x, self.y)
        #    self.font_manager.render_text(self.image, self.text , self.font, (255,255,255), 0, 0, self.rect.width, self.rect.height)
        #self.image.blit(self.hud_background, (0,0)):
        #self.image.blit(self.healthbarbackground, (128 + 34, 64 + 18))
        #self.image.blit(self.healthbarfollowfill, (128 + 40, 64 + 22))

        
        self.healthbar_width = self.healthbarfill.get_width()
        self.healthbarfill_height = self.healthbarfill.get_height()
        #create caps 4 in size for front and end
        self.middle_width = self.healthbar_width - 4 - 4
        self.visible_width = max(1, int(self.middle_width * self.health_ratio * 20))
        self.max_width = self.middle_width * 1 * 20

        self.left_cap = self.healthbarfill.subsurface((0, 0, 4, self.healthbarfill_height))
        self.left_cap_background = self.healthbarbackground.subsurface((0,0,4, self.healthbarbackground.get_height()))
        self.left_cap_follow = self.healthbarfollowfill.subsurface((0, 0, 4, self.healthbarfill_height))
        self.right_cap = self.healthbarfill.subsurface((4 + self.middle_width, 0, 4, self.healthbarfill_height))
        self.right_cap_background = self.healthbarbackground.subsurface((0,0,4, self.healthbarbackground.get_height()))
        self.right_cap_follow = self.healthbarfollowfill.subsurface((4 + self.middle_width, 0, 4, self.healthbarfill_height))
        self.fill_crop = self.healthbarfill.subsurface((4, 0, self.middle_width, self.healthbarfill_height))
        self.fill_crop_background = self.healthbarbackground.subsurface((4,0, self.middle_width, self.healthbarbackground.get_height()))
        self.fill_crop_follow = self.healthbarfollowfill.subsurface((4, 0, self.middle_width, self.healthbarfill_height))
        
        bar_x = 128 + 40
        bar_y = 64 + 22
        self.scale_middle = pygame.transform.scale(self.fill_crop,(self.visible_width, self.healthbarfill_height))
        self.scale_middle_background = pygame.transform.scale(self.fill_crop_background, (self.max_width, self.healthbarbackground.get_height()))
        self.scale_middle_follow = pygame.transform.scale(self.fill_crop_follow, (self.visible_width, self.healthbarfill_height))
        self.image.blit(self.left_cap_background, (bar_x, bar_y))
        self.image.blit(self.scale_middle_background, (bar_x + 4, bar_y))
        self.image.blit(self.right_cap_background, (bar_x + 4 + self.max_width, bar_y))
        self.image.blit(self.left_cap_follow, (bar_x, bar_y))
        self.image.blit(self.scale_middle_follow, (bar_x + 4, bar_y))
        self.image.blit(self.right_cap_follow, (bar_x + 4 + self.visible_width, bar_y))
        self.image.blit(self.left_cap, (bar_x, bar_y))
        self.image.blit(self.scale_middle, (bar_x + 4, bar_y))
        self.image.blit(self.right_cap, (bar_x + 4 + self.visible_width, bar_y))
        #for i in range(4):
        #self.image.blit(self.filler_2, (128 + 56, 64 + 18 ))
        #self.image.blit(self.filler_2, (128 + 88, 64 + 18))
        #self.image.blit(self.filler_2, (128 + 120, 64 + 18))

        #self.image.blit(self.hud_overlay, (0,0))

        screen.blit(self.image, self.rect)
    def update(self, dt):
        pass        
    #heads up display data 
    def get_hudd(self, hudd=None, text=None):
        if hudd != None:
            self.hudd = hudd
            self.health_ratio = self.hudd["health"] / self.max_health
        #if text != None:
        #    self.text = f"{text}"
        #pass
