# ASTEROIDS GAME - CODEBASE CHEAT SHEET

## 🔍 QUICK REFERENCE

### **Entry Point**
- **Main File**: `game.py` - Creates Game instance and runs main game loop
- **Start State**: `menus/title.py` - First screen that loads

### **Core Architecture**
- **State Pattern**: Uses state stack with `game/state.py` base class
- **Physics**: PyMunk physics engine for realistic collisions
- **Graphics**: Pygame with layered sprite groups and custom canvas/camera system

---

## 📁 FILE STRUCTURE BREAKDOWN

### **game/** - Core Systems
- `game.py` - Main game class with game loop
- `state.py` - Base State class (all screens inherit from this)
- `constants.py` - ALL GAME CONSTANTS (physics, collision categories, etc.)
- `collision_manager.py` - Unified collision handling system
- `camera.py` - Camera following with deadzone
- `headsup.py` - HUD display (health bars, fuel, etc.)
- `userinterface.py` - UI component class

### **entities/** - Game Objects
- `circleshape.py` - Base class for physics objects
- `player.py` - Player ship with controls and weapons
- `asteroid.py` - Asteroids that split when destroyed
- `shot.py` - Player bullets
- `pickup.py` - Power-ups (fuel, bombs, shields, etc.)
- `enemies/` - Enemy types (aliens, centipedes, etc.)

### **menus/** - UI Screens
- `title.py` - Title screen with meteor animation
- `startmenu.py` - Character selection
- `pause.py` - Pause overlay
- `game_over.py` - Game over screen

### **levels/** - Game Levels
- `level1.py` - Main gameplay level
- `spawner.py` - Universal spawning system for entities

### **effects/** - Visual Effects
- `explosions/` - Various explosion animations
- `debris.py` - Asteroid debris particles

---

## 🎮 CONTROLS & PLAYER MECHANICS

### **Player Controls** (in `entities/player.py`)
- **W** - Thrust forward (consumes fuel)
- **S** - Thrust backward
- **A/D** - Rotate left/right
- **SPACE** - Shoot bullets
- **M** - Multishot (if powerup collected)
- **R** - Fire rocket (if rockets available)
- **B** - Drop bomb (if bombs available)
- **P** - Pause game

### **Player Stats**
```python
self.lives = 1
self.health = 100
self.fuel = 100
self.bombs = 99
self.rockets = 99
self.shields = 1
self.shields_health = 100
```

---

## 🏗️ CORE SYSTEMS

### **State Management**
```python
# State stack in game.py
self.state_stack = []
# States can enter/exit
new_state.enter_state()  # Pushes to stack
self.exit_state()       # Pops from stack
```

### **Physics & Collisions**
- **PyMunk Space**: `level.space` handles all physics
- **Collision Categories**: Defined in `constants.py` (bitmasks)
- **Collision Manager**: `collision_manager.py` routes collision events

### **Collision Types** (constants.py)
```python
PLAYER_CATEGORY = 0b0000100000      # Type 1
ASTEROID_CATEGORY = 0b0000010000    # Type 2
ENEMY_CATEGORY = 0b0001000000       # Type 5
PLAYER_BULLET_CATEGORY = 0b0010000000  # Type 3
```

### **Spawning System**
- **Universal Spawner**: `levels/spawner.py`
- Handles asteroids, enemies, any entity type
- Spawns from screen edges with random velocities

---

## 🎯 COLLISION SYSTEM

### **Collision Registration** (in `levels/level1.py`)
```python
# Format: register(type_a, type_b, handler_function)
self.collision_manager.register(1, 2, self.post_solve_p_a)  # Player-Asteroid
self.collision_manager.register(2, 3, self.post_solve_s_a)  # Shot-Asteroid
self.collision_manager.register(1, 4, self.begin_p_p, phase="begin")  # Player-Pickup
```

### **Key Collision Handlers**
- `post_solve_p_a` - Player hits asteroid (damage player)
- `post_solve_s_a` - Shot hits asteroid (split asteroid)
- `post_solve_s_e` - Shot hits enemy (damage enemy)
- `begin_p_p` - Player collects pickup (add to inventory)

---

## 🔧 COMMON PATTERNS

### **Sprite Creation Pattern**
```python
# 1. Create entity
entity = SomeEntity(x, y, params)
# 2. Add to groups
self.updatable.add(entity)
self.drawable.add(entity)
# 3. Add to physics space
self.space.add(entity.body, entity.shape)
```

### **Animation Pattern** (used in shots, explosions)
```python
self.frame_timer += dt
if self.frame_timer > self.frame_interval:
    self.frame += 1
    if self.frame >= self.max_frame:
        self.kill()  # Remove when animation ends
```

### **Time-To-Live Pattern**
```python
self.time_to_live -= dt
if self.time_to_live <= 0:
    self.kill()
    self.space.remove(self.body, self.shape)
```

---

## 🎨 GRAPHICS SYSTEM

### **Layered Rendering**
1. **Background** - Parallax starfield layers
2. **Canvas** - Game world (2x screen size for camera movement)
3. **Camera** - Follows player with deadzone
4. **HUD** - Fixed overlay (health, fuel, score)

### **Canvas vs Screen**
- **GAME_WIDTH/HEIGHT** = 2560x1440 (canvas size)
- **SCREEN_WIDTH/HEIGHT** = 1280x720 (window size)
- Camera shows portion of canvas on screen

---

## 🔑 KEY VARIABLES

### **Game State**
- `game.state_stack` - Current active states
- `game.dt` - Delta time for frame-rate independent updates

### **Level State**
- `level.score` - Current player score
- `level.current_asteroid_count` - Active asteroids
- `level.current_alien_count` - Active enemies
- `level.space` - PyMunk physics space

### **Player State**
- `player.body.position` - Player world position
- `player.rotation` - Current facing direction
- `player.timer` - Shooting cooldown
- `player.respawn_timer` - Invincibility after hit

---

## 💥 DAMAGE SYSTEM

### **Impact Damage** (in `level1.py`)
```python
def impact_damage_check(self, impact_force):
    if impact_force >= IMPACT_THRESHOLD:
        damage = max(min(impact_force * IMPACT_NORMALIZER, MAX_IMPACT_DAMAGE), MIN_IMPACT_DAMAGE)
        return damage
```

### **Player Health System**
1. **Shields** - Absorb damage first
2. **Health** - Direct damage when shields down
3. **Lives** - Reset health when depleted

---

## 🚀 ENTRY POINTS FOR COMMON TASKS

### **Add New Enemy Type**
1. Create class in `entities/enemies/`
2. Inherit from `CircleShape` or `CommonAlien`
3. Set collision_type and collision masks
4. Add to spawn list in `level1.py`

### **Add New Weapon**
1. Create entity class (inherit `CircleShape`)
2. Add shooting method to `player.py`
3. Bind to key in `player.update()`
4. Register collision handlers

### **Add New Powerup**
1. Create class in `entities/pickup.py`
2. Add pickup logic in `level1.begin_p_p()`
3. Add to drop list in `level1.create_drop()`

### **Add New Menu**
1. Create class inheriting `State`
2. Implement `update()`, `draw()`, `handle_events()`
3. Add state transitions in other menus

---

## 🐛 DEBUGGING HELPERS

### **Physics Debug**
- Collision types printed during registration
- Impact force printed in collision handlers
- Body removal tracked in asteroids

### **Common Issues**
- **Memory Leaks**: Always remove from both sprite groups AND physics space
- **Collision Misses**: Check collision categories/masks in constants.py
- **State Issues**: Ensure proper enter_state()/exit_state() calls

---

## 📦 DEPENDENCIES

### **Physics**
- **PyMunk** - 2D physics simulation
- Bodies, shapes, space, constraints

### **Graphics**
- **Pygame** - Rendering and input
- Surfaces, rects, sprite groups

### **Asset Loading**
- Images loaded from `./assets/`
- Fonts from `./assets/fonts/`
- Sprites organized by type

---

## ⚡ PERFORMANCE NOTES

### **Optimization Patterns**
- `convert_alpha()` called on loaded images
- Sprite groups for batch operations
- Time-based culling (TTL on entities)
- Boundary checking for cleanup

### **Resource Management**
- Physics bodies removed when sprites killed
- Animation frames cleaned up automatically
- Spawner limits prevent runaway creation

---

## 🔄 GAME LOOP FLOW

1. **Handle Events** - Input processing
2. **Update** - All game logic, physics step
3. **Draw** - Render to canvas, blit to screen
4. **Delta Time** - Frame-rate independent timing

### **State Update Chain**
`Game.update()` → `Current State.update()` → `sprite groups.update()`

---

## 💡 QUICK TIPS

- **Start Here**: Look at `level1.py` for main game logic
- **Physics Issues**: Check `collision_manager.py` registration
- **New Entities**: Use `CircleShape` as base class
- **UI Elements**: Use `UserInterface` or `HeadsUp` classes
- **Constants**: Everything configurable is in `constants.py`
- **State Debugging**: Print `game.state_stack` to see active states

---

*Last Updated: Based on codebase analysis - focus on these core systems for quick navigation during 25-minute coding sessions*