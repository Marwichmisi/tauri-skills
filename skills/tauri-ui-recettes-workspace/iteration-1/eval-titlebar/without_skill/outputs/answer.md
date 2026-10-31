# Titlebar custom — Tauri v2

## 1. `tauri.conf.json` : désactiver les décorations natives

```json
{
  "app": {
    "windows": [
      {
        "label": "main",
        "title": "Custom Titlebar",
        "width": 900,
        "height": 600,
        "decorations": false,
        "resizable": true,
        "maximizable": true,
        "minimizable": true,
        "closable": true
      }
    ]
  }
}
```

`decorations: false` supprime la titlebar native. Il faut donc recréer minimize / maximize / close en HTML/JS.

## 2. Capability : autoriser `core:window:*`

Créer `src-tauri/capabilities/main.json` (référencée dans `tauri.conf.json` ou incluse par défaut) :

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Permissions pour la titlebar custom",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:allow-close",
    "core:window:allow-minimize",
    "core:window:allow-toggle-maximize",
    "core:window:allow-start-dragging"
  ]
}
```

Sans ces permissions, les appels `minimize()`, `toggleMaximize()`, `close()` sont bloqués par le système de capabilities de Tauri v2.

## 3. HTML : zone de drag

```html
<div id="titlebar" data-tauri-drag-region>
  <span data-tauri-drag-region>Mon App</span>
  <div class="titlebar-buttons">
    <button id="titlebar-minimize">—</button>
    <button id="titlebar-maximize">□</button>
    <button id="titlebar-close">✕</button>
  </div>
</div>
```

`data-tauri-drag-region` marque la zone déplaçable. Les boutons ne doivent pas hériter du drag, sinon le clic ne marche pas.

## 4. CSS : drag + boutons non-draggables

```css
#titlebar {
  height: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  user-select: none;
  app-region: drag;
}

.titlebar-buttons button {
  app-region: no-drag;
  width: 46px;
  height: 32px;
  border: none;
  background: transparent;
  cursor: pointer;
}

.titlebar-buttons button:hover {
  background: rgba(255, 255, 255, 0.1);
}

#titlebar-close:hover {
  background: #e81123;
  color: white;
}
```

## 5. JS : `getCurrentWindow`

Voir `titlebar.js` :

```js
import { getCurrentWindow } from "@tauri-apps/api/window";

const appWindow = getCurrentWindow();

document.getElementById("titlebar-minimize")?.addEventListener("click", () => {
  appWindow.minimize();
});

document.getElementById("titlebar-maximize")?.addEventListener("click", () => {
  appWindow.toggleMaximize();
});

document.getElementById("titlebar-close")?.addEventListener("click", () => {
  appWindow.close();
});
```

Prérequis : `@tauri-apps/api` installé (`npm i @tauri-apps/api`) et `@tauri-apps/plugin-window` si gestion d'événements avancée.

## Notes

- Sur Windows, `transparent: true` + `decorations: false` demande un CSS de fond géré manuellement.
- Tester `toggleMaximize()` après `minimize()` sur chaque OS : le comportement diffère légèrement entre Windows, macOS et Linux.
