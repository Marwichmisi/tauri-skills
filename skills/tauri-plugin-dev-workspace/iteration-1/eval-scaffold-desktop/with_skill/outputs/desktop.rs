// Desktop implementation for my-plugin.
// See tauri-docs develop/Plugins/index.mdx ("Plugin Development"):
// "The plugin APIs defined in the project's `desktop.rs` and `mobile.rs`
//  are exported to the user as a struct with the same name as the plugin
//  (in pascal case)."

pub struct MyPlugin<R: tauri::Runtime>(std::marker::PhantomData<R>);

impl<R: tauri::Runtime> MyPlugin<R> {
    pub fn upload(&self, _url: String) {
        // desktop implementation of `upload` (commands.rs exposes it via invoke_handler)
    }
}
