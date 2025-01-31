import pygame

class SquareShape(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pass    

    def update(self, dt):
        pass
