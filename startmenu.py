from state import State 
from constants import * 
from userinterface import UserInterface 
import pygame
from level1 import Level1
class StartMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.hudd = {"Start":"___"}
        self.__font = "GravityRegular5"
        self.__font_path = "Fonts/GravityRegular5.ttf"
        self.title_box = pygame.Rect(self.SCREEN_WIDTH /2, self.SCREEN_HEIGHT / 10, 256, 64 * 10)
        #self.title_box = UserInterface(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2, 256, 64 * 5, self.__font, self.__font_path, self.hudd, "Start", "Title Screen")
        self.start_game = UserInterface(self.title_box.x, self.title_box.y + (64 * 2), 256, 64, self.__font, self.__font_path, self.hudd, "Start", "New Game" )
        self.preferences = UserInterface(self.title_box.x , self.title_box.y + (64 * 4), 256, 64, self.__font, self.__font_path, self.hudd, "Start", "Preferences" )        
        self.highscore = UserInterface(self.title_box.x, self.title_box.y + (64 * 6), 256, 64, self.__font, self.__font_path, self.hudd, "Start", "HighScore" )        
        self.quit_game = UserInterface(self.title_box.x, self.title_box.y + (64 * 8) , 256, 64, self.__font, self.__font_path, self.hudd, "Start", "Quit" )        
        self.hover = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.start_game, self.preferences, self.highscore, self.quit_game)
        self.updatable.add( self.start_game, self.preferences, self.highscore, self.quit_game)
        self.drawable.add(self.start_game, self.preferences, self.highscore, self.quit_game)
        
    def update(self, dt):
        super().update(dt)
        #self.title_box.get_hudd(self.hudd)
        mouse_pos = pygame.mouse.get_pos()
        self.hover.empty()
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                self.hover.add(button)
                self.drawable.remove(button)
            else:
                self.drawable.add(button)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            new_state = Level1(self.game)
            new_state.enter_state()


            

    def draw(self):
        super().draw()
        for obj in self.hover:
            #create a copy of the rect
            hover_rect = obj.rect.copy()
            hover_rect.inflate_ip(20, 10)
            #pygame.time.set_timer(self.canvas.blit(obj.image, hover_rect), 500)
            self.canvas.blit(obj.image, hover_rect)
        for obj in self.drawable:
            obj.draw()
            self.canvas.blit(obj.image, obj.rect)
        self.screen.blit(self.canvas, (0,0), self.camera.camera_box)

