use tauri::{
    plugin::{Builder, TauriPlugin},
    Manager, Runtime,
};

mod commands;
mod desktop;
mod mobile;

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error("plugin error: {0}")]
    Plugin(String),
    #[error("mobile not supported on this target")]
    MobileNotSupported,
}

impl From<Error> for tauri::InvokeError {
    fn from(e: Error) -> Self {
        Self::from(e.to_string())
    }
}

pub type Result<T> = std::result::Result<T, Error>;

/// Entry point for the `my-plugin` Tauri v2 plugin.
pub fn init<R: Runtime>() -> TauriPlugin<R> {
    Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![commands::upload])
        .setup(|app, _api| {
            let _handle = app.handle().clone();
            log::info!("my-plugin setup");
            Ok(())
        })
        .build()
}
