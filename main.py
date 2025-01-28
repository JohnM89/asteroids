import pygame
#import all with wildcard (only suitable for small projects)
from constants import *
from player import Player
def main():
    #initalize pygame
    pygame.init()
    #utilize Clock object to track time and control framerate
    game_clock = pygame.time.Clock()
    #set delta time variable
    dt = 0
    #set the display properties
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting asteroids!")
    #check import success
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x , y)
    #game loop
    while True:
        #allow game window to close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #fill screen Surface
        pygame.Surface.fill(screen, (0,0,0))
        player.update(dt)
        player.draw(screen)
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

