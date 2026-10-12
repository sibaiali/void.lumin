# VOID LUMIN // Android APK & Play Store Packaging Guide
> How to export Void Lumin as a standalone Android `.apk` or publish directly to Google Play Store.

---

## 🚀 Option 1: Instant PWA Install (Zero Build Tools Required)
Void Lumin is already equipped with a Progressive Web App (PWA) manifest (`manifest.json`) and service worker (`sw.js`).

1. Open **`https://your-vercel-domain.app`** (or `http://localhost:8080`) on your Android phone (Chrome / Edge).
2. Tap the bottom button **`📱 Install App / APK`** (or tap browser menu `⋮` &rarr; **Install App** / **Add to Home screen**).
3. The app is installed directly to your Android app drawer with full offline caching, custom icon, and fullscreen hardware acceleration.

---

## 📦 Option 2: Generate Standalone `.apk` with Capacitor
Void Lumin includes `capacitor.config.json` pre-configured for Android.

### Prerequisites:
- Node.js installed
- Android Studio with Android SDK

### Steps to Build APK:
```bash
# 1. Install Capacitor CLI in the project folder
npm install @capacitor/core @capacitor/cli @capacitor/android

# 2. Add Android native platform
npx cap add android

# 3. Synchronize web assets
npx cap sync android

# 4. Open in Android Studio & Build APK
npx cap open android
```
In Android Studio:
- Go to **Build &rarr; Build Bundle(s) / APK(s) &rarr; Build APK(s)**.
- Your standalone release `.apk` is generated under `android/app/build/outputs/apk/release/`.

---

## 🏪 Option 3: Publish to Google Play Store using Bubblewrap (TWA)
Google provides **Bubblewrap**, an official CLI to package any PWA into a production-signed `.aab` (Android App Bundle) for Google Play:

```bash
# 1. Install Google Bubblewrap CLI
npm install -g @bubblewrap/cli

# 2. Initialize from your live URL
bubblewrap init --manifest="https://your-vercel-domain.app/manifest.json"

# 3. Build Google Play Store Bundle
bubblewrap build
```
Upload the resulting `app-release-bundle.aab` directly to Google Play Console.
