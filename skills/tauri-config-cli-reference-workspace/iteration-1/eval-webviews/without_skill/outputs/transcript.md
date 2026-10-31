# Transcript — eval webviews (without_skill)

- Baseline sans skill : aucune lecture de `skills/tauri-config-cli-reference`.
- Réponse rédigée de mémoire (connaissances générales Tauri / webviews) :
  - Windows 11 = WebView2 Evergreen Chromium.
  - Android 14 = System WebView Chromium via Play Store.
  - macOS Sonoma = WKWebView / Safari 17 lié à l'OS.
  - Vérifs : commande macOS (`sw_vers` + `defaults read Safari Info.plist`), inspector Android (`chrome://inspect#devices` + `adb dumpsys`), équivalence caniuse (Chrome/Edge vs Safari).
- Outputs sauvegardés dans `outputs/` : `answer.md`, `transcript.md`.
- Limite : versions exactes approximatives, à confirmer via docs officielles.
