use std::sync::Mutex;
use tauri::{Builder, Manager};

#[derive(Default)]
struct AppState {
  counter: u32,
}

#[tauri::command]
fn increase_counter(state: tauri::State<'_, Mutex<AppState>>) -> u32 {
  let mut state = state.lock().unwrap();
  state.counter += 1;
  state.counter
}

fn main() {
  Builder::default()
    .setup(|app| {
      app.manage(Mutex::new(AppState::default()));
      Ok(())
    })
    .invoke_handler(tauri::generate_handler![increase_counter])
    .run(tauri::generate_context!())
    .unwrap();
}
