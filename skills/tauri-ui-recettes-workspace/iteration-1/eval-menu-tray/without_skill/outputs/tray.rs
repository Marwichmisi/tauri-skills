// --- Cargo.toml (extrait) ---
// [dependencies]
// tauri = { version = "2", features = ["tray-icon"] }
// # `tray-icon` active TrayIconBuilder + événements tray.
// # Le support menu natif est inclus via `tauri::menu`.

use tauri::{
    menu::{CheckMenuItemBuilder, MenuBuilder, PredefinedMenuItem},
    tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent},
    Manager,
};

pub fn setup_tray_and_menu(app: &mut tauri::App) -> tauri::Result<()> {
    // 1. Menu natif (app menu)
    let quit = PredefinedMenuItem::quit(app, Some("Quit App"))?;
    let separator = PredefinedMenuItem::separator(app)?;
    let statusbar = CheckMenuItemBuilder::new("Show Status Bar")
        .id("show-statusbar")
        .checked(true)
        .build(app)?;

    let menu = MenuBuilder::new(app)
        .item(&quit)
        .item(&separator)
        .item(&statusbar)
        .build()?;

    app.set_menu(menu)?;

    // Exemple get/setText côté Rust
    // (récupération via id après construction)
    if let Some(item) = app.menu().and_then(|m| m.get("show-statusbar")) {
        // MenuItemKind -> downcast si besoin ; ici exemple Check item
        let _current: String = item.as_check_menuitem_unchecked().text()?;
        item.as_check_menuitem_unchecked()
            .set_text("Show Status Bar (enabled)")?;
    }

    // 2. Tray icon avec menu dédié
    let tray_show = CheckMenuItemBuilder::new("Show window")
        .id("tray-show")
        .checked(true)
        .build(app)?;
    let tray_quit = PredefinedMenuItem::quit(app, Some("Quit"))?;
    let tray_sep = PredefinedMenuItem::separator(app)?;

    let tray_menu = MenuBuilder::new(app)
        .item(&tray_show)
        .item(&tray_sep)
        .item(&tray_quit)
        .build()?;

    let _tray = TrayIconBuilder::new()
        .id("main-tray")
        .icon(app.default_window_icon().unwrap().clone())
        .tooltip("My Tauri app")
        .menu(&tray_menu)
        .menu_on_left_click(true)
        .on_menu_event(|app, event| {
            // event.id() -> id string défini dans les builders
            match event.id().as_ref() {
                "tray-show" => {
                    if let Some(win) = app.get_webview_window("main") {
                        let _ = win.show();
                    }
                }
                "show-statusbar" => {
                    println!("statusbar toggled");
                }
                _ if event.id() == quit_id() => {
                    app.exit(0);
                }
                _ => {}
            }
        })
        .on_tray_icon_event(|tray, event| {
            if let TrayIconEvent::Click {
                button: MouseButton::Left,
                button_state: MouseButtonState::Up,
                ..
            } = event
            {
                println!("tray left click: {:?}", tray.id());
            }
        })
        .build(app)?;

    Ok(())
}

fn quit_id() -> String {
    // `PredefinedMenuItem::quit` utilise un id interne ; on le compare
    // par texte dans cet exemple simplifié (baseline sans doc).
    "quit".to_string()
}

// --- main.rs ---
// fn main() {
//     tauri::Builder::default()
//         .setup(|app| setup_tray_and_menu(app))
//         .on_menu_event(|app, event| {
//             println!("menu event: {}", event.id().as_ref());
//             if event.id().as_ref() == "show-statusbar" {
//                 let _ = app;
//             }
//         })
//         // `on_tray_icon_event` global alternatif au closure builder :
//         // .on_tray_icon_event(|app, event| { ... })
//         .run(tauri::generate_context!())
//         .expect("failed to run app");
// }
