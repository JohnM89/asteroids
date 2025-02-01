import pygame

#base class for game objects
#extends the pygame Sprite class to also store a position, velocity and radius
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        #check if has class variable containers
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        #set variables for CircleShape class
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.mass = 1.0

    def draw(self, screen):
             #sub class to override
        pass
    
    #rewrite for single function to return true or false & keep game logic in main.py game loop
    def collisions(self, obj):
        distance = pygame.math.Vector2.distance_to(self.position, obj.position)
        return distance <= (self.radius + obj.radius)
            #print("Game Over!")
            #exit()

    #def check_shot(self, obj):
        #distance = pygame.math.Vector2.distance_to(self.position, obj.position)
        #if distance <= (self.radius + obj.radius):
            #obj.kill()
            #self.kill()

    def update(self, dt):
        #sub class to override
        pass
