# Ghost Catching Game - Google Play Store Upload Guide

Complete step-by-step guide to upload your game to Google Play Store.

## Prerequisites

Before you start, make sure you have:

1. **Google Play Developer Account**
   - Visit: https://play.google.com/apps/publish
   - Pay: $25 one-time registration fee
   - Verify your identity and payment method

2. **Google AdMob Account**
   - Visit: https://admob.google.com
   - Link to your Google Play account
   - Create Ad Unit IDs (see AdMob Setup section)

3. **Signed APK/AAB File**
   - Built from buildozer
   - Signed with your keystore

4. **App Assets**
   - Icon (512x512 PNG)
   - Feature graphic (1024x500 PNG)
   - Screenshots (1080x1920 PNG, minimum 2)
   - Description and other text

## Step 1: Create a Keystore for Signing

A keystore is needed to sign your APK for release. You only need to do this once.

```bash
# Generate a keystore (replace with your own values)
keytool -genkey -v -keystore ghost_catching_game.keystore \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -alias ghostcatching

# When prompted, enter:
# - Keystore password: (create a strong password)
# - Key password: (can be same as keystore password)
# - First and Last Name: Your Name
# - Organization: Your Company/Name
# - City: Your City
# - State: Your State
# - Country: Your Country Code (e.g., US, TH)
```

**IMPORTANT**: Save this keystore file in a safe location. You'll need it for future updates!

## Step 2: Build Release APK

```bash
# Navigate to project directory
cd /home/ubuntu/ghost_catching_game

# Build release APK
buildozer android release

# The APK will be in: bin/ghostcatchinggame-1.0.0-release.apk
```

## Step 3: Sign the APK

```bash
# Sign with your keystore
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
    -keystore ghost_catching_game.keystore \
    bin/ghostcatchinggame-1.0.0-release.apk ghostcatching

# Verify the signature
jarsigner -verify -verbose bin/ghostcatchinggame-1.0.0-release.apk
```

## Step 4: Align the APK (Optional but Recommended)

```bash
# Align APK for better performance
zipalign -v 4 bin/ghostcatchinggame-1.0.0-release.apk \
    bin/ghostcatchinggame-1.0.0-release-aligned.apk

# Use the aligned APK for upload
```

## Step 5: Set Up AdMob

### Create Ad Unit IDs

1. Go to https://admob.google.com
2. Click "Apps" → "Add App"
3. Select "Android"
4. Enter app name: "Ghost Catching Game"
5. Accept Google Play policies
6. Click "Create"

### Create Interstitial Ad Unit

1. In AdMob dashboard, click your app
2. Click "Ad units" → "Create ad unit"
3. Select "Interstitial"
4. Name: "Level Complete Interstitial"
5. Copy the Ad Unit ID
6. Update `src/ad_manager.py`:
   ```python
   self.interstitial_ad_unit_id = "ca-app-pub-xxxxxxxxxxxxxxxx/yyyyyyyyyyyyyy"
   ```

### Create Rewarded Ad Unit

1. Click "Ad units" → "Create ad unit"
2. Select "Rewarded"
3. Name: "Retry Rewarded"
4. Copy the Ad Unit ID
5. Update `src/ad_manager.py`:
   ```python
   self.rewarded_ad_unit_id = "ca-app-pub-xxxxxxxxxxxxxxxx/zzzzzzzzzzzzzz"
   ```

### Link AdMob to Play Console

1. In Google Play Console, go to Monetization → AdMob
2. Link your AdMob account
3. Your app will be linked automatically

## Step 6: Prepare App Listing

### Create New App

1. Go to https://play.google.com/apps/publish
2. Click "Create app"
3. App name: "Ghost Catching Game"
4. Default language: English
5. App type: Game
6. Category: Puzzle
7. Click "Create app"

### Fill in App Details

#### 1. App Access
- Access type: Default (free)
- Click "Save"

#### 2. Target Audience
- Target audience: Everyone
- Content rating: Everyone (3+)
- Click "Save"

#### 3. Content Rating
- Complete content rating questionnaire
- Click "Save"

#### 4. App Listing

**Title** (50 characters max):
```
Ghost Catching Game
```

**Short description** (80 characters max):
```
Catch ghosts with talismans in this addictive turn-based puzzle game!
```

**Full description** (4000 characters max):
See `GOOGLE_PLAY_DESCRIPTION.md` for the full description.

**Screenshots** (minimum 2, maximum 8):
- Upload 5-8 screenshots (1080x1920 PNG)
- Show gameplay, levels, UI, and features
- Recommended: 2 gameplay, 2 difficulty levels, 1 victory screen

**Feature graphic** (1024x500 PNG):
- Upload your feature graphic
- This appears at the top of your store listing

**Icon** (512x512 PNG):
- Upload your app icon
- Must be a PNG with transparency

**Promo graphic** (180x120 PNG, optional):
- Promotional image for featured listings

**Video** (optional):
- YouTube video URL (if you have a trailer)

**Contact details**:
- Email: your-email@example.com
- Website: your-website.com (optional)
- Phone: your-phone-number (optional)

**Privacy policy**:
- Create a privacy policy (see template below)
- Paste URL or text

**Content rating**:
- Select "Everyone" or appropriate rating

#### 5. Pricing & Distribution

**Pricing**:
- Select "Free"
- Click "Save"

**Countries/regions**:
- Select all countries where you want to distribute
- Default: All countries
- Click "Save"

**Device categories**:
- Select "Phones and tablets"
- Click "Save"

**Consent**:
- Check all required consents
- Click "Save"

## Step 7: Upload APK

1. Go to "Release" → "Production"
2. Click "Create new release"
3. Upload your signed and aligned APK
4. Review the app bundle information
5. Add release notes:
   ```
   Version 1.0.0 - Initial Release
   
   Features:
   - 99 challenging levels
   - Turn-based puzzle gameplay
   - Progressive difficulty
   - Free to play with ads
   ```
6. Click "Save"

## Step 8: Review & Submit

1. Go to "App content" and verify all information
2. Check "Ads" section and verify AdMob setup
3. Review "Ratings & reviews" settings
4. Check "Policies" for any violations
5. Go to "Release" → "Production"
6. Click "Review release"
7. Verify all information is correct
8. Click "Submit release"

## Step 9: Wait for Review

- Initial review typically takes 1-3 hours
- You'll receive email confirmation
- App will appear on Google Play Store once approved
- You can track status in Play Console

## Step 10: Post-Launch

### Monitor Performance

1. Check "Statistics" for:
   - Downloads and installs
   - Uninstalls
   - Crash rate
   - ANR (Application Not Responding) rate

2. Check "Ratings & reviews" for:
   - User feedback
   - Common issues
   - Feature requests

3. Check "AdMob" for:
   - Ad impressions
   - Revenue
   - eCPM (earnings per 1000 impressions)

### Update Your App

When you have updates:

1. Update version in `main.py`:
   ```python
   __version__ = "1.1.0"
   ```

2. Update `buildozer.spec`:
   ```
   version = 1.1.0
   ```

3. Rebuild and sign APK
4. Upload to Play Console
5. Add release notes
6. Submit for review

## Privacy Policy Template

```markdown
# Privacy Policy for Ghost Catching Game

## Information We Collect

Ghost Catching Game collects the following information:

1. **Device Information**: Device model, OS version, unique device ID
2. **Usage Information**: Levels played, time spent, game progress
3. **Advertising Information**: Ad impressions, clicks, user interactions
4. **Crash Reports**: Error logs for debugging

## How We Use Information

We use collected information to:
- Improve game performance and user experience
- Display targeted advertisements
- Fix bugs and crashes
- Understand user behavior and preferences

## Third-Party Services

Our app uses:
- **Google AdMob**: For displaying advertisements
- **Google Analytics**: For usage analytics
- **Google Play Services**: For app functionality

## Data Retention

- Usage data is retained for 90 days
- Crash reports are retained for 30 days
- Advertising data is retained per Google AdMob policy

## Your Rights

You have the right to:
- Access your personal data
- Request deletion of your data
- Opt-out of personalized ads (Android Settings → Google → Manage your Google Account → Data & Privacy)

## Contact Us

For privacy concerns, contact: privacy@ghostcatchinggame.com

## Changes to This Policy

We may update this policy from time to time. Changes will be posted in the app.

Last updated: [Current Date]
```

## Troubleshooting

### App Rejected for Policy Violation

**Common reasons**:
- Misleading app description
- Inappropriate content
- Broken functionality
- Crash on startup

**Solution**:
- Review rejection email carefully
- Fix the issue
- Resubmit with explanation

### Low Downloads

**Possible reasons**:
- Poor app listing quality
- Lack of marketing
- Bad ratings/reviews
- Competitive market

**Solution**:
- Improve screenshots and description
- Fix bugs and improve ratings
- Market on social media
- Regular updates

### Low Ad Revenue

**Possible reasons**:
- Low traffic
- Low-value user demographics
- Ad placement issues
- Ad blockers

**Solution**:
- Improve game quality to increase downloads
- Optimize ad placement
- A/B test different ad formats
- Target high-value regions

## Useful Resources

- [Google Play Console Help](https://support.google.com/googleplay/android-developer)
- [AdMob Help Center](https://support.google.com/admob)
- [Android App Signing Guide](https://developer.android.com/studio/publish/app-signing)
- [Google Play Policies](https://play.google.com/about/developer-content-policy/)

---

**Congratulations on launching your game!** 🎉

Good luck with Ghost Catching Game on Google Play Store!
