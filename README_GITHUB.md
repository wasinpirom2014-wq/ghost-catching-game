# 👻 Ghost Catching Game

A challenging puzzle game where you trap ghosts using mystical talismans!

## 🎮 Game Features

- **99 Challenging Levels** - From easy to extremely difficult
- **Smart Ghost AI** - Ghosts try to escape using intelligent pathfinding
- **Turn-based Gameplay** - Strategic puzzle mechanics
- **Beautiful Graphics** - Mystical theme with ghosts and talismans
- **Ad-supported** - Monetized with Google AdMob

## 📱 Download

**Coming soon to Google Play Store!**

## 🎯 How to Play

1. **Place Talismans** - Tap on empty cells to place mystical talismans
2. **Block the Ghost** - Prevent the ghost from escaping off the screen
3. **Guide to Pot** - Force the ghost into the sacred pot
4. **Win!** - Capture the ghost to complete the level

### Game Rules
- You place 1 talisman → Ghost moves 1 cell (alternating turns)
- Ghost escapes off screen → You lose
- Ghost enters the pot → You win!

## 🏆 Level Progression

- **Levels 1-20**: Easy (5-8 pots, 20-60 talismans available)
- **Levels 21-60**: Medium (2-5 pots, 45-85 talismans available)
- **Levels 61-99**: Hard (1 pot, 60-100 talismans available)

## 🛠️ Built With

- **Python 3.10+**
- **Pygame** - Game engine
- **Buildozer** - Android APK builder
- **Google AdMob** - Monetization

## 📦 Build Instructions

### Prerequisites
- Ubuntu 20.04+ or Debian-based Linux
- Python 3.10+
- 8GB RAM
- 10GB free disk space

### Build APK

```bash
# Install Buildozer
pip install buildozer cython

# Build debug APK
buildozer android debug

# Build release APK
buildozer android release
```

### Using GitHub Actions (Recommended)

This repository includes GitHub Actions workflow that automatically builds APK on every push!

1. Push code to GitHub
2. Go to **Actions** tab
3. Wait for build to complete (~30-60 minutes)
4. Download APK from **Artifacts**

## 📄 License

This project is proprietary software. All rights reserved.

## 👨‍💻 Developer

Created with ❤️ by [Your Name]

## 📞 Contact

- Email: your.email@example.com
- Website: https://yourwebsite.com

## 🎨 Screenshots

![Screenshot 1](assets/screenshots/screenshot_1_gameplay_easy.png)
![Screenshot 2](assets/screenshots/screenshot_2_gameplay_hard.png)
![Screenshot 3](assets/screenshots/screenshot_3_victory.png)
![Screenshot 4](assets/screenshots/screenshot_4_menu.png)

## 💰 Monetization

This game is free to play and monetized through Google AdMob:
- **Interstitial Ads** - Shown after level completion
- **Rewarded Video Ads** - Watch to retry failed levels

## 🚀 Roadmap

- [ ] Release on Google Play Store
- [ ] Add sound effects and music
- [ ] Add power-ups and special talismans
- [ ] Add leaderboards
- [ ] Add achievements
- [ ] Create more levels (100-200)

## 🐛 Bug Reports

Found a bug? Please open an issue on GitHub!

## ⭐ Support

If you like this game, please give it a star on GitHub!

---

**Made with Manus AI** 🤖
