import pygame
#import all with wildcard (only suitable for small projects)
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
def main():
    #initalize pygame
    pygame.init()
    #utilize Clock object to track time and control framerate
    game_clock = pygame.time.Clock()
    #set delta time variable
    dt = 0
    #set the display properties
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    #create groups to hold objects like player
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    AsteroidField.containers = (updatable)

    Asteroid.containers = (asteroids, updatable, drawable)
    #add groups to Player class containers
    Player.containers = (updatable, drawable)
    asteroidfield = AsteroidField()
    #create new Player object after this update 
    player = Player(x , y)
    

    #game loop
    while True:
        #allow game window to close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #update objects
        updatable.update(dt)
        for obj in asteroids:
            obj.collisions(player)
        #fill screen Surface
        pygame.Surface.fill(screen, (0,0,0))
        #draw objects
        for obj in drawable:
            obj.draw(screen)
        #refresh the screen
        #draw player before refreshing
        pygame.display.flip()
        #pauses game loop until 1/60th of a second has passed
        #also returns delta time since last called
        game_clock.tick(60)
        #get return value from Clock object to track time passed and divide by 1000 to convert from ms to seconds
        dt = game_clock.get_time() / 1000
        




if __name__ == "__main__":
    #possibly better place to call pygame.init?
    #pygame.init()
    main()

