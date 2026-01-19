# Ghost Catching Game

A turn-based puzzle game where players place talismans to catch ghosts and direct them into sacred pots.

## Game Overview

**Ghost Catching Game** is an engaging puzzle game that combines strategy and quick thinking. Players must carefully place talismans (magical symbols) to create barriers that guide a ghost into a sacred pot. The ghost will try to escape, so you need to plan your moves wisely!

### Features

- **99 Levels** with progressive difficulty
- **Turn-based gameplay** - You place a talisman, then the ghost moves
- **Smart AI** - The ghost uses intelligent pathfinding to escape
- **Progressive Difficulty:**
  - Levels 1-20 (Easy): Multiple pots and obstacles to help you
  - Levels 21-60 (Medium): Fewer pots and obstacles
  - Levels 61-99 (Hard): Single pot, minimal obstacles
- **Ad-supported** - Free to play with optional ads
- **Mobile optimized** - Built for Android devices

### Game Mechanics

1. **Place Talismans**: Tap on empty grid cells to place talismans
2. **Ghost Movement**: After each talisman placement, the ghost moves one cell
3. **Win Condition**: Guide the ghost into a sacred pot
4. **Lose Condition**: The ghost escapes off the edge of the screen

### Monetization

- **Interstitial Ads**: Full-screen ads appear after completing each level
- **Rewarded Video Ads**: Optional video ads for:
  - Undoing the last 3 moves when stuck
  - Skipping a difficult level (after 3 failed attempts)

## Installation & Development

### Requirements

- Python 3.8+
- Pygame 2.1.0+
- Kivy 2.1.0+ (for Android build)
- Buildozer 1.4.0+ (for Android packaging)

### Desktop Development

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python3 main.py
   ```

### Android Build

1. Install Buildozer:
   ```bash
   pip install buildozer
   ```

2. Set up Android SDK and NDK (first time only):
   ```bash
   buildozer android debug
   ```
   This will automatically download and configure the necessary tools.

3. Build the APK:
   ```bash
   buildozer android release
   ```

4. The APK will be generated in the `bin/` directory

### Google Play Store Deployment

1. **Create Google Play Developer Account**
   - Visit https://play.google.com/apps/publish
   - Pay the one-time registration fee ($25)

2. **Prepare App Listing**
   - App name: "Ghost Catching Game"
   - Description: See `GOOGLE_PLAY_DESCRIPTION.md`
   - Screenshots: Place in `assets/screenshots/`
   - Icon: Place in `assets/icon.png`
   - Feature graphic: Place in `assets/feature_graphic.png`

3. **Set Up AdMob**
   - Create AdMob account at https://admob.google.com
   - Create Ad Unit IDs for:
     - Interstitial Ads
     - Rewarded Video Ads
   - Add these IDs to `src/ad_manager.py`

4. **Upload to Google Play**
   - Sign the APK with your keystore
   - Upload to Google Play Console
   - Fill in all required information
   - Submit for review

## File Structure

```
ghost_catching_game/
├── main.py                 # Main game engine
├── buildozer.spec          # Android build configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   └── ad_manager.py      # AdMob integration
├── assets/
│   ├── icon.png           # App icon
│   ├── presplash.png      # Splash screen
│   ├── feature_graphic.png # Google Play feature graphic
│   └── screenshots/       # Google Play screenshots
└── levels/
    └── level_data.json    # Level configurations (optional)
```

## Game Design Document

### Level Progression

- **Easy (Levels 1-20)**: 3-5 pots, 5-8 obstacles, large grid
- **Medium (Levels 21-60)**: 2-4 pots, 2-5 obstacles, medium grid
- **Hard (Levels 61-99)**: 1 pot, 0-2 obstacles, large grid

### Ghost AI

The ghost uses a scoring algorithm to determine its next move:
1. Avoid pots (high priority)
2. Move towards the edge of the screen
3. Choose the path that maximizes escape chances

### Talisman System

- Each talisman acts as a permanent barrier
- Talismans cannot be removed once placed
- Limited number of talismans per level (increases with difficulty)

## Controls

### Desktop
- **Mouse Click**: Place talisman on grid
- **R Key**: Restart current level
- **ESC Key**: Return to menu

### Mobile (Android)
- **Tap**: Place talisman on grid
- **Swipe Down**: Restart level (optional)
- **Back Button**: Return to menu

## Troubleshooting

### Game crashes on startup
- Ensure Pygame is properly installed: `pip install --upgrade pygame`
- Check Python version: `python3 --version` (should be 3.8+)

### Android build fails
- Clear build cache: `buildozer android clean`
- Ensure Java is installed: `java -version`
- Check Android SDK path in buildozer.spec

### AdMob ads not showing
- Verify Ad Unit IDs are correct in `src/ad_manager.py`
- Ensure app is signed with release keystore
- Test ads may take 24 hours to appear

## Performance Optimization

- Grid size: 20x25 cells (800x1000 pixels)
- Rendering: 60 FPS
- Ghost AI: Calculated once per turn
- Memory usage: ~50MB on Android devices

## Future Enhancements

- Power-ups (freeze ghost, extra talismans, etc.)
- Daily challenges
- Leaderboards
- Multiplayer mode
- Sound effects and music
- Different ghost types with unique AI

## License

This game is created for Google Play Store distribution.

## Support & Feedback

For issues or suggestions, please contact the developer through Google Play Store.

## Credits

Developed with:
- Pygame (game engine)
- Kivy (Android framework)
- Buildozer (Android packaging)

---

**Happy Ghost Catching!** 👻
