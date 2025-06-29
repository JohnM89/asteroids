import pygame
import os
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
        self.max_fuel = 100
        #self.max_rockets = 30
        self.health_ratio = self.hudd["health"] / self.max_health
        self.fuel_ratio = self.hudd["fuel"] / self.max_fuel
        self.sheild_health = self.hudd["sheilds_health"]
        
        self.sheild_level = int(self.sheild_health / 100 * 8)
        self.key = key
        self.ui_text = ui_text
        self.font_manager = FontManager()
        self.font_manager.load_font(self.font, self.__path, self.font_size)


        #if self.hudd != None:
        #    self.text = f"{self.ui_text}{self.hudd[self.key]}"
        #elif self.hudd == None:
        #    self.text = f"{self.ui_text}"
        self.flask_sprites = []
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.player_icon = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Portraits/PlayerSmallFrame.png')
        self.player_icon = pygame.transform.scale_by(self.player_icon, (3,3))
        self.healthbarbackground = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Red/RoundBarBackground.png')
        self.fuelbarbackground = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Red/FighterBarSecondaryBackground.png')
        self.sheildbackground = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Blue/FlaskBackground.png').convert_alpha()
        self.sheildbackground = pygame.transform.scale_by(self.sheildbackground, (3, 3))
        self.sheildforeground = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Blue/FlaskForeground.png').convert_alpha()
        self.fuelbarforeground = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Red/FighterBarSecondaryForeground.png').convert_alpha()
        self.sheildforeground = pygame.transform.scale_by(self.sheildforeground, (3, 3))
        for img in sorted(os.listdir('./assets/sprites/flasks')):
            self.flask_sprites.append(pygame.image.load(os.path.join('./assets/sprites/flasks', img)))
        self.healthbarfill = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Red/RoundBarFill.png')
        self.fuelbarfill = pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/ValueBars/Red/FighterBarSecondaryFill.png')
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
        self.image.blit(self.player_icon, (32,64))
        self.image.blit(self.sheildbackground, (88, 64))
        #self.sheild_level = int(self.sheild_health / 100 * 8)
        flask_level = self.flask_sprites[self.sheild_level]
        flask_level = pygame.transform.scale_by(flask_level, (3,3))
        self.image.blit(flask_level, (94, 70))
        self.image.blit(self.sheildforeground, (88, 64))

        
        self.healthbar_width = self.healthbarfill.get_width()
        self.fuelbar_width = self.fuelbarfill.get_width()
        self.healthbarfill_height = self.healthbarfill.get_height()
        self.fuelbarfill_height = self.fuelbarfill.get_height()
        self.fuelbarfill_middle_width = self.fuelbar_width - 4 - 4
        self.visible_fuel_width = max(1, int(self.fuelbarfill_middle_width * self.fuel_ratio * 20))
        self.max_fuel_width = self.fuelbarfill_middle_width * 1 * 20
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

        self.fuel_left_cap = self.fuelbarfill.subsurface((0, 0, 4, self.fuelbarfill_height))
        self.fuel_left_cap_background = self.fuelbarbackground.subsurface((0,0,4, self.fuelbarbackground.get_height()))
        self.fuel_left_cap_follow = self.fuelbarforeground.subsurface((0, 0, 4, self.fuelbarfill_height))
        self.fuel_right_cap = self.fuelbarfill.subsurface((4 + self.fuelbarfill_middle_width, 0, 4, self.fuelbarfill_height))
        self.fuel_right_cap_background = self.fuelbarbackground.subsurface(( self.fuelbarbackground.get_width() - 4 ,0,4, self.fuelbarbackground.get_height()))
        self.fuel_right_cap_follow = self.fuelbarforeground.subsurface((4 + self.fuelbarfill_middle_width, 0, 4, self.fuelbarfill_height))
        self.fuel_fill_crop = self.fuelbarfill.subsurface((4, 0, self.fuelbarfill_middle_width, self.fuelbarfill_height))
        self.fuel_fill_crop_background = self.fuelbarbackground.subsurface((4,0, self.fuelbarfill_middle_width, self.fuelbarbackground.get_height()))
        self.fuel_fill_crop_follow = self.fuelbarforeground.subsurface((4, 0, self.fuelbarfill_middle_width, self.fuelbarfill_height))

        bar_x = 128 + 18
        bar_y = 64 + 26
        fuel_bar_x = 128 + 18
        fuel_bar_y = 64 + 9
        self.fuel_scale_middle = pygame.transform.scale(self.fuel_fill_crop,(self.visible_fuel_width, self.fuelbarfill_height))
        self.fuel_scale_middle_background = pygame.transform.scale(self.fuel_fill_crop_background, (self.max_fuel_width + 8, self.fuelbarbackground.get_height() + 1))
        #self.fuel_left_cap_background = pygame.transform.scale_by(self.fuel_left_cap_background, ( 0, 2)) 
        #self.fuel_right_cap_background = pygame.transform.scale_by(self.fuel_right_cap_background, (0, 2))
        self.fuel_scale_middle_follow = pygame.transform.scale(self.fuel_fill_crop_follow, (self.visible_fuel_width, self.fuelbarfill_height))
        self.image.blit(self.fuel_left_cap_background, (fuel_bar_x - 4, fuel_bar_y - 2))
        self.image.blit(self.fuel_scale_middle_background, (fuel_bar_x, fuel_bar_y - 2))
        self.image.blit(self.fuel_right_cap_background, (fuel_bar_x + self.max_fuel_width + 8, fuel_bar_y - 2))
        self.image.blit(self.fuel_left_cap_follow, (fuel_bar_x, fuel_bar_y))
        self.image.blit(self.fuel_scale_middle_follow, (fuel_bar_x + 4, fuel_bar_y))
        self.image.blit(self.fuel_right_cap_follow, (fuel_bar_x + 4 + self.visible_fuel_width, fuel_bar_y))
        self.image.blit(self.fuel_left_cap, (fuel_bar_x, fuel_bar_y))
        self.image.blit(self.fuel_scale_middle, (fuel_bar_x + 4, fuel_bar_y))
        self.image.blit(self.fuel_right_cap, (fuel_bar_x + 4 + self.visible_fuel_width, fuel_bar_y))

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
            self.fuel_ratio = self.hudd["fuel"] / self.max_fuel
            self.sheilds_health = self.hudd["sheilds_health"]

            self.sheild_level = int(self.hudd["sheilds_health"] / 100 * 8)
            #print(self.sheilds_health)
            #print(self.sheild_level)
        #if text != None:
        #    self.text = f"{text}"
        #pass
