SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GAME_WIDTH = SCREEN_WIDTH 
GAME_HEIGHT = SCREEN_HEIGHT 

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8 #seconds
ASTEROID_TTL = 10.0
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
MAX_ASTEROIDS = 20

ALIEN_MIN_RADIUS = 20
ALIEN_KINDS = 3
ALIEN_SPAWN_RATE = 20.0
ALIEN_TTL = 20.0
ALIEN_MAX_RADIUS = ALIEN_MIN_RADIUS * ALIEN_KINDS
ALIEN_MAX_COUNT = 3
MAX_ALIENS = 5

#TODO
#set object masks
PLAYER_CATEGORY = 0b000010
ASTEROID_CATEGORY = 0b000001
ENEMY_CATEGORY = 0b000100   
PLAYER_BULLET_CATEGORY = 0b001000  
ENEMY_BULLET_CATEGORY = 0b010000  
WALL_CATEGORY = 0b100000   

PLAYER_MASK = 0b010101 
ASTEROID_MASK = 0b011111    
ENEMY_MASK = 0b101011   
PLAYER_BULLET_MASK = 0b000101  
ENEMY_BULLET_MASK = 0b000001
WALL_MASK = 0b000100  

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 300
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3
PLAYER_RESPAWN_TIMER = 2.5
FLASH_INTERVAL = 0.2
PLAYER_COLOUR = (255, 255, 255)
FLICKER_COLOUR = (255, 0 ,0)
DRAG_COEFFICENT = 0.99
ACCELERATION = 300

SHOT_RADIUS = 5

#uibox margins 
MARGIN_PERCENT = 5
HORIZONTAL_MARGIN = SCREEN_WIDTH * (MARGIN_PERCENT / 100)
VERTICAL_MARGIN = SCREEN_HEIGHT * (MARGIN_PERCENT / 100)

GRAVITY_CONSTANT = 100

