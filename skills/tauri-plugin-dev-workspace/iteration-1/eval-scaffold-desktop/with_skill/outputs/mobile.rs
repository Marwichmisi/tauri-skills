// Mobile implementation stub for my-plugin (desktop-first scaffold).
// See tauri-docs develop/Plugins/index.mdx ("Plugin Development"):
// mobile APIs live in `mobile.rs`; full Kotlin/Swift wiring is out of scope
// for this desktop eval (see references/mobile.md for `init` form).

pub struct MyPlugin<R: tauri::Runtime>(std::marker::PhantomData<R>);

impl<R: tauri::Runtime> MyPlugin<R> {
    pub fn upload(&self, _url: String) {
        // mobile fallback for `upload`; Android/iOS projects added via
        // `plugin android add` / `plugin ios add` (index.mdx wording).
    }
}
