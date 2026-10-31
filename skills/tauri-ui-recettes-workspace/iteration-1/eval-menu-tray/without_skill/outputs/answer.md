# Menus + Tray natifs desktop (Tauri v2) — baseline sans skill

> Baseline produite de mémoire (connaissance générale), sans lecture de doc.

## 1. Quand utiliser quoi

| Besoin | API |
|---|---|
| Menu bar native (macOS) / menu fenêtre | `Menu` (`@tauri-apps/api/menu`) côté JS, `MenuBuilder` côté Rust |
| Items cochables | `CheckMenuItem` / `CheckMenuItemBuilder` |
| Quit / Separator natifs | `PredefinedMenuItem` (`item: 'Quit'`, `item: 'Separator'`) |
| Icône zone de notification | `TrayIcon` (`@tauri-apps/api/tray`) côté JS, `TrayIconBuilder` côté Rust |
| Clic gauche ouvre le menu tray | `menuOnLeftClick: true` (JS) / `.menu_on_left_click(true)` (Rust) |

Desktop uniquement. Ne pas appeler depuis mobile/web pur.

## 2. JS — Menu (`menu.js`)

- `Menu.new({ items: [...] })` accepte des descripteurs `{ id, text, accelerator, action }` ou des instances (`MenuItem`, `CheckMenuItem`, `PredefinedMenuItem`).
- `await using menu = await Menu.new(...)` : pattern Explicit Resource Management pour fermer le handle en fin de scope.
- `await menu.setAsAppMenu()` : installe comme menu applicatif.
- `await item.text()` / `await item.setText('...')` : lecture/renommage dynamique.

Voir `menu.js`.

## 3. JS — Tray (`tray.js`)

```js
await TrayIcon.new({
  id: 'main-tray',
  icon: 'icons/32x32.png',
  tooltip: 'My Tauri app',
  menu: trayMenu,
  menuOnLeftClick: true,
  action: (event) => { /* Click / DoubleClick ... */ },
});
```

- `menu` : instance `Menu` construite au préalable (avec quit/check/separator).
- `menuOnLeftClick: true` : le clic gauche ouvre le menu (sinon seul le clic droit l'ouvre selon OS).
- `TrayIcon.getById(id)` pour retrouver l'instance, `setTooltip`, `setVisible`.

Voir `tray.js`.

## 4. Rust — `tray.rs`

- `Cargo.toml` : activer `tauri` avec `features = ["tray-icon"]`.
- Builders :
  - `MenuBuilder::new(app).item(&...).build()?`
  - `CheckMenuItemBuilder::new("label").id("...").checked(true).build(app)?`
  - `PredefinedMenuItem::quit(app, ...)` / `::separator(app)?`
  - `TrayIconBuilder::new().id(...).icon(...).tooltip(...).menu(&menu).menu_on_left_click(true)...build(app)?`
- Événements :
  - `.on_menu_event(|app, event| match event.id().as_ref() { ... })` sur le builder tray, ou `.on_menu_event(...)` global sur `tauri::Builder`.
  - `.on_tray_icon_event(|tray, event| ...)` avec `TrayIconEvent::Click { button: MouseButton::Left, button_state: MouseButtonState::Up, .. }`.
- `app.set_menu(menu)` pour le menu applicatif, `item.text()` / `set_text()` pour get/setText.

Voir `tray.rs`.

## 5. Limites connues de cette baseline

- Écrite sans vérification doc : noms exacts (`menuOnLeftClick` vs `menu_on_left_click`, forme `TrayIconEvent::Click`, ids des predefined items) à confirmer contre la doc Tauri v2.
- Icône tray : format attendu (PNG 32px vs `Image` bytes) variable selon version.
- `await using` requiert toolchain récente ; sinon utiliser `try/finally` + `menu.close()`.
