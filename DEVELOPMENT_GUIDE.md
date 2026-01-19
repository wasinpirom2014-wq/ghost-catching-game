# Ghost Catching Game - Development Guide

This guide explains the architecture and how to extend the game.

## Project Structure

```
ghost_catching_game/
├── main.py                          # Main game engine
├── buildozer.spec                   # Android build configuration
├── requirements.txt                 # Python dependencies
├── README.md                        # User documentation
├── DEVELOPMENT_GUIDE.md             # This file
├── GOOGLE_PLAY_DESCRIPTION.md       # App Store listing
├── GOOGLE_PLAY_UPLOAD_GUIDE.md      # Upload instructions
├── android_manifest_template.xml    # Android manifest template
├── src/
│   ├── __init__.py                  # Package initialization
│   ├── config.py                    # Game configuration
│   ├── ad_manager.py                # AdMob integration
│   ├── analytics.py                 # Analytics (future)
│   ├── sound_manager.py             # Sound effects (future)
│   └── particle_system.py           # Particle effects (future)
├── assets/
│   ├── icon.png                     # App icon (512x512)
│   ├── presplash.png                # Splash screen
│   ├── feature_graphic.png          # Google Play feature
│   ├── screenshots/                 # Google Play screenshots
│   ├── audio/
│   │   ├── background.mp3           # Background music
│   │   ├── talisman.wav             # Talisman placement sound
│   │   ├── ghost_move.wav           # Ghost movement sound
│   │   ├── level_complete.wav       # Level complete sound
│   │   └── level_failed.wav         # Level failed sound
│   └── fonts/
│       └── game_font.ttf            # Custom font (optional)
└── levels/
    └── level_data.json              # Level configurations (future)
```

## Core Classes

### Game Class
Main game loop and state management.

```python
class Game:
    def __init__(self)              # Initialize game
    def load_level(level_num)       # Load specific level
    def handle_events()             # Process user input
    def handle_game_click(pos)      # Handle grid clicks
    def check_game_state()          # Check win/lose conditions
    def draw()                      # Render game
    def run()                       # Main game loop
```

### Level Class
Represents a single game level.

```python
class Level:
    def __init__(level_num)         # Create level
    def generate_level()            # Generate level layout
```

### GameGrid Class
Manages the game grid and cell states.

```python
class GameGrid:
    def set_cell(pos, cell_type)    # Set cell type
    def get_cell(pos)               # Get cell type
    def is_valid_placement(pos)     # Check if placement is valid
```

### Ghost Class
Represents the ghost with AI pathfinding.

```python
class Ghost:
    def move_ai(grid, pot_positions) # AI movement logic
    def get_valid_moves(grid)       # Get possible moves
```

### Position Class
Represents a grid position.

```python
class Position:
    def distance_to(other)          # Calculate distance
```

## Game Flow

```
1. Game Initialization
   ├── Create game window
   ├── Load level 1
   └── Enter main loop

2. Main Game Loop
   ├── Handle Events
   │   ├── Mouse click on grid
   │   ├── Keyboard input (R, ESC)
   │   └── Window close
   ├── Update Game State
   │   ├── Place talisman if clicked
   │   ├── Move ghost
   │   └── Check win/lose conditions
   └── Render
       ├── Draw grid
       ├── Draw entities
       └── Draw UI

3. Level Completion
   ├── Show "Level Complete" screen
   ├── Show interstitial ad
   └── Load next level

4. Level Failure
   ├── Show "Ghost Escaped" screen
   ├── Offer retry or reward ad
   └── Restart level or continue
```

## Ghost AI Algorithm

The ghost uses a scoring system to determine its next move:

```python
def move_ai(grid, pot_positions):
    valid_moves = get_valid_moves(grid)
    
    for each move:
        # Score 1: Distance from pots (maximize)
        min_pot_distance = min distance to any pot
        
        # Score 2: Distance from center (maximize)
        distance_from_center = distance to grid center
        
        # Score 3: Distance from edges (minimize)
        distance_from_edge = min distance to any edge
        
        # Combined score
        score = (
            min_pot_distance * 2 +
            distance_from_edge * -1
        )
    
    # Choose move with highest score
    best_move = move with highest score
    ghost.pos = best_move
```

## How to Extend the Game

### Add New Level Difficulty

1. Edit `src/config.py`:
```python
LEVEL_CONFIG = {
    'extreme': {
        'range': (100, 150),
        'min_pots': 1,
        'max_pots': 1,
        'min_obstacles': 0,
        'max_obstacles': 1,
        'base_talismans': 35,
        'talisman_per_level': 1.0,
    },
}
```

2. Update `TOTAL_LEVELS` in config.py

### Add Sound Effects

1. Place audio files in `assets/audio/`
2. Create `src/sound_manager.py`:
```python
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
    
    def load_sound(name, path):
        self.sounds[name] = pygame.mixer.Sound(path)
    
    def play_sound(name):
        self.sounds[name].play()
```

3. Integrate into main.py:
```python
self.sound_manager = SoundManager()
self.sound_manager.play_sound('talisman_place')
```

### Add Particle Effects

1. Create `src/particle_system.py`:
```python
class Particle:
    def __init__(pos, velocity, lifetime):
        self.pos = pos
        self.velocity = velocity
        self.lifetime = lifetime
    
    def update(dt):
        self.pos += self.velocity * dt
        self.lifetime -= dt

class ParticleSystem:
    def emit(pos, count):
        # Create particles
        pass
    
    def update(dt):
        # Update all particles
        pass
    
    def draw(screen):
        # Draw all particles
        pass
```

### Add Power-ups

1. Create new CellType:
```python
class CellType(Enum):
    FREEZE_GHOST = 5  # Freezes ghost for 1 turn
    EXTRA_TALISMAN = 6  # Gives extra talisman
    REVEAL_PATH = 7  # Shows ghost's next move
```

2. Add power-up logic to Level class:
```python
def apply_powerup(powerup_type):
    if powerup_type == CellType.FREEZE_GHOST:
        self.ghost_frozen = True
        self.freeze_duration = 1
```

### Add Leaderboard

1. Create `src/leaderboard.py`:
```python
class Leaderboard:
    def save_score(level, time, talismans_used):
        # Save to local storage or cloud
        pass
    
    def get_top_scores(level):
        # Retrieve top scores
        pass
```

2. Integrate into Game class:
```python
self.leaderboard = Leaderboard()
self.leaderboard.save_score(
    self.current_level,
    time_taken,
    self.level.talisman_count
)
```

### Add Analytics

1. Create `src/analytics.py`:
```python
class Analytics:
    def track_level_complete(level, time, talismans):
        # Send analytics event
        pass
    
    def track_ad_shown(ad_type):
        # Track ad impressions
        pass
```

### Add Multiplayer

1. Create `src/multiplayer.py`:
```python
class MultiplayerGame:
    def __init__(player1, player2):
        self.players = [player1, player2]
        self.current_player = 0
    
    def switch_player():
        self.current_player = 1 - self.current_player
    
    def check_winner():
        # Determine winner
        pass
```

## Testing

### Unit Tests

Create `tests/test_game.py`:
```python
import unittest
from main import Game, Ghost, GameGrid, Position

class TestGhost(unittest.TestCase):
    def test_valid_moves(self):
        grid = GameGrid(20, 25)
        ghost = Ghost(Position(10, 10))
        moves = ghost.get_valid_moves(grid)
        self.assertEqual(len(moves), 4)  # Up, down, left, right
    
    def test_ghost_trapped(self):
        # Test ghost trapped by talismans
        pass

class TestGameGrid(unittest.TestCase):
    def test_cell_placement(self):
        grid = GameGrid(20, 25)
        pos = Position(5, 5)
        grid.set_cell(pos, CellType.TALISMAN)
        self.assertEqual(grid.get_cell(pos), CellType.TALISMAN)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest tests/test_game.py
```

### Manual Testing Checklist

- [ ] Game starts without errors
- [ ] Level 1 loads correctly
- [ ] Talisman placement works
- [ ] Ghost moves correctly
- [ ] Win condition triggers
- [ ] Lose condition triggers
- [ ] Level progression works
- [ ] All 99 levels load
- [ ] Ads display (test mode)
- [ ] UI is responsive
- [ ] No crashes on edge cases

## Performance Optimization

### Memory Usage
- Cache level data after generation
- Use object pooling for particles
- Limit simultaneous animations

### CPU Usage
- Optimize ghost AI pathfinding
- Use dirty rectangle rendering
- Cache grid calculations

### Rendering
- Use hardware acceleration
- Minimize draw calls
- Optimize asset sizes

## Debugging

Enable debug mode in `src/config.py`:
```python
DEBUG_CONFIG = {
    'enabled': True,
    'show_grid_numbers': True,
    'show_ghost_ai_debug': True,
    'show_fps': True,
}
```

## Common Issues

### Game runs slowly
- Reduce FPS in config
- Disable particle effects
- Optimize asset sizes

### Ghost AI behaves unexpectedly
- Check scoring algorithm
- Verify valid moves calculation
- Debug with grid numbers enabled

### Ads not showing
- Verify Ad Unit IDs
- Check AdMob account status
- Test with test ads first

### App crashes on Android
- Check logcat: `adb logcat`
- Verify permissions in manifest
- Test on multiple devices

## Build & Deploy

### Development Build
```bash
buildozer android debug
adb install -r bin/ghostcatchinggame-debug.apk
```

### Release Build
```bash
buildozer android release
# Sign APK (see GOOGLE_PLAY_UPLOAD_GUIDE.md)
```

### Clean Build
```bash
buildozer android clean
buildozer android release
```

## Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Android Development](https://developer.android.com/)
- [Google Play Console Help](https://support.google.com/googleplay/android-developer)

## Version History

### v1.0.0 (Initial Release)
- 99 levels
- Turn-based gameplay
- Ghost AI
- Interstitial ads
- Rewarded ads

### v1.1.0 (Planned)
- Sound effects
- Particle effects
- Power-ups
- Achievements

### v2.0.0 (Future)
- Multiplayer mode
- Leaderboards
- Daily challenges
- Custom themes

---

Happy developing! 🎮
