# Scope FS : lire $APPLOCALDATA, bloquer webview-data

## But
L'app lit ses fichiers sous `$APPLOCALDATA`, mais ne doit jamais lire
les donnees webview (cookies, storage, caches WebView2/WebKit).

## Solution : set reutilisable (TOML)
Voir `scope.toml` : un `[[set]]` nomme `applocaldata-no-webview-read`.

Principe :
- `allow = [{ path = "$APPLOCALDATA/**" }]` : autorise tout l'arbre en recursif.
- `deny = [...]` : bloque explicitement :
  - `$APPLOCALDATA/webview-data/**` (nommage Linux courant)
  - `$APPLOCALDATA/**/webview-data/**` (variante imbriquee / par fenetre)
  - `$APPLOCALDATA/EBWebView/**` (Windows WebView2)
  - `$APPLOCALDATA/WebView2/**` (Windows WebView2, variante)
- Le meme couple allow/deny est repete sur chaque permission de lecture :
  `allow-read-recursive`, `allow-read-file`, `allow-read-text-file`,
  `allow-read-binary-file`, `allow-read-dir`.
  Sans ca, limiter une seule commande laisse les autres commandes
  contourner le scope.

Usage dans une capability :
```json
{
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": [
    "fs-applocaldata-no-webview:applocaldata-no-webview-read"
  ]
}
```
Adapter le prefixe au nom du fichier sous `src-tauri/permissions/`.

## Pourquoi deny gagne sur allow
En Tauri v2 (plugin fs), l'evaluation est :
1. le chemin doit matcher une entree `allow`,
2. s'il matche aussi une entree `deny`, il est refuse.

Donc un `allow` large `$APPLOCALDATA/**` ne re-ouvre jamais
un sous-chemin liste en `deny`. C'est ce qui rend le motif
allow-large + deny-cible sur pour exclure `webview-data`
sans avoir a enumerer chaque sous-dossier autorise.

## Limites / a verifier
- Ne donner aucune permission d'ecriture si seule la lecture est requise.
- Tester qu'une lecture de `$APPLOCALDATA/webview-data/Cookies` echoue
  alors qu'une lecture de `$APPLOCALDATA/data/app.json` reussit.
- Sur Windows/Linux, verifier le vrai nom du dossier webview
  (`webview-data` vs `EBWebView` vs `WebView2`) et ajuster la liste `deny`.
