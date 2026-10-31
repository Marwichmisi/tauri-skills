# Tray — Cargo, icône, menu, events

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/learn/system-tray.mdx` (titre `System Tray`)

> Tauri allows you to create and customize a system tray for your application. This can enhance the user experience by providing quick access to common actions.

## Config (même fichier)

```toml title="src-tauri/Cargo.toml"
tauri = { version = "2.0.0", features = [ "tray-icon" ] }
```

## Créer (même fichier)

- JS : `TrayIcon.new(options)` (`TrayIconOptions`). Rust : `TrayIconBuilder::new().build(app)?` (`TrayIconBuilder`, docs.rs linké jamais copié).

## Icône (même fichier)

- JS : `icon: await defaultWindowIcon()`. Rust : `.icon(app.default_window_icon().unwrap().clone())`.

## Menu (même fichier, voir `references/menus.md` pour le détail items)

> By default the menu is displayed on both left and right clicks. To prevent the menu from popping up on left click, call the `show_menu_on_left_click(false)` Rust function or set the `menuOnLeftClick` JavaScript option to `false`.

- JS : `Menu.new({ items: [{ id: 'quit', text: 'Quit' }] })` puis `TrayIcon.new({ menu, menuOnLeftClick: true })`. Click JS : `action` partagée ou dédiée par item.
- Rust : `MenuItem::with_id(app, "quit", "Quit", true, None)` + `Menu::with_items(app, &[&quit_i])` + `TrayIconBuilder::new().menu(&menu).show_menu_on_left_click(true)`. Click Rust : `.on_menu_event(|app, event| match event.id.as_ref() { "quit" => app.exit(0), _ => ... })`.

## Events tray (même fichier)

- Types doc seuls : `Click` (`button` + `buttonState`), `DoubleClick`, `Enter`, `Move`, `Leave`. Linux : Unsupported (icône affichée, event non émis, menu contextuel au clic droit).
- JS : `action: (event) => switch (event.type)`. Rust : `.on_tray_icon_event(|tray, event| match event { TrayIconEvent::Click { button: MouseButton::Left, button_state: MouseButtonState::Up, .. } => { app.get_webview_window("main") → unminimize/show/set_focus }, _ => ... })`.

Valider avec `scripts/check-ui-recettes.py --frontend examples/tray.js`. `TrayIcon.create` inventé rejeté.
