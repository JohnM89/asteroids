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
        self.hud_background = pygame.image.load('./assets/source/2D_ShootEmUp_GUI/PNG/HeadsUpDisplay/HUD_Background.png')
        self.hud_background = pygame.transform.scale(self.hud_background, (w, h))
        self.hud_overlay = pygame.image.load('./assets/source/2D_ShootEmUp_GUI/PNG/HeadsUpDisplay/HUD_Top_2.png')
        self.hud_overlay = pygame.transform.scale(self.hud_overlay, (w, h))
        self.filler_1 = pygame.image.load('./assets/source/2D_ShootEmUp_GUI/PNG/HeadsUpDisplay/Energy_Filler_Bar_Gold_1.png')
        #self.filler_1 = pygame.transform.scale(self.filler_1, (w , h))
        self.filler_2 = pygame.image.load('./assets/source/2D_ShootEmUp_GUI/PNG/HeadsUpDisplay/Energy_Filler_Bar_Gold_2.png')
        self.filler_3 = pygame.image.load('./assets/source/2D_ShootEmUp_GUI/PNG/HeadsUpDisplay/Energy_Filler_Bar_Gold_3.png')
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
        self.image.blit(self.hud_background, (0,0))
        #self.image.blit(self.filler_1, (64, 0))
        self.image.blit(self.hud_overlay, (0,0))

        screen.blit(self.image, self.rect)
    def update(self, dt):

        pass
    #heads up display data 
    def get_hudd(self, hudd=None, text=None):
        #if hudd != None:
        #    self.text = f"{self.ui_text}{hudd[self.key]}"
        #if text != None:
        #    self.text = f"{text}"
        pass
