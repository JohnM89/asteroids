import pygame
from squareshape import *
from constants import *
from font import FontManager
class UserInterface(SquareShape):
    def __init__(self, x, y, w, h, font, path, ui_text, key=None, hudd=None):
        super().__init__(x, y, w, h)
        self.font_size = 16
        self.font = font
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.__path = path
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
            #box_x = self.rect.x + (self.rect.w / 100) * 6
            #box_y = self.rect.y + self.rect.h - (self.rect.h / 1.5)
            self.font_manager.render_text(screen, self.text, self.font, (255,255,255), self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        else:
            

            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            pygame.draw.rect(self.image, (255,255,255), (0, 0, self.w, self.h), width=2, border_radius=2)
            self.font_manager.render_text(self.image, self.text , self.font, (255,255,255), 0, 0, self.rect.width, self.rect.height)
    def update(self, dt):

        pass
    #heads up display data 
    def get_hudd(self, hudd=None, text=None):
        if hudd != None:
            self.text = f"{self.ui_text}{hudd[self.key]}"
        if text != None:
            self.text = f"{text}"
