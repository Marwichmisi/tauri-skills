# Versions webview — extrait doc

Source : `tauri-docs/src/content/docs/reference/webview-versions.md`, commit `ec113a50`, titre frontmatter `Webview Versions`.

## WebView2, Windows (même fichier)

> Tauri uses WebView2 which is based on Microsoft Edge and therefore Chromium. WebView2 can update itself.

- Supporté Windows 7+, préinstallé sur Windows 11. Sur antérieur à Windows 11, l'installeur Tauri garantit WebView2 sur le système.
- Version récente Chromium garantie (auto-update).

## Android WebView (même fichier)

> Tauri uses the system Android WebView, which is based on Chromium. Tauri does not bundle a WebView with your app.

- Version = provider WebView de l'appareil (composant système à jour sur la plupart des prod, provider interchangeable en réglages dev sur certaines images).
- Dev : ouvrir l'Android Web Inspector (voir `develop/`) et inspecter via Chrome DevTools ; ou réglages dev Android (provider + version).

## WebKit, macOS / iOS / Linux (même fichier)

> Tauri uses WebKit on macOS (through WKWebView) and Linux (through webkit2gtk).

- macOS ≥ 10.10 (Yosemite) : webview préinstallée, core component, updates via OS. macOS non supportées **ne reçoivent pas** les updates WebKit.
- Numéros WebKit : 5 segments + préfixe système (`$(SYSTEM_VERSION_PREFIX)$(MAJOR).$(MINOR).$(TINY).$(MICRO).$(NANO)`, trailing `.0.0` omis) ; préfixe = version OS (ex `17` = macOS 12.x Monterey, `19` = 14.0, `8` = `sdk=iphone*`). Exemple doc : Safari 15.5 sur Monterey 12.x = `17613.2.7.1.8`.
- macOS : `awk '/CFBundleVersion/{getline;gsub(/<[^>]*>/,"");print}' /System/Library/Frameworks/WebKit.framework/Resources/Info.plist`. Table OS → WebKit → Safari du fichier (ex Sonoma 14.0 Beta → `616.1.14.11.11` → 17.0, Ventura 13.4.1 → `615.2.9.11.7` → 16.5.1) : consulter le fichier pour la valeur exacte, vérifier le support via `caniuse`.
- Linux : nature diverse, liste très incomplète (ex Debian 11/Ubuntu 20.04-22.04 → `webkitgtk` 2.36 → WebKit `614.1.6` → TP 140/16.0). Toujours vérifier les dépôts de la distro.

Pas de check déterministe : versions documentées, pas de règle à valider (renvoi doc). Pour `webkit2gtk` Linux en dev/debug, voir skill `tauri-dev-quality`.
