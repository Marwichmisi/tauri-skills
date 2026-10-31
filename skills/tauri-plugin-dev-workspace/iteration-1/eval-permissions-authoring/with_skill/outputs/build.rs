#[path = "src/scope.rs"]
mod scope;

const COMMANDS: &[&str] = &["upload"];

fn main() {
    tauri_plugin::Builder::new(COMMANDS)
        .global_scope_schema(schemars::schema_for!(scope::Entry))
        .build();
}
