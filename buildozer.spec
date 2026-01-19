[app]

# (str) Title of your application
title = Ghost Catching Game

# (str) Package name
package.name = ghostcatchinggame

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ghostcatching

# (source.dir) Source directory (where the main.py is)
source.dir = .

# (list) Source includes patterns, e.g. ['images/*', 'data/*']
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,levels/*,src/*

# (list) Source excludes patterns, e.g. ['tests/*', 'docs/*']
source.exclude_exts = spec

# (list) List of directory to exclude from build
source.exclude_dirs = tests,bin,build,dist

# (list) List of exclusions using pattern matching
source.exclude_patterns = license,images/*/*.py

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pygame,requests

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash of the application
presplash.filename = %(source.dir)s/assets/presplash.png

# (string) Icon of the application
icon.filename = %(source.dir)s/assets/icon.png

# (str) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (str) AdMob App ID
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-1477667343771195~1325700040

# (list) Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Android API level to target
android.api = 31

# (int) Minimum API Contstraint
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use legacy toolchain
android.use_legacy_toolchain = False

# (str) Gradle dependencies (Google Play Services for AdMob)
android.gradle_dependencies = com.google.android.gms:play-services-ads:20.6.0

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup scheme, see the documentation
android.backup_scheme = 

# (list) Pattern to whitelist for the whole project
android.whitelist = lib-dynload/termios.so

# (str) Path to a custom whitelist file
android.whitelist_src = 

# (str) Path to a custom blacklist file
android.blacklist_src = 

# (list) List of Java .jar files to add to the libs so that pydroid can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
android.add_src = 

# (int) overrides automatic versionCode (used in build.gradle)
android.version_code = 1

# (str) overrides automatic versionName (used in build.gradle)
android.version_name = 1.0.0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning upon buildozer run if buildozer.spec is newer than Buildozer version
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = .buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin
