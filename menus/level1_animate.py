from game.state import State
from game.constants import *
from game.userinterface import UserInterface
import pygame
import os
#from .startmenu import StartMenu
from effects.meteor_intro import MeteorIntro
from levels.level1 import Level1   
class Level1Animate(State):
    def __init__(self, game, selected_sprite):
        super().__init__(game)
        self.selected_sprite = selected_sprite
        self.background = pygame.image.load('./assets/source/Bright/blue_green.png')
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.alphaSurface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        #self.alpha = 255
        self.fade_timer = 0
        #self.canvas.blit(self.background, (0, 0))
        #
        #self.animated_fade_panelsq
        #
        #self.animated_fade_panels = pygame.image.load(os.path.join('assets', 'source',"ButtonDigital_Press.png"))
        #
        self.meteor = MeteorIntro(self, -10, self.SCREEN_HEIGHT / 2, 64)
        self.first_pass = True
        self.animate_meteor = False
        self.faded = False
        self.timer = 0
        self.hudd = {"Start":"Game"}
        #self.ui_sprites = [pygame.image.load('./assets/source/Pixel UI & HUD/Sprites/Panels/Blue/FrameDigitalA.png')]
        #self.title_box = UserInterface(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 , 256, 64, "GravityRegular5", "./assets/fonts/Fonts/GravityRegular5.ttf", "Asteroids", sprite_array=None)
        #self.updatable.add(self.title_box)
        #self.drawable.add(self.title_box)
        
    
    #def fade_in(self, dt):
        #if self.faded:
            
        #if self.timer == 5:
            


    def update(self, dt):
        super().update(dt)
        #self.alphaSurface.set_alpha(self.alpha)
        #if self.alpha != 0:
        #    self.alpha = max(0, self.alpha - int(dt * 65))
        #elif self.alpha == 0 and self.first_pass:
        meteor = MeteorIntro(self, 0, self.SCREEN_HEIGHT / 2, 64 )
        self.animate_meteor = True
        self.drawable.add(self.meteor, layer=1)
        self.updatable.add(self.meteor)
        if self.animate_meteor:
            if self.meteor.x > self.SCREEN_WIDTH / 2:
                #self.updatable.add(self.title_box)
                #self.drawable.add(self.title_box, layer=0)
                pass

            if self.meteor.x < self.SCREEN_WIDTH:
                self.meteor.x += (dt * 180)
            elif self.meteor.x >= self.SCREEN_WIDTH:
                self.animate_meteor = False
                self.first_pass = False
                self.drawable.remove(self.meteor)
                self.updatable.remove(self.meteor)
                self.meteor.kill()
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                print("registered")
                if event.key == pygame.K_SPACE:
                    new_state = Level1(self.game, self.selected_sprite)
                    new_state.enter_state()


    
    def draw(self):
        #pass
        super().draw()
        #self.canvas.fill((0, 0, 0))
        self.canvas.blit(self.background, (0,0))
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        #self.canvas.blit(self.alphaSurface, (0,0))
        self.screen.blit(self.canvas, (0,0), self.camera.camera_box)
        #self.alphaSurface.fill((0, 0, 0))
        #self.screen.fill((254, 0, 0))
        #self.title_box.draw()
