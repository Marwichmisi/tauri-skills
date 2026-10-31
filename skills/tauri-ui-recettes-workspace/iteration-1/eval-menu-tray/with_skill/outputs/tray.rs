// Cargo (src-tauri/Cargo.toml):
// tauri = { version = "2.0.0", features = [ "tray-icon" ] }

use tauri::{
    Manager,
    menu::{Menu, MenuBuilder, MenuItem},
    tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent},
};

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            // App/window menu (learn/window-menu.mdx): MenuBuilder + set_menu + on_menu_event
            let app_menu = MenuBuilder::new(app)
                .text("open", "Open")
                .check("check_item", "Check Item")
                .separator()
                .text("quit", "Quit")
                .build()?;
            app.set_menu(app_menu)?;

            app.on_menu_event(|app_handle, event| match event.id().0.as_str() {
                "quit" => {
                    app_handle.exit(0);
                }
                "open" => {
                    println!("open event");
                }
                _ => {
                    println!("menu event: {:?}", event.id());
                }
            });

            // Tray menu + icon (learn/system-tray.mdx)
            let quit_i = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;
            let menu = Menu::with_items(app, &[&quit_i])?;

            TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .menu(&menu)
                .show_menu_on_left_click(true)
                .on_menu_event(|app, event| match event.id.as_ref() {
                    "quit" => {
                        println!("quit menu item was clicked");
                        app.exit(0);
                    }
                    _ => {
                        println!("menu item {:?} not handled", event.id);
                    }
                })
                .on_tray_icon_event(|tray, event| match event {
                    TrayIconEvent::Click {
                        button: MouseButton::Left,
                        button_state: MouseButtonState::Up,
                        ..
                    } => {
                        println!("left click pressed and released");
                        let app = tray.app_handle();
                        if let Some(window) = app.get_webview_window("main") {
                            let _ = window.unminimize();
                            let _ = window.show();
                            let _ = window.set_focus();
                        }
                    }
                    _ => {
                        println!("unhandled event {event:?}");
                    }
                })
                .build(app)?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
