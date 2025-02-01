import pygame
#import all with wildcard (only suitable for small projects)
from constants import *
from player import Player
from shot import Shot
from asteroid import Asteroid
from userinterface import UserInterface
from asteroidfield import AsteroidField
from font import FontManager
def main():
    #initalize pygame
    pygame.init()
    #utilize default font for time being
    #font_manager = FontManager()
    #font_manager.load_font("GravityRegular5", "Fonts/GravityRegular5.ttf", 24)
    #utilize Clock object to track time and control framerate
    game_clock = pygame.time.Clock()
    #set delta time variable
    dt = 0
    hudd = {"score": 0, "lives": 3}
    #set a simple scoring mechanic (using constant)
    #score_display = default_font.render(f"{score}", True, (0, 0, 0))
    #set the display properties
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    
    #create groups to hold objects like player
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    uibar = pygame.sprite.Group()
    UserInterface.containers = (uibar, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    #add groups to Player class containers
    Player.containers = (updatable, drawable)
    asteroidfield = AsteroidField()
    #uibarbottom = UserInterface()
    #placeholder uibar for score
    uibarbottom = UserInterface((SCREEN_WIDTH - SCREEN_WIDTH / 8) - (HORIZONTAL_MARGIN / 6), (SCREEN_HEIGHT - 64) - (VERTICAL_MARGIN / 4), SCREEN_WIDTH / 8, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", hudd, "lives", "Lives: ")
    uibartop = UserInterface(HORIZONTAL_MARGIN / 6, VERTICAL_MARGIN / 4, SCREEN_WIDTH / 8, 64, "GravityRegular5", "Fonts/GravityRegular5.ttf", hudd, "score", "Score: ")
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
        #get hud data
        for sprite in uibar:
            if hasattr(sprite, 'get_hudd'):
                sprite.get_hudd(hudd)
        #check for collisions
        for obj in asteroids:
            #keep game logic in loop and keep object dynamic
            if obj.collisions(player):
                #if player has more than 0 lives, on collision reset to center
                if player.lives > 0:
                    #prevent multiple lost lives in short span with spawn timer
                    if player.respawn_timer <= 0:
                        player.lives -= 1
                        player.respawn_timer = PLAYER_RESPAWN_TIMER
                        player.respawn_flash = True
                        hudd["lives"] = player.lives
                        player.position = pygame.Vector2(x , y)
        
                else:
                    print("Game Over!")
                    print(f"You scored: {hudd['score']}")
                    exit()
            for shot in shots:
                if obj.collisions(shot):
                    shot.kill()
                    hudd["score"] += 1
                    obj.split()
        
        #fill screen Surface
        pygame.Surface.fill(screen, (0,0,0))
        #font_manager.render_text(screen , f"{score}", "GravityRegular5", (255, 255, 255), (50, 50))
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

