# Mobile — multi-fenêtres + associations de fichiers

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/learn/mobile-multiwindow.mdx` (titre `Multi-Window on Mobile`)
- `tauri-docs/src/content/docs/learn/mobile-file-associations.mdx` (titre `File Associations on Mobile`)
- `tauri-docs/src/content/docs/learn/index.mdx` (titre `Learn`, routeur seul : pointe vers splashscreen / sidecar-nodejs / mobile-multiwindow / mobile-file-associations, sans doctrine propre)

> Tauri supports multiple windows on Android and iOS, allowing your app to display content side-by-side on tablets or in separate scenes on iPad.
> Tauri supports file associations on Android and iOS, allowing your app to be registered as a handler for specific file types.

## Capability commune (mobile-multiwindow.mdx)

```json title="src-tauri/capabilities/default.json"
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": ["core:default", "core:webview:allow-create-webview-window"]
}
```
- Fenêtres dynamiques (`main-1`, `main-2`, ...) : wildcard `"windows": ["main", "main-*"]` (note SceneRequested). Doctrine permissions en `tauri-security-capabilities`.

## Android multi-window (mobile-multiwindow.mdx)

- `androidx.window:window:1.5.0` + `androidx.startup:startup-runtime:1.2.0` (`build.gradle.kts`).
- `DetailActivity : TauriActivity()`, manifest `PROPERTY_ACTIVITY_EMBEDDING_SPLITS_ENABLED=true` + `tools:node="merge"` + `InitializationProvider` + `SplitInitializer`, règles `res/xml/main_split_config.xml` (`SplitPairRule` `splitRatio 0.33`, `splitMinWidthDp 840`, `primaryActivityName .MainActivity` / `secondaryActivityName .DetailActivity`).
- Condition : Android 12L (API 32)+, `app.supportsMultipleWindows` à runtime. Router frontend `createBrowserRouter` (pas hash) pour URLs distinctes par fenêtre.

## iOS multi-window (mobile-multiwindow.mdx)

- `src-tauri/Info.ios.plist` : `UIApplicationSceneManifest` + `UIApplicationSupportsMultipleScenes true` + `UISceneConfigurations`.
- `RunEvent::SceneRequested` → `WebviewWindowBuilder::new(app, format!("main-{counter}"), WebviewUrl::default()).build()` (compteur `cfg(target_os = "ios")`). Condition iOS 13+.

## Créer des fenêtres (mobile-multiwindow.mdx)

- JS : `new WebviewWindow(\`detail-${id}\`, { url: \`detail/${id}\`, activityName: 'DetailActivity' })` + `once('tauri://created'/'tauri://error')`. Getters : `activityName()`, `sceneIdentifier()`.
- Rust : `WebviewWindowBuilder::new(main_window, "detail", WebviewUrl::App("detail/1".into()))` + `#[cfg(target_os = "android")] .activity_name("DetailActivity")`. Options : `activityName` / `createdByActivityName` (Android), `requestedBySceneIdentifier` (iOS, hérité du manager sinon foreground).

## File associations (mobile-file-associations.mdx)

```json title="src-tauri/tauri.conf.json"
{ "bundle": { "fileAssociations": [{ "ext": ["png"], "mimeType": "image/png" }, { "ext": ["jpg", "jpeg"], "mimeType": "image/jpeg" }] } }
```
- Options doc seules : `ext` (sans point), `mimeType` (requis Android, inféré sinon), `role` (`Editor` défaut/`Viewer`/`Shell`/`QLGenerator`/`None`), `rank` (`Default` défaut/`Owner`/`Alternate`/`None`), `name` (défaut première ext), `exportedType` (`identifier` reverse-DNS + `conformsTo` ex `public.data/image/json/plain-text`, requis Apple types custom), `androidIntentActionFilters` (`Send`/`SendMultiple`/`View`, défaut les trois).
- Ouverture : `RunEvent::Opened { urls }` (macOS/iOS/Android). Cold (launch) + warm (runtime) : stocker en `OpenedUrls(Mutex<Vec<Url>>)` + commande `opened_urls` + `app.emit("opened", urls)` côté Rust ; côté JS `invoke('opened_urls')` puis `listen('opened', e => handleFiles(e.payload))`. Voir `examples/mobile-windows.rs` + `examples/mobile-windows.js`.

Valider avec `scripts/check-ui-recettes.py --config examples/tauri.conf.file-associations.json --frontend examples/mobile-windows.js --rust examples/mobile-windows.rs`. `RunEvent::Opened` sans `emit("opened")` = FAIL, `SceneRequested` sans builder = FAIL.
