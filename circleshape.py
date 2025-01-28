import pygame

#base class for game objects
#extends the pygame Sprite class to also store a position, velocity and radius
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
             #sub class to override
        pass

    def update(self, dt):
        #sub class to override
        pass
