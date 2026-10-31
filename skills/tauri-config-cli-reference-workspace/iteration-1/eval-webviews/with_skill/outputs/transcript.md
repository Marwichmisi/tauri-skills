# Transcript — skill tauri-config-cli-reference (eval webviews)

## 1. Chargement skill

- Lu `SKILL.md` (commit `ec113a50`, EN canonique seule, Workflow / Routage / Frontières / Règle anti-drift).
- Intention demandée : `Quelle webview cible mon app sur Windows 11, Android 14 et macOS Sonoma, et comment vérifier la version exacte ?` → classée `Vérifier une version webview`.

## 2. Routage (table SKILL.md)

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Vérifier une version webview (WebView2 Windows, Android WebView, WebKit macOS/iOS/Linux) | `references/webviews.md` | — (renvoi doc, tables dans le fichier) | — (renvoi doc) |

→ Lu `references/webviews.md` en premier (Source : `tauri-docs/src/content/docs/reference/webview-versions.md`, commit `ec113a50`, titre `Webview Versions`).
→ Lu aussi `references/config.md`, `references/cli.md`, `references/environment.md` pour écarter config / CLI / env (hors intention).
→ Pas d'`examples/` applicable (renvoi doc). Pas de `scripts/check-config-cli.py --config/--cli/--env` (aucun artefact config/CLI/env, pas de mode webview — renvoi doc explicite ligne 28 de `references/webviews.md`).

## 3. Extraction fidèle (sans invention)

- Windows : WebView2 = Edge/Chromium, auto-update, préinstallé Win 11, installeur garantit sur < Win 11.
- Android : system WebView = Chromium, non bundlée, version = provider appareil ; vérif = Android Web Inspector via Chrome DevTools ou réglages dev.
- macOS/iOS/Linux : WebKit via WKWebView / webkit2gtk ; macOS ≥ 10.10 préinstallée + updates OS ; numéros 5 segments + préfixe ; commande `awk … /System/Library/Frameworks/WebKit.framework/Resources/Info.plist` ; table Sonoma 14.0 Beta → `616.1.14.11.11` → 17.0 ; support via `caniuse`.
- Linux : renvoi distro + `tauri-dev-quality` pour debug webkit2gtk.

## 4. Frontières appliquées

- Aucune capability/permission déclarée → renvoi `tauri-security-capabilities` si doute.
- Aucune fiche plugin → `tauri-plugins-catalogue` hors sujet.
- Cas `webkit2gtk` Linux en debug → renvoi explicite vers `tauri-dev-quality` (demandé + prévu par `references/webviews.md` ligne 28 et `SKILL.md` Frontières).

## 5. Écriture outputs

- `outputs/answer.md` : réponse + Sources (fichier + commit + titre) + Frontières.
- `outputs/transcript.md` : présent fichier (étapes skill).
- Aucun script webview créé (consigne + skill : renvoi doc).
