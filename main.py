import pygame
from constants import *
def main():
    #initalize pygame
    pygame.init()
    #set the display properties
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    #game loop
    while True:
        #allow game window to close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        #fill screen Surface
        pygame.Surface.fill(screen, (0,0,0))
        #refresh the screen
        pygame.display.flip()




if __name__ == "__main__":
    #pygame.init()
    main()

