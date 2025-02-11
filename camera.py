from constants import *
import pygame

class Camera():
    def __init__(self, screen, canvas):
        self.screen = screen
        self.canvas = canvas 
        self.camera_box = pygame.Rect(0, 0, screen.get_width(), screen.get_height()) 
        self.canvas_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        #deadzone.y  



    def update_camera(self, target):
        if target:
            #print(target)
            self.camera_box.center = target.rect.center
            #print(self.camera_box.center)
        #self.camera_box.x = max(0, min(self.camera_box.x, self.canvas.get_width() - self.screen.get_width()))  
        #self.camera_box.y = max(0, min(self.camera_box.y, self.camera_box.get_height() - self.screen.get_height()))
        else:
            self.camera_box.center = self.canvas_rect.center

    def apply(self, entity):
        return entity.rect.move(-self.camera_box.x, -self.camera_box.y)
        
        


