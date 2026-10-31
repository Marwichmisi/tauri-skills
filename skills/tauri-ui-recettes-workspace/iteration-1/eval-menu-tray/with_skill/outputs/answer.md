# Eval 2 — Menus + tray natifs desktop (Tauri v2)

Sources (commit `ec113a50`, EN canonique seule) :
- `tauri-docs/src/content/docs/learn/window-menu.mdx` (titre `Window Menu`)
- `tauri-docs/src/content/docs/learn/system-tray.mdx` (titre `System Tray`)

> Native application menus can be attached to both to a window or system tray. Available on desktop.
> Starting from Tauri 2.12, the JavaScript menu APIs now support Explicit Resource Management. Which allows you to use the `await using` syntax that closes the menu resources automatically.
> Tauri allows you to create and customize a system tray for your application. This can enhance the user experience by providing quick access to common actions.
> The menus will not clean up automatically unless `close` is called or closed by `await using` after the binding variable goes out of scope.
> By default the menu is displayed on both left and right clicks. To prevent the menu from popping up on left click, call the `show_menu_on_left_click(false)` Rust function or set the `menuOnLeftClick` JavaScript option to `false`.

## 1. Menu fenêtre — JS (`menu.js`)

`Menu.new({ items: [{ id, text, action }, { item: 'Separator' }] })` puis `setAsAppMenu()`, lecture `menu.get('status')` → `setText` (`references/menus.md`, `examples/menu.js`) :

```js
await using menu = await Menu.new({
  items: [
    { id: 'quit', text: 'Quit', action: () => { console.log('quit pressed'); } },
    { id: 'check_item', text: 'Check Item', checked: true },
    { item: 'Separator' },
  ],
});
await using prev = await menu.setAsAppMenu();
await using statusItem = await menu.get('status');
if (statusItem) {
  await statusItem.setText('Status: Ready');
}
```

Anti-leak `learn/window-menu.mdx § Prevent JavaScript menu leaks` : `await using` sur `menu`, sur le retour de `setAsAppMenu()` et sur `menu.get(...)`. Fichier complet : `menu.js`.

## 2. Tray — JS (`tray.js`)

`Menu.new(...)` puis `TrayIcon.new({ menu, menuOnLeftClick: true })`, icône `defaultWindowIcon()`, `action: (event) => switch (event.type)` (`Click`/`DoubleClick`/`Enter`/`Move`/`Leave`) :

```js
await using menu = await Menu.new({
  items: [
    { id: 'quit', text: 'Quit', action: () => { console.log('quit pressed'); } },
    { item: 'Separator' },
  ],
});
const options = {
  icon: await defaultWindowIcon(),
  menu,
  menuOnLeftClick: true,
  action: (event) => { switch (event.type) { /* Click / DoubleClick / ... */ } },
};
const tray = await TrayIcon.new(options);
await menu.close();
```

`TrayIcon.create` / `Menu.create` rejetés (inventés). Fichier complet : `tray.js`.

## 3. Cargo

```toml title="src-tauri/Cargo.toml"
tauri = { version = "2.0.0", features = [ "tray-icon" ] }
```

## 4. Rust (`tray.rs`)

App menu : `MenuBuilder::new(app).text(...).check(...).separator().build()?` + `app.set_menu(menu)` + `app.on_menu_event(|app_handle, event| match event.id().0.as_str() ...)`.
Tray : `MenuItem::with_id(app, "quit", "Quit", true, None)` + `Menu::with_items(app, &[&quit_i])` + `TrayIconBuilder::new().icon(app.default_window_icon().unwrap().clone()).menu(&menu).show_menu_on_left_click(true).on_menu_event(...).on_tray_icon_event(...)` :

```rust
let quit_i = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;
let menu = Menu::with_items(app, &[&quit_i])?;
TrayIconBuilder::new()
  .menu(&menu)
  .show_menu_on_left_click(true)
  .on_menu_event(|app, event| match event.id.as_ref() {
    "quit" => app.exit(0),
    _ => println!("menu item {:?} not handled", event.id),
  })
  .on_tray_icon_event(|tray, event| match event {
    TrayIconEvent::Click { button: MouseButton::Left, button_state: MouseButtonState::Up, .. } => {
      if let Some(window) = tray.app_handle().get_webview_window("main") {
        let _ = window.unminimize();
        let _ = window.show();
        let _ = window.set_focus();
      }
    }
    _ => println!("unhandled event {event:?}"),
  })
  .build(app)?;
```

Fichier complet : `tray.rs`. `TrayBuilder` / `WindowBuilder::` rejetés (doc : `TrayIconBuilder` / `WebviewWindowBuilder`).

## 5. Validation `scripts/check-ui-recettes.py`

```
OK skills/tauri-ui-recettes-workspace/iteration-1/eval-menu-tray/with_skill/outputs/menu.js
 - frontend APIs: Menu.new, setAsAppMenu
OK skills/tauri-ui-recettes-workspace/iteration-1/eval-menu-tray/with_skill/outputs/tray.js
 - frontend APIs: Menu.new, TrayIcon.new, defaultWindowIcon, menuOnLeftClick
OK skills/tauri-ui-recettes-workspace/iteration-1/eval-menu-tray/with_skill/outputs/tray.rs
 - rust APIs: Menu::with_items, MenuBuilder, MenuItem::with_id, TrayIconBuilder, get_webview_window, on_menu_event, on_tray_icon_event, show_menu_on_left_click
```

Contrôle négatif (Menu sans `await using` ni `.close()`) :
```
FAIL /tmp/opencode/leak-test.js
 - menu leak: Menu/Submenu/MenuItem sans 'await using' ni .close() (learn/window-menu.mdx § Prevent JavaScript menu leaks)
```

Artefacts : `menu.js`, `tray.js`, `tray.rs`, `transcript.md` (ce fichier : `answer.md`).
