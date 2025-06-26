from .constants import *
import pygame

class Camera():
    def __init__(self, screen, canvas):
        self.screen = screen
        self.canvas = canvas 
        self.camera_box = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) 
        self.canvas_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.deadzone = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 200)
        self.start = True


    def update_camera(self, target):
        if target:
            if self.start == True:

            #print(target)
                self.camera_box.center = target.rect.center
                self.start = False
            dx = target.rect.centerx - self.camera_box.x    
            dy = target.rect.centery - self.camera_box.y
            #self.camera_box.center = target.rect.center
            if dx < self.deadzone.left:
                self.camera_box.x -= self.deadzone.left - dx
            elif dx > self.deadzone.right:
                self.camera_box.x += dx - self.deadzone.right   

            if dy < self.deadzone.top:
                self.camera_box.y -= self.deadzone.top - dy 
            elif dy > self.deadzone.bottom:
                self.camera_box.y += dy - self.deadzone.bottom
            #target.rect.move(-self.camera_box.x, -self.camera_box.y)
            #self.camera_box.center = (target.rect.x, target.rect.y)
            #print(self.camera_box.center)
            self.camera_box.x = max(0, min(self.camera_box.x, self.canvas.get_width() - self.screen.get_width()))  
            self.camera_box.y = max(0, min(self.camera_box.y, self.canvas.get_height() - self.screen.get_height()))
        else:
            self.camera_box.center = self.canvas_rect.center

    def apply(self, entity):
        return entity.rect.move(-self.camera_box.x, -self.camera_box.y)
        
        


