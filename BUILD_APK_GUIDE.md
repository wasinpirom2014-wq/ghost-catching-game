# คู่มือการ Build APK - Ghost Catching Game

## 🎯 ภาพรวม

คู่มือนี้จะแนะนำวิธีการ **build APK** จากเกม Ghost Catching Game ที่คุณสร้างขึ้น เพื่อนำไปติดตั้งบนมือถือ Android และอัปโหลดไป Google Play Store

---

## ✅ สิ่งที่เตรียมพร้อมแล้ว

- ✓ เกมสมบูรณ์พร้อม 99 ด่าน
- ✓ Ad Unit IDs จาก Google AdMob
- ✓ Assets ครบถ้วน (Icon, Splash Screen, Screenshots)
- ✓ ไฟล์ buildozer.spec พร้อมใช้งาน
- ✓ เอกสารครบถ้วน

---

## 🖥️ ความต้องการของระบบ

### สำหรับ Linux (แนะนำ)
- **OS**: Ubuntu 20.04+ หรือ Debian-based Linux
- **RAM**: 8 GB ขึ้นไป
- **Storage**: 10 GB ว่าง (สำหรับ Android SDK/NDK)
- **Python**: 3.8+

### สำหรับ Windows/macOS
- ใช้ WSL2 (Windows Subsystem for Linux) หรือ Virtual Machine
- หรือใช้ GitHub Actions / Cloud Build Service

---

## 📦 ขั้นตอนที่ 1: ติดตั้ง Dependencies

### 1.1 อัปเดตระบบ
```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 ติดตั้ง Build Tools
```bash
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-11-jdk \
    python3-pip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev
```

### 1.3 ติดตั้ง Buildozer
```bash
sudo pip3 install --upgrade buildozer
sudo pip3 install --upgrade cython
```

### 1.4 ติดตั้ง Dependencies ของเกม
```bash
cd /home/ubuntu/ghost_catching_game
pip3 install -r requirements.txt
```

---

## 🔨 ขั้นตอนที่ 2: Build APK ครั้งแรก

### 2.1 เข้าไปยังโฟลเดอร์เกม
```bash
cd /home/ubuntu/ghost_catching_game
```

### 2.2 Build Debug APK (สำหรับทดสอบ)
```bash
buildozer android debug
```

**หมายเหตุ**: 
- การ build ครั้งแรกจะใช้เวลา **1-2 ชั่วโมง**
- Buildozer จะดาวน์โหลด Android SDK, NDK, และ dependencies อัตโนมัติ (~2 GB)
- ต้องมีอินเทอร์เน็ตเชื่อมต่อตลอดเวลา

### 2.3 ตรวจสอบ APK ที่สร้างเสร็จ
```bash
ls -lh bin/
```

คุณจะเห็นไฟล์:
```
ghostcatchinggame-1.0.0-debug.apk
```

---

## 📱 ขั้นตอนที่ 3: ทดสอบ APK บนมือถือ

### 3.1 เปิด USB Debugging บนมือถือ
1. ไปที่ **Settings** → **About Phone**
2. กด **Build Number** 7 ครั้ง (เพื่อเปิด Developer Mode)
3. กลับไปที่ **Settings** → **Developer Options**
4. เปิด **USB Debugging**

### 3.2 เชื่อมต่อมือถือกับคอมพิวเตอร์
```bash
# ติดตั้ง ADB
sudo apt install -y android-tools-adb

# ตรวจสอบว่ามือถือเชื่อมต่อแล้ว
adb devices
```

### 3.3 ติดตั้ง APK บนมือถือ
```bash
adb install -r bin/ghostcatchinggame-1.0.0-debug.apk
```

### 3.4 ทดสอบเกม
- เปิดเกมบนมือถือ
- ทดสอบการเล่น
- ตรวจสอบว่าโฆษณาแสดงหรือไม่ (จะเป็น Test Ads)

---

## 🔐 ขั้นตอนที่ 4: สร้าง Keystore สำหรับ Signing

### 4.1 สร้าง Keystore
```bash
keytool -genkey -v \
    -keystore ~/ghost_catching_game.keystore \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000 \
    -alias ghostcatching
```

### 4.2 กรอกข้อมูล
```
Enter keystore password: [ใส่รหัสผ่าน - อย่าลืม!]
Re-enter new password: [ใส่รหัสผ่านอีกครั้ง]
What is your first and last name? [ชื่อ-นามสกุล]
What is the name of your organizational unit? [ชื่อองค์กร/บริษัท]
What is the name of your organization? [ชื่อองค์กร]
What is the name of your City or Locality? [เมือง]
What is the name of your State or Province? [จังหวัด]
What is the two-letter country code for this unit? [TH]
Is CN=..., OU=..., O=..., L=..., ST=..., C=TH correct? [yes]
```

### 4.3 เก็บ Keystore ไว้อย่างปลอดภัย
```bash
# สำรองไฟล์ Keystore
cp ~/ghost_catching_game.keystore ~/Backup/
```

**⚠️ สำคัญมาก**:
- **เก็บไฟล์ Keystore ไว้ให้ดี** - หากสูญหาย จะไม่สามารถอัปเดตแอปได้อีก!
- **จดรหัสผ่านไว้** - ต้องใช้ทุกครั้งที่อัปเดตแอป
- **อย่าแชร์ Keystore ให้ใคร** - เป็นความลับสูงสุด

---

## 🚀 ขั้นตอนที่ 5: Build Release APK

### 5.1 แก้ไข buildozer.spec
เปิดไฟล์ `buildozer.spec` และเพิ่ม:

```ini
[app]
# ... (ส่วนอื่นๆ)

# Keystore สำหรับ signing
android.keystore = ~/ghost_catching_game.keystore
android.keystore_alias = ghostcatching
```

### 5.2 Build Release APK
```bash
buildozer android release
```

Buildozer จะถามรหัสผ่าน Keystore:
```
Enter keystore password: [ใส่รหัสผ่าน]
Enter key password: [ใส่รหัสผ่านอีกครั้ง]
```

### 5.3 ตรวจสอบ APK ที่สร้างเสร็จ
```bash
ls -lh bin/
```

คุณจะเห็นไฟล์:
```
ghostcatchinggame-1.0.0-release.apk
```

---

## 📤 ขั้นตอนที่ 6: อัปโหลดไป Google Play Store

### 6.1 เตรียม Assets
คัดลอกไฟล์เหล่านี้ไปยังคอมพิวเตอร์ของคุณ:
- `bin/ghostcatchinggame-1.0.0-release.apk`
- `assets/icon.png`
- `assets/feature_graphic.png`
- `assets/screenshots/*.png`

### 6.2 เข้า Google Play Console
1. ไปที่ https://play.google.com/console
2. คลิก **"Create app"**
3. กรอกข้อมูลแอป:
   - **App name**: Ghost Catching Game
   - **Default language**: English (United States)
   - **App or game**: Game
   - **Free or paid**: Free

### 6.3 กรอกข้อมูลแอป
ใช้ข้อมูลจากไฟล์ `GOOGLE_PLAY_DESCRIPTION.md`:
- **Short description**: คัดลอกจาก "Short Description"
- **Full description**: คัดลอกจาก "Full Description"
- **App category**: Puzzle
- **Content rating**: PEGI 3 / Everyone

### 6.4 อัปโหลด Assets
- **App icon**: อัปโหลด `assets/icon.png`
- **Feature graphic**: อัปโหลด `assets/feature_graphic.png`
- **Screenshots**: อัปโหลดทั้ง 4 ภาพจาก `assets/screenshots/`

### 6.5 อัปโหลด APK
1. ไปที่ **"Release"** → **"Production"**
2. คลิก **"Create new release"**
3. อัปโหลด `ghostcatchinggame-1.0.0-release.apk`
4. กรอก **Release notes**:
   ```
   Initial release of Ghost Catching Game
   - 99 challenging levels
   - Smart ghost AI
   - Beautiful graphics
   - Ad-supported free game
   ```

### 6.6 Submit for Review
1. ตรวจสอบข้อมูลทั้งหมด
2. คลิก **"Submit for review"**
3. รอ Review (โดยปกติ 1-3 ชั่วโมง)

---

## 🔄 ขั้นตอนที่ 7: อัปเดตแอป (ในอนาคต)

### 7.1 เปลี่ยนเวอร์ชัน
แก้ไขไฟล์ `buildozer.spec`:
```ini
version = 1.0.1
android.version_code = 2
```

### 7.2 Build APK ใหม่
```bash
buildozer android release
```

### 7.3 อัปโหลดเวอร์ชันใหม่
- เข้า Google Play Console
- ไปที่ **"Release"** → **"Production"**
- คลิก **"Create new release"**
- อัปโหลด APK เวอร์ชันใหม่
- Submit

---

## 🐛 แก้ปัญหาที่พบบ่อย

### ปัญหา: Buildozer ติดตั้งไม่สำเร็จ
**วิธีแก้**:
```bash
sudo pip3 install --upgrade pip
sudo pip3 install --upgrade buildozer cython
```

### ปัญหา: Build ล้มเหลวเพราะ Java version
**วิธีแก้**:
```bash
sudo update-alternatives --config java
# เลือก Java 11
```

### ปัญหา: Out of memory
**วิธีแก้**:
```bash
# เพิ่ม swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### ปัญหา: APK ติดตั้งไม่ได้บนมือถือ
**วิธีแก้**:
- ตรวจสอบว่าเปิด "Install from unknown sources" แล้ว
- ลบ APK เวอร์ชันเก่าออกก่อน
- ลองใช้ `adb install -r` แทน

### ปัญหา: โฆษณาไม่แสดง
**วิธีแก้**:
- ตรวจสอบว่าใส่ Ad Unit IDs ถูกต้อง
- รอ 1-2 ชั่วโมงหลังสร้าง Ad Units
- ตรวจสอบ internet connection บนมือถือ
- ดู logs: `adb logcat | grep AdMob`

---

## 📊 ตรวจสอบสถานะ Build

### ดู Build Logs
```bash
# ดู logs แบบเรียลไทม์
tail -f .buildozer/logs/buildozer.log

# ค้นหา errors
grep -i error .buildozer/logs/buildozer.log
```

### ทดสอบ APK
```bash
# ติดตั้งบนมือถือ
adb install -r bin/ghostcatchinggame-1.0.0-debug.apk

# ดู logs จากแอป
adb logcat | grep python

# ดูข้อมูล APK
aapt dump badging bin/ghostcatchinggame-1.0.0-debug.apk
```

---

## 🎓 Tips & Best Practices

### 1. ทดสอบบ่อยๆ
- Build debug APK และทดสอบบนมือถือจริงก่อน release
- ทดสอบบนมือถือหลายรุ่น (ถ้าทำได้)

### 2. Version Control
- ใช้ Git เก็บโค้ด
- Tag version ทุกครั้งที่ release
- เก็บ Keystore แยกจาก Git (ห้าม commit!)

### 3. Optimize APK Size
- ลบไฟล์ที่ไม่จำเป็นออก
- ใช้ ProGuard/R8 สำหรับ obfuscation
- Compress assets

### 4. Monitor Performance
- ใช้ Android Profiler ดู memory/CPU usage
- ตรวจสอบ crash reports ใน Play Console
- ติดตาม user reviews

---

## 📞 ช่องทางขอความช่วยเหลือ

### Buildozer
- **Docs**: https://buildozer.readthedocs.io/
- **GitHub**: https://github.com/kivy/buildozer
- **Community**: https://groups.google.com/g/kivy-users

### Google Play Console
- **Help**: https://support.google.com/googleplay/android-developer
- **Policy**: https://play.google.com/about/developer-content-policy/

### AdMob
- **Help**: https://support.google.com/admob
- **Community**: https://groups.google.com/g/google-admob-ads-sdk

---

## ✅ Checklist ก่อน Release

- [ ] ทดสอบเกมบนมือถือจริง
- [ ] ตรวจสอบว่าโฆษณาแสดงถูกต้อง
- [ ] ทดสอบทุกด่าน (อย่างน้อย 10 ด่านแรก)
- [ ] ตรวจสอบไม่มี crash
- [ ] เตรียม Screenshots สวยงาม
- [ ] เขียน Description ที่น่าสนใจ
- [ ] ตั้งค่า Content Rating
- [ ] เตรียม Privacy Policy (ถ้ามีการเก็บข้อมูล)
- [ ] Sign APK ด้วย Keystore
- [ ] สำรอง Keystore ไว้ปลอดภัย
- [ ] อัปโหลดไป Play Console
- [ ] Submit for review

---

**สำเร็จแล้ว!** 🎉

คุณพร้อมที่จะ build APK และเผยแพร่เกมของคุณแล้ว!

**Good luck!** 🚀🎮
