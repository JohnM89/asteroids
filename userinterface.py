import pygame
from squareshape import *
from constants import *
from font import FontManager
class UserInterface(SquareShape):
    def __init__(self, x, y, w, h, font, path, hudd, key, ui_text):
        super().__init__(x, y, w, h)
        self.font_size = 16
        self.font = font
        self.__path = path
        self.hudd = hudd
        self.key = key
        self.ui_text = ui_text
        self.font_manager = FontManager()
        self.font_manager.load_font(self.font, self.__path, self.font_size)
        self.text = f"{self.ui_text}{self.hudd[self.key]}"
    def draw(self, screen):
        #ui box, will hold score, lives and powerups etc...
        pygame.draw.rect(screen, (255, 255, 255), self.rect, width=2, border_radius=2)
        #offset x by margin of 6
        box_x = self.rect.x + ( self.rect.w / 100) * 6
        #set height to height - heigh / 1.5, temporary solution
        box_y = self.rect.y + self.rect.h - (self.rect.h / 1.5)
        self.font_manager.render_text(screen, self.text , self.font, (255,255,255), (box_x, box_y))
    def update(self, dt):
        pass 
    #heads up display data 
    def get_hudd(self, hudd):
        self.text = f"{self.ui_text}{hudd[self.key]}"

