# App, Path, Window — APIs JS courantes

Sources régénérées avant écriture (commit figé tauri-docs `ec113a50`) :
- `tauri@37b3be6 packages/api/src/app.ts` (`getVersion`, `getName`, `show`/`hide`)
- `tauri@37b3be6 packages/api/src/path.ts` (`BaseDirectory`, `join`, `resolve`, `*Dir`)
- `tauri@37b3be6 packages/api/src/window.ts` (`getCurrentWindow`, `getAllWindows`, `Window`)
- `tauri@37b3be6 packages/api/src/webview.ts`, `webviewWindow.ts`, `dpi.ts`, `image.ts`, `menu.ts`, `tray.ts`
- Rust linkée : `https://docs.rs/tauri/2/tauri/window/struct.Window.html`, jamais copiée.
- Régénéré le 2026-10-31 via sparse checkout `37b3be6`.

## App

```typescript
import { getVersion, getName, getTauriVersion, getIdentifier } from '@tauri-apps/api/app';
import { show, hide } from '@tauri-apps/api/app';
```

> Only the read-only commands are enabled by `core:app:default`
> (`allow-version`, `allow-name`, `allow-tauri-version`, `allow-identifier`, ...).
> Every other function documents the permission it needs.

`show`/`hide` exigent `core:app:allow-app-show`/`allow-app-hide` (hors default).
Doctrine permissions : `tauri-security-capabilities`.

## Path

```typescript
import { appConfigDir, join, resolve, basename } from '@tauri-apps/api/path';
const cfg = await appConfigDir();
const file = await join(cfg, 'photo.png');
```

`BaseDirectory` (AppConfig, AppData, AppLocalData, AppCache, AppLog, Audio, Cache,
Config, Data, Desktop, Document, Download, Exe, Font, Home, Picture, Public, Runtime,
Template, Video, Resource...). `resolveResource` pour `$RESOURCE`.
Variables `$APPDATA`, `$APPLOCALDATA`, `$APPCACHE`... injectées au runtime
(voir `references/plugin-apis.md` scope `fs`).

## Window / Webview

```typescript
import { getCurrentWindow, getAllWindows } from '@tauri-apps/api/window';
const win = getCurrentWindow();
await win.minimize();
await win.toggleMaximize();
await win.close();
```

`getAllWindows(): Promise<Window[]>`. Classe `Window` (3214 lignes source) :
`minimize/maximize/close/setTitle/onResized/onMoved/...`, helpers `TauriEvent`.
`WebviewWindow`, `Webview` : même pattern. `dpi.ts` (`LogicalSize`, `PhysicalSize`),
`image.ts` (`Image`, `transformImage`), `menu.ts`/`tray.ts` : `Resource`
(`await using`, voir `references/core-api.md` + skill `tauri-ui-recettes`).

`withGlobalTauri` : `window.__TAURI__.app|event|window|path` si
`app.withGlobalTauri: true` (voir skill `tauri-start`). Bundler recommandé :
`import { ... } from '@tauri-apps/api/<module>'`.

Frontière : fenêtres/menus/tray/splashscreen idiomatiques → `tauri-ui-recettes` ;
commands/events Rust ↔ frontend → `tauri-ipc-bridge` ; config schéma → `tauri-config-cli-reference`.
