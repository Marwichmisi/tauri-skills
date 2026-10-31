# Webviews cibles Tauri — Windows 11 / Android 14 / macOS Sonoma

## 1. Windows 11 → WebView2 (Edge Chromium)

- **Moteur :** Microsoft Edge WebView2, base Chromium Evergreen.
- **Particularité :** pré-installé sur Windows 11, mise à jour automatique indépendante de l'OS (canal Evergreen). Tauri ne fige pas la version, il utilise le runtime présent sur la machine.
- **Équivalence caniuse :** prendre la version Chromium sous-jacente (ex. WebView2 120.x = Chrome/Edge 120) et vérifier sur caniuse.com avec le filtre **Chrome / Edge**.
- **Vérification rapide (dans l'app) :**
  ```js
  console.log(navigator.userAgent);
  // ex: Edg/... Chrome/120.0.0.0
  ```

## 2. Android 14 → Android System WebView (Chromium)

- **Moteur :** Android System WebView, base Chromium, mis à jour via Play Store indépendamment d'Android 14.
- **Particularité :** sur appareil réel la version dépend de la MAJ Play Store, pas d'Android 14 lui-même. Sur émulateur, souvent version plus ancienne.
- **Équivalence caniuse :** version Chromium affichée dans l'user-agent → filtre **Chrome Android** sur caniuse.com.
- **Vérification via inspector Android :**
  1. Activer options développeur + débogage USB.
  2. Ouvrir `chrome://inspect#devices` dans Chrome desktop.
  3. Inspecter la WebView Tauri, taper dans la console :
  ```js
  navigator.userAgent; navigator.appVersion;
  ```
  Alternative ADB :
  ```
  adb shell dumpsys package com.google.android.webview | grep version
  adb shell dumpsys package com.android.webview | grep version
  ```

## 3. macOS Sonoma → WKWebView (WebKit / Safari)

- **Moteur :** WKWebView (WebKit), version liée à Safari et à macOS. Sonoma (14.0) livre Safari 17.x ; les MAJ mineures (14.1 → Safari 17.1, 14.4 → Safari 17.4, etc.) font évoluer WebKit.
- **Particularité :** pas de mise à jour indépendante comme WebView2 : figer le support Sonoma = supporter Safari 17.
- **Équivalence caniuse :** filtre **Safari / Safari iOS 17.x** sur caniuse.com. Attention aux gaps connus WebKit (ex. certaines APIs PWA, WebRTC, codecs).
- **Vérification version exacte (commande macOS) :**
  ```bash
  sw_vers
  defaults read /Applications/Safari.app/Contents/Info.plist CFBundleShortVersionString
  # ou :
  system_profiler SPSoftwareDataType
  ```
  + dans la WebView :
  ```js
  navigator.userAgent
  // ex: Version/17.4 Safari/605.1.15
  ```

## Résumé

| OS | Webview Tauri | Versionnée par | Check caniuse avec |
|----|---------------|----------------|---------------------|
| Windows 11 | WebView2 (Edge Chromium) | Runtime Evergreen auto-MAJ | Chrome / Edge |
| Android 14 | System WebView (Chromium) | Play Store, pas l'OS | Chrome Android |
| macOS Sonoma | WKWebView (WebKit) | Safari 17.x lié à Sonoma | Safari 17 |

**Règle pratique :** toujours lire `navigator.userAgent` dans la webview cible pour obtenir la version exacte, puis reporter cette version sur caniuse.com.
