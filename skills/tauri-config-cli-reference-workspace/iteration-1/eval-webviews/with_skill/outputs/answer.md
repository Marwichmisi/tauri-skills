# Webviews cibles — Windows 11 / Android 14 / macOS Sonoma

## 1. Windows 11

- **Cible : WebView2** — basée sur Microsoft Edge donc Chromium.
- Préinstallée sur Windows 11. Sur Windows < 11, l'installeur Tauri garantit WebView2 sur le système.
- WebView2 s'auto-met à jour → version Chromium récente garantie.

> Tauri uses WebView2 which is based on Microsoft Edge and therefore Chromium. WebView2 can update itself.

## 2. Android 14

- **Cible : system Android WebView** — basée sur Chromium. Tauri ne bundle pas de WebView avec l'app.
- Version = provider WebView de l'appareil (composant système à jour sur la plupart des prod, provider interchangeable en réglages dev sur certaines images).

> Tauri uses the system Android WebView, which is based on Chromium. Tauri does not bundle a WebView with your app.

- **Vérification :**
  - Dev : ouvrir l'Android Web Inspector (voir `develop/`) et inspecter via Chrome DevTools ;
  - ou réglages dev Android (provider + version).

## 3. macOS Sonoma

- **Cible : WebKit via WKWebView.**
- macOS ≥ 10.10 (Yosemite) : webview préinstallée, core component, updates via OS. macOS non supportées **ne reçoivent pas** les updates WebKit.

> Tauri uses WebKit on macOS (through WKWebView) and Linux (through webkit2gtk).

- **Numéros WebKit :** 5 segments + préfixe système (`$(SYSTEM_VERSION_PREFIX)$(MAJOR).$(MINOR).$(TINY).$(MICRO).$(NANO)`, trailing `.0.0` omis) ; préfixe = version OS (ex `17` = macOS 12.x Monterey, `19` = 14.0, `8` = `sdk=iphone*`). Exemple doc : Safari 15.5 sur Monterey 12.x = `17613.2.7.1.8`.
- **Commande macOS (version exacte) :**

```sh
awk '/CFBundleVersion/{getline;gsub(/<[^>]*>/,"");print}' /System/Library/Frameworks/WebKit.framework/Resources/Info.plist
```

- **Table OS → WebKit → Safari (extrait doc) :** Sonoma 14.0 Beta → `616.1.14.11.11` → 17.0 ; Ventura 13.4.1 → `615.2.9.11.7` → 16.5.1. Consulter le fichier pour la valeur exacte.
- **Équivalence caniuse :** vérifier le support via `caniuse` à partir de la version Safari mappée.

## 4. Cas Linux webkit2gtk en debug

Hors périmètre ici — nature diverse, liste très incomplète (ex Debian 11 / Ubuntu 20.04-22.04 → `webkitgtk` 2.36 → WebKit `614.1.6` → TP 140/16.0 ; toujours vérifier les dépôts de la distro).
Pour `webkit2gtk` Linux en dev/debug → voir skill `tauri-dev-quality`.

## Sources

- Source : `tauri-docs/src/content/docs/reference/webview-versions.md`, commit `ec113a50`, titre frontmatter `Webview Versions`.
- Relayé via skill `tauri-config-cli-reference` → `references/webviews.md` (copie fidèle, même Source en tête). Routage : intention `Vérifier une version webview` → `references/webviews.md` → renvoi doc, pas de script.
- EN canonique seule. Traductions ignorées.

## Frontières

- `tauri-security-capabilities` : seule autorité capabilities/permissions/scopes — aucune permission déclarée ici.
- `tauri-plugins-catalogue` : fiches `plugin/*` — hors sujet webview.
- `tauri-ipc-bridge` : formats/fusion config, icons, sidecars — hors sujet.
- `tauri-distribution` : signing/bundler/updater — hors sujet.
- `tauri-start`, `tauri-migrate`, `tauri-dev-quality`, `tauri-plugin-dev` : `init/dev/build/icon`, `migrate`, debug/WebDriver, `plugin new`. Ici : pour `webkit2gtk` Linux en dev/debug, renvoyer vers `tauri-dev-quality`.
- Hors pack : `about/`, `contribute`, traductions. Générés absents au commit : régénérer, jamais inventer.
- Pas de check déterministe : versions documentées, pas de règle à valider (`scripts/check-config-cli.py` sans mode webview — renvoi doc).
