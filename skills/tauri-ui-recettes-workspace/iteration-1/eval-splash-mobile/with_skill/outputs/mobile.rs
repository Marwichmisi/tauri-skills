use std::sync::Mutex;
use tauri::Manager;

struct OpenedUrls(Mutex<Vec<tauri::Url>>);

#[tauri::command]
fn opened_urls(app: tauri::AppHandle) -> Vec<tauri::Url> {
    app.state::<OpenedUrls>().0.lock().unwrap().clone()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    #[cfg(target_os = "ios")]
    let mut counter = 0;

    tauri::Builder::default()
        .manage(OpenedUrls(Mutex::new(vec![])))
        .invoke_handler(tauri::generate_handler![opened_urls])
        .setup(|app| {
            tauri::WebviewWindowBuilder::new(
                app, "main", tauri::WebviewUrl::default(),
            )
            .build()?;
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run(move |app, event| {
            #[cfg(target_os = "ios")]
            if let tauri::RunEvent::SceneRequested { .. } = event {
                counter += 1;
                tauri::WebviewWindowBuilder::new(
                    app,
                    format!("main-{counter}"),
                    tauri::WebviewUrl::default(),
                )
                .build()
                .unwrap();
            }
            #[cfg(any(target_os = "macos", target_os = "ios", target_os = "android"))]
            if let tauri::RunEvent::Opened { urls } = event {
                use tauri::Emitter;
                app.state::<OpenedUrls>()
                    .0
                    .lock()
                    .unwrap()
                    .extend(urls.clone());
                app.emit("opened", urls).unwrap();
            }
            #[cfg(not(target_os = "ios"))]
            let _ = (app, event);
        });
}

// Android multi-window: create a detail window bound to DetailActivity
#[allow(dead_code)]
fn open_detail(main: &tauri::WebviewWindow) -> tauri::Result<tauri::WebviewWindow> {
    let builder = tauri::WebviewWindowBuilder::new(main, "detail", tauri::WebviewUrl::App("detail/1".into()));
    #[cfg(target_os = "android")]
    let builder = builder.activity_name("DetailActivity");
    builder.build()
}
