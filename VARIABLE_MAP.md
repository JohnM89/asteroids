# VARIABLE FLOW DIAGRAM

## 🎮 GAME LOOP VARIABLES

```
game.py
├── self.running ────────────► Controls main while loop
├── self.playing ────────────► Controls game.run() loop
├── self.dt ─────────────────► Delta time (passed to all updates)
├── self.state_stack ───────► [Title, Level1, Pause] - Active states
└── self.screen ────────────► Main pygame display surface
```

## 🎯 LEVEL1 STATE VARIABLES

```
levels/level1.py
├── Physics World
│   ├── self.space ─────────► PyMunk physics space (all bodies)
│   └── self.collision_manager ► Routes collision events
│
├── Game State
│   ├── self.score ────────► Player score (updates HUD)
│   ├── self.current_asteroid_count ► Track active asteroids
│   ├── self.current_alien_count ───► Track active enemies
│   └── self.scaling_factor ────────► Difficulty multiplier
│
├── Spawn Control
│   ├── self.max_asteroids ─────────► Asteroid limit
│   ├── self.asteroid_spawn_rate ───► Time between spawns
│   ├── self.alien_max_count ───────► Enemy limit
│   └── self.alien_spawn_rate ──────► Time between enemy spawns
│
├── Sprite Groups
│   ├── self.updatable ─────► All objects needing update()
│   ├── self.drawable ──────► All objects needing draw()
│   ├── self.asteroids ─────► Asteroid sprites only
│   ├── self.shots ─────────► Player bullet sprites
│   ├── self.aliens ────────► Enemy sprites only
│   └── self.ui ────────────► UI elements
│
├── Visual Layers
│   ├── self.canvas ────────► Game world surface (2560x1440)
│   ├── self.screen ────────► Window surface (1280x720)
│   ├── self.camera ────────► Camera following player
│   └── self.background_layer* ► Parallax starfield layers
│
└── HUD Data
    ├── self.hudd ──────────► {"score": 0, "lives": 99, "fuel": 100...}
    └── self.hud_display ───► HeadsUp display object
```

## 🚀 PLAYER VARIABLES

```
entities/player.py
├── Physics Properties
│   ├── self.body.position ─────► (x, y) world coordinates
│   ├── self.body.velocity ─────► Movement vector
│   ├── self.rotation ──────────► Facing angle (radians)
│   └── self.radius ────────────► Collision radius
│
├── Combat Stats
│   ├── self.health ────────────► Hit points (0-100)
│   ├── self.lives ─────────────► Extra lives count
│   ├── self.fuel ──────────────► Thrust fuel (0-100)
│   ├── self.bombs ─────────────► Bomb count
│   ├── self.rockets ───────────► Rocket count
│   ├── self.multishot ─────────► Multishot powerup flag
│   └── self.yamato ────────────► Special weapon count
│
├── Shield System
│   ├── self.shields ───────────► Shield layers count
│   └── self.shields_health ────► Shield hit points (0-100)
│
├── Timers
│   ├── self.timer ─────────────► Shot cooldown timer
│   ├── self.rocket_timer ──────► Rocket cooldown timer
│   ├── self.respawn_timer ─────► Invincibility timer
│   └── self.yamato_timer ──────► Special weapon cooldown
│
├── Visual Effects
│   ├── self.current_colour ────► Flicker during invincibility
│   ├── self.time_since_change ─► Flicker timing
│   └── self.thrust ────────────► Thrust animation object
│
└── References (Dependency Injection)
    ├── self.space ─────────────► Physics world
    ├── self.canvas ────────────► Drawing surface
    ├── self.updatable ─────────► Update group
    ├── self.drawable ──────────► Draw group
    └── self.shots ─────────────► Player bullets group
```

## 💫 ASTEROID VARIABLES

```
entities/asteroid.py
├── Physics
│   ├── self.body.position ─────► World coordinates
│   ├── self.body.velocity ─────► Movement vector
│   └── self.radius ────────────► Size/collision radius
│
├── Visual
│   ├── self.kind ──────────────► Size type (1=small, 2=med, 3=large)
│   ├── self.meteor_types_* ────► Sprite arrays by size
│   ├── self.base_image ────────► Original sprite
│   └── self.sprite_image ──────► Rotated/scaled sprite
│
├── Lifecycle
│   ├── self.time_to_live ──────► Auto-cleanup timer
│   ├── self.damage_accumulated ► Damage tracking
│   └── self.split_threshold ───► Damage needed to split
│
└── References
    ├── self.space ─────────────► Physics world
    └── self.level ─────────────► Level1 instance
```

## 🛸 ENEMY VARIABLES (Flying Saucer Example)

```
entities/enemies/flyingsaucer.py
├── AI State
│   ├── self.max_view_distance ─► Sight range
│   ├── self.ray_cast ──────────► RayCast object for vision
│   └── self.timer ─────────────► Action cooldown
│
├── Visual
│   ├── self.skin ──────────────► Array of sprite variants
│   ├── self.rotation ──────────► Current facing
│   └── self.base_image ────────► Selected sprite
│
└── Inherited from CommonAlien
    ├── self.body.position
    ├── self.radius
    ├── self.health
    └── self.space
```

## 🎨 SPRITE GROUP RELATIONSHIPS

```
OBJECT LIFECYCLE:
Create Entity → Add to Groups → Add to Physics
     │              │               │
     ▼              ▼               ▼
entity = Shot()  updatable.add()  space.add()
                 drawable.add()    (body, shape)
```

## 🔄 UPDATE FLOW

```
game.py: game.run()
   │
   ├── self.dt = get_delta_time()
   │
   ├── handle_events()
   │     └── state_stack[-1].handle_events()
   │
   ├── update(dt)
   │     └── state_stack[-1].update(dt)
   │           └── self.updatable.update(dt)
   │                 ├── player.update(dt)
   │                 ├── asteroid1.update(dt)
   │                 ├── shot1.update(dt)
   │                 └── ... all entities
   │
   └── draw()
         └── state_stack[-1].draw()
               └── self.drawable.draw()
```

## 🎯 COLLISION VARIABLE FLOW

```
COLLISION EVENT:
Body A hits Body B
      │
      ▼
collision_manager.py: route_collision()
      │
      ├── Get collision types from shapes
      ├── Look up handler function
      │
      ▼
Handler Function (e.g., post_solve_s_a)
      │
      ├── arbiter.total_impulse ──► Impact force
      ├── arbiter.contact_point_set.points[0] ──► Where hit occurred
      ├── contact_point.normal ───► Direction of impact
      │
      ▼
Asteroid.split(normal, impulse, contact_point)
      │
      ├── Creates new asteroids
      ├── Calculates split vectors
      └── Updates level.current_asteroid_count
```

## 📊 HUD VARIABLE BINDING

```
level1.py: self.hudd = {
    "score": self.score,           ► Updates from enemy kills
    "lives": self.player.lives,    ► Updates from player damage
    "fuel": self.player.fuel,      ► Updates from thrust usage
    "health": self.player.health,  ► Updates from collisions
    "shields_health": self.player.shields_health
}
     │
     ▼
headsup.py: HeadsUp.update()
     │
     ├── Reads self.hudd values
     ├── Updates progress bars
     └── Renders to HUD surface
```

## 🎮 INPUT VARIABLE FLOW

```
pygame.event.get() ──► events
     │
     ▼
Game.handle_events(events)
     │
     ▼
Current State.handle_events(events)
     │
     ▼ (in Level1)
Player.update() reads pygame.key.get_pressed()
     │
     ├── keys[K_SPACE] ──► player.shoot()
     ├── keys[K_w] ────── ► player.move()
     ├── keys[K_a] ────── ► player.rotate(-1)
     └── keys[K_d] ────── ► player.rotate(1)
```

## 🔧 COMMON VARIABLE PATTERNS

### **Position Sync Pattern**
```
# Physics position → Visual position
self.rect.center = (int(self.body.position.x), int(self.body.position.y))
```

### **Timer Pattern**
```
self.timer -= dt
if self.timer <= 0:
    # Do action
    self.timer = COOLDOWN_TIME  # Reset
```

### **Group Management Pattern**
```
# Add entity to all necessary systems
self.updatable.add(entity)
self.drawable.add(entity)
self.space.add(entity.body, entity.shape)
```

### **Cleanup Pattern**
```
# Remove from ALL systems
entity.kill()  # Removes from sprite groups
self.space.remove(entity.body, entity.shape)  # Remove from physics
```

---

*This diagram shows how data flows between your game systems. Use it to track down where variables come from and where they go.*