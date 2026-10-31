const COMMANDS: &[&str] = &["upload"];

fn main() {
    tauri_plugin::Builder::new(COMMANDS).build();
}
