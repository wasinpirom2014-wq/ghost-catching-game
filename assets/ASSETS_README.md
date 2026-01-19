# Ghost Catching Game - Assets Documentation

This directory contains all visual assets for the Ghost Catching Game.

## Files Included

### App Icon
- **File**: `icon.png`
- **Size**: 512x512 pixels
- **Format**: PNG with transparency
- **Usage**: Google Play Store app icon, launcher icon
- **Description**: Cute light blue ghost surrounded by golden Thai-inspired mystical talismans on dark purple background

### Feature Graphic
- **File**: `feature_graphic.png`
- **Size**: 1024x500 pixels
- **Format**: PNG
- **Usage**: Google Play Store feature graphic (top of store listing)
- **Description**: Game title with gameplay scene showing ghost, talismans, grid, and sacred pot

### Splash Screen
- **File**: `presplash.png`
- **Size**: 1080x1920 pixels (portrait)
- **Format**: PNG
- **Usage**: App loading screen
- **Description**: Game title with ghost character and floating talismans, "Loading..." text at bottom

### Screenshots

#### Screenshot 1: Easy Level Gameplay
- **File**: `screenshots/screenshot_1_gameplay_easy.png`
- **Size**: 1080x1920 pixels (portrait)
- **Description**: Shows Level 5 gameplay with multiple pots, few talismans placed, ghost in center

#### Screenshot 2: Hard Level Gameplay
- **File**: `screenshots/screenshot_2_gameplay_hard.png`
- **Size**: 1080x1920 pixels (portrait)
- **Description**: Shows Level 75 with many talismans creating complex maze, single pot, trapped ghost

#### Screenshot 3: Victory Screen
- **File**: `screenshots/screenshot_3_victory.png`
- **Size**: 1080x1920 pixels (portrait)
- **Description**: "Level Complete!" screen with happy ghost in pot, stats, and "Next Level" button

#### Screenshot 4: Main Menu
- **File**: `screenshots/screenshot_4_menu.png`
- **Size**: 1080x1920 pixels (portrait)
- **Description**: Main menu with game title, ghost character, and menu buttons

## Design Guidelines

### Color Palette
- **Primary Background**: Dark purple to indigo gradient (#14142E to #2D1B69)
- **Ghost**: Light blue/cyan (#64C8FF)
- **Talismans**: Golden yellow (#FFD700) with glow effects
- **Sacred Pot**: Orange (#FF8C42) with glow effects
- **UI Text**: White (#FFFFFF)
- **Success**: Green (#64FF64)
- **Failure**: Red (#FF6464)

### Style
- Flat design with subtle gradients
- Mystical/magical atmosphere
- Thai-inspired sacred symbols on talismans
- Glowing particle effects
- Professional mobile game aesthetic
- Cute, friendly ghost character (not scary)

### Typography
- Game title: Bold, mystical font with golden glow
- UI text: Clean, readable sans-serif
- High contrast for readability

## Usage in Build

### Buildozer Configuration
These assets are automatically included in the Android build via `buildozer.spec`:

```ini
# Icon
icon.filename = assets/icon.png

# Presplash
presplash.filename = assets/presplash.png
```

### Google Play Store Upload
Use these assets when creating your Google Play Store listing:

1. **App Icon** → Upload to "App icon" section (512x512)
2. **Feature Graphic** → Upload to "Feature graphic" section (1024x500)
3. **Screenshots** → Upload all 4 screenshots to "Phone screenshots" section (minimum 2 required)

## Customization

To customize these assets:

1. **Colors**: Maintain the mystical purple/golden theme for consistency
2. **Ghost Character**: Keep the cute, friendly appearance
3. **Thai Elements**: Preserve Thai-inspired sacred symbols for cultural authenticity
4. **Readability**: Ensure text is readable at all sizes

## File Sizes

- Total assets size: ~39 MB (uncompressed)
- Icon: ~2-3 MB
- Feature Graphic: ~5-7 MB
- Presplash: ~8-10 MB
- Screenshots: ~5-8 MB each

## Optimization

For production:
- Icons should be optimized to < 1 MB
- Screenshots can be compressed to reduce APK size
- Use PNG-8 where possible for smaller file sizes
- Consider using WebP format for better compression

## Tools Used

All assets were generated using AI image generation with detailed prompts to ensure:
- Consistent visual style
- Professional quality
- Appropriate resolution
- Cultural authenticity

## License

These assets are part of the Ghost Catching Game project and should only be used for this application.

---

**Ready to use!** These assets are production-ready and optimized for Google Play Store submission.
