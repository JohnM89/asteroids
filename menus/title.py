from game.state import State
from game.constants import *
from game.userinterface import UserInterface
import pygame
import os
from .startmenu import StartMenu
#from level1 import Level1   
class Title(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.image.load(os.path.join('assets', 'images',"blue-preview.png"))
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.alphaSurface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.alpha = 255
        self.fade_timer = 0
        #self.canvas.blit(self.background, (0, 0))
        #
        #self.animated_fade_panelsq
        #
        #self.animated_fade_panels = pygame.image.load(os.path.join('assets', 'source',"ButtonDigital_Press.png"))
        #
        self.faded = False
        self.timer = 0
        self.hudd = {"Start":"Game"}
        self.ui_sprites = [pygame.image.load('./assets/source/Super Pixel Sci-Fi UI - Futura Max/window_theme/window_theme_green/subpanel_focused.png')]
        self.title_box = UserInterface(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 , 256, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "Asteroids", sprite_array=self.ui_sprites)
        self.updatable.add(self.title_box)
        self.drawable.add(self.title_box)
        
    
    #def fade_in(self, dt):
        #if self.faded:
            
        #if self.timer == 5:
            


    def update(self, dt):
        super().update(dt)
        self.alphaSurface.set_alpha(self.alpha)
        if self.fade_timer < 121:
            if self.fade_timer > 100:
                if self.alpha != 0:
                    self.alpha = max(0, self.alpha - int(dt * 65))
            else:
                self.fade_timer += int(dt * 60)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                print("registered")
                if event.key == pygame.K_SPACE:
                    new_state = StartMenu(self.game)
                    new_state.enter_state()


    
    def draw(self):
        #pass
        super().draw()
        #self.canvas.fill((0, 0, 0))
        self.canvas.blit(self.background, (0,0))
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.canvas.blit(self.alphaSurface, (0,0))
        self.screen.blit(self.canvas, (0,0), self.camera.camera_box)
        self.alphaSurface.fill((0, 0, 0))
        #self.screen.fill((254, 0, 0))
        #self.title_box.draw()
