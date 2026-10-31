# Titlebar custom Tauri v2 — réponse

Source : `tauri-docs/src/content/docs/learn/window-customization.mdx`, commit `ec113a50`, titre `Window Customization` (EN canonique).
Routage skill : `references/windows.md` → `examples/titlebar.js` + `examples/tauri.conf.windows.json`.

## 1. Config fenêtre

`decorations: false` sous la fenêtre (doc § `tauri.conf.json` : « Set `decorations` to `false` in your `tauri.conf.json` ») :

```json
{
  "app": {
    "windows": [
      {
        "label": "main",
        "decorations": false
      }
    ]
  }
}
```

Fichier : `outputs/tauri.conf.json`. Le `label: main` est ajouté pour labels uniques exigés par le check ; la doc omet le label dans l'extrait (`"tauri": { "windows": [{ "decorations": false }] }`).

## 2. Capability (sans inventer)

Permissions doc seules, doctrine `tauri-security-capabilities` (`src-tauri/capabilities/default.json`) :

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": [
    "core:window:default",
    "core:window:allow-close",
    "core:window:allow-minimize",
    "core:window:allow-toggle-maximize",
    "core:window:allow-start-dragging"
  ]
}
```

`default` inclut `core:window:allow-internal-toggle-maximize` (tableau permissions du doc).

## 3. HTML drag-region + CSS touch/pen

```html
<div data-tauri-drag-region></div>
```

Doc : « `data-tauri-drag-region` will only work on the element to which it is directly applied. If you want the drag behavior to apply to child elements as well, you'll need to add it to each child individually. » — sinon boutons/inputs cassés.

Touch/pen Windows (doc `:::tip`) :

```css
*[data-tauri-drag-region] {
  app-region: drag;
}
```

## 4. JS boutons

Fichier : `outputs/titlebar.js` (copie fidèle `examples/titlebar.js` = snippet doc § JavaScript) :

```javascript
import { getCurrentWindow } from '@tauri-apps/api/window';
const appWindow = getCurrentWindow();
document.getElementById('titlebar-minimize')?.addEventListener('click', () => appWindow.minimize());
document.getElementById('titlebar-maximize')?.addEventListener('click', () => appWindow.toggleMaximize());
document.getElementById('titlebar-close')?.addEventListener('click', () => appWindow.close());
```

Variante manuelle doc (drag custom) : `mousedown` + `e.buttons === 1` → `detail === 2 ? toggleMaximize() : startDragging()`.

## 5. Validation

```sh
python3 skills/tauri-ui-recettes/scripts/check-ui-recettes.py --config skills/tauri-ui-recettes-workspace/iteration-1/eval-titlebar/with_skill/outputs/tauri.conf.json --frontend skills/tauri-ui-recettes-workspace/iteration-1/eval-titlebar/with_skill/outputs/titlebar.js
```

Résultat :

```
OK skills/tauri-ui-recettes-workspace/iteration-1/eval-titlebar/with_skill/outputs/tauri.conf.json
 - windows: ['main']
OK skills/tauri-ui-recettes-workspace/iteration-1/eval-titlebar/with_skill/outputs/titlebar.js
 - frontend APIs: getCurrentWindow
```
