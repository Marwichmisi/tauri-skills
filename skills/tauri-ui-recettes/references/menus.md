# Menus fenêtre — base, multi-niveaux, prédéfinis, events, leaks

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/learn/window-menu.mdx` (titre `Window Menu`)

> Native application menus can be attached to both to a window or system tray. Available on desktop.

> Starting from Tauri 2.12, the JavaScript menu APIs now support Explicit Resource Management. Which allows you to use the `await using` syntax that closes the menu resources automatically.

## Base (même fichier)

- JS : `Menu.new({ items: [{ id, text, action }, { item: 'Separator' }] })` puis `menu.setAsAppMenu()`, lecture `menu.get('status')` → `setText`. Rust : `MenuBuilder::new(app).text("open","Open").check(...).separator().build()?` puis `app.set_menu(menu)`.

## Multi-niveaux (même fichier)

- JS : `Submenu.new({ text, items, icon })` (`File`, `Edit`, `About` en premier sur macOS — top-level ignorés sinon, premier submenu sous About OS). `setIcon` / `setNativeIcon` dynamiques. Rust : `SubmenuBuilder::new(app, "File").submenu_icon(image).text(...).build()?` + `CheckMenuItemBuilder` (`id`, `checked`, `enabled`) + `IconMenuItemBuilder` ; feature `image-ico`/`image-png` requise (`tauri = { features = ["image-png"] }`).
- macOS : tout sous submenu, sinon ignoré.

## Prédéfinis (même fichier)

- JS : `PredefinedMenuItem.new({ item: 'Copy' | 'Separator' | 'Undo' | 'Redo' | 'Cut' | 'Paste' | 'SelectAll' })`. Rust : `.copy().separator().undo().redo().cut().paste().select_all()` ou `PredefinedMenuItem::copy(app, Some("custom text"))`.

## Events + statut (même fichier)

- JS : `action: () => {}` par item. Rust : `app.on_menu_event(|app_handle, event| match event.id().0.as_str() { "open" => ..., _ => ... })`. Changement statut : `set_menu` à nouveau, `set_text` / `set_icon` / `set_checked` / `set_accelerator`.

## Anti-leak JS (même fichier, discriminant)

> The menus will not clean up automatically unless `close` is called or closed by `await using` after the binding variable goes out of scope.
> You should close the menu items you got e.g. from `Menu.get`, the `await using` syntax makes it easier.
> You should close the menu resource whenever you don't need to access it in JavaScript anymore.

- Pattern exigé : `await using menu = await Menu.new(...)` + `await using prev = await menu.setAsAppMenu()` + `await menu.close()` quand fini ; `copy` géré par `menu` → `await copy.close()`.

Valider avec `scripts/check-ui-recettes.py --frontend examples/menu.js` (échoue sans `await using` ni `.close()`).
