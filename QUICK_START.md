# Ghost Catching Game - Quick Start Guide

Get your game running in minutes!

## 1. Install Dependencies (5 minutes)

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python3 -c "import pygame; print('Pygame OK')"
```

## 2. Run the Game (2 minutes)

```bash
# Navigate to project directory
cd /home/ubuntu/ghost_catching_game

# Run the game
python3 main.py
```

**Controls:**
- **Click on grid**: Place talisman
- **R key**: Restart level
- **ESC key**: Return to menu
- **Close window**: Exit game

## 3. Build for Android (30 minutes - first time only)

```bash
# Install Buildozer
pip install buildozer

# Navigate to project directory
cd /home/ubuntu/ghost_catching_game

# Build debug APK (first time - downloads SDK/NDK)
buildozer android debug

# APK location: bin/ghostcatchinggame-debug.apk
```

## 4. Test on Android Device

```bash
# Install Android SDK Platform Tools
# Download from: https://developer.android.com/studio/releases/platform-tools

# Connect your Android device via USB
# Enable USB debugging on device

# Install APK
adb install -r bin/ghostcatchinggame-debug.apk

# Run app
adb shell am start -n org.ghostcatching.ghostcatchinggame/.MainActivity
```

## 5. Prepare for Google Play (1 hour)

### Create Assets

1. **Icon** (512x512 PNG)
   - Place in `assets/icon.png`
   - Should be colorful and recognizable

2. **Feature Graphic** (1024x500 PNG)
   - Place in `assets/feature_graphic.png`
   - Shows at top of store listing

3. **Screenshots** (1080x1920 PNG, minimum 2)
   - Place in `assets/screenshots/`
   - Show gameplay, levels, UI

### Set Up AdMob

1. Go to https://admob.google.com
2. Create new app
3. Create Ad Unit IDs:
   - Interstitial Ad
   - Rewarded Ad
4. Update `src/ad_manager.py` with your Ad Unit IDs

### Create Keystore

```bash
# Generate keystore (do this once!)
keytool -genkey -v -keystore ghost_catching_game.keystore \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -alias ghostcatching

# Save this file in a safe location!
```

## 6. Build Release APK

```bash
# Build release APK
buildozer android release

# Sign APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
    -keystore ghost_catching_game.keystore \
    bin/ghostcatchinggame-1.0.0-release.apk ghostcatching

# Align APK
zipalign -v 4 bin/ghostcatchinggame-1.0.0-release.apk \
    bin/ghostcatchinggame-1.0.0-release-aligned.apk
```

## 7. Upload to Google Play

1. Go to https://play.google.com/apps/publish
2. Create new app
3. Fill in app details (see `GOOGLE_PLAY_DESCRIPTION.md`)
4. Upload screenshots and graphics
5. Upload signed APK
6. Submit for review

See `GOOGLE_PLAY_UPLOAD_GUIDE.md` for detailed instructions.

## Troubleshooting

### Game won't start
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Reinstall Pygame
pip install --upgrade pygame
```

### Build fails
```bash
# Clear build cache
buildozer android clean

# Try again
buildozer android debug
```

### APK won't install
```bash
# Check device compatibility
adb devices

# Uninstall old version
adb uninstall org.ghostcatching.ghostcatchinggame

# Reinstall
adb install -r bin/ghostcatchinggame-debug.apk
```

### Ads not showing
- Verify Ad Unit IDs in `src/ad_manager.py`
- Use test ads first (set `test_mode = True`)
- Wait 24 hours for live ads to activate

## Next Steps

1. **Customize Game**
   - Edit colors in `src/config.py`
   - Adjust difficulty in `LEVEL_CONFIG`
   - Add sound effects

2. **Add Features**
   - Power-ups
   - Achievements
   - Leaderboards
   - See `DEVELOPMENT_GUIDE.md`

3. **Market Your Game**
   - Create social media accounts
   - Share screenshots and videos
   - Ask for reviews
   - Engage with players

4. **Monitor Performance**
   - Check Google Play Console stats
   - Monitor AdMob revenue
   - Fix bugs based on user feedback
   - Regular updates

## Useful Commands

```bash
# View game logs (Android)
adb logcat | grep python

# Clear app data
adb shell pm clear org.ghostcatching.ghostcatchinggame

# Take screenshot
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png

# View app info
adb shell dumpsys package org.ghostcatching.ghostcatchinggame
```

## File Locations

- **Game code**: `/home/ubuntu/ghost_catching_game/main.py`
- **Configuration**: `/home/ubuntu/ghost_catching_game/src/config.py`
- **Assets**: `/home/ubuntu/ghost_catching_game/assets/`
- **Build output**: `/home/ubuntu/ghost_catching_game/bin/`
- **Build cache**: `/home/ubuntu/ghost_catching_game/.buildozer/`

## Important Notes

⚠️ **Backup your keystore!**
- Store `ghost_catching_game.keystore` in a safe location
- You'll need it for all future app updates
- Losing it means you can't update your app on Google Play

📝 **Keep version numbers updated**
- Update `version` in `buildozer.spec`
- Update `__version__` in `main.py`
- Increment for each release

💰 **Monetization Tips**
- Ads appear after each level (good balance)
- Rewarded ads for help (optional)
- Free to play model (best for growth)
- Typical revenue: $0.50-2.00 per 1000 downloads

## Support Resources

- [Pygame Docs](https://www.pygame.org/docs/)
- [Buildozer Docs](https://buildozer.readthedocs.io/)
- [Android Docs](https://developer.android.com/docs)
- [Google Play Help](https://support.google.com/googleplay)

---

**You're all set!** 🎮

Start with `python3 main.py` and have fun!
