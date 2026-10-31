# Architecture — extrait doc

Sources (toutes commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/concept/architecture.mdx` (titre `Tauri Architecture`)
- `tauri-docs/src/content/docs/concept/index.mdx` (titre `Core Concepts`)

## Introduction (architecture.mdx)

> Tauri is a polyglot and generic toolkit that is very composable and allows engineers to make a wide variety of applications. It is used for building applications for desktop computers using a combination of Rust tools and HTML rendered in a Webview. Apps built with Tauri can ship with any number of pieces of an optional JS API and Rust API so that webviews can control the system via message passing. Developers can extend the default API with their own functionality and bridge the Webview and Rust-based backend easily.
>
> Tauri apps can have [tray-type interfaces](/learn/system-tray/). They can be [updated](/plugin/updater/) and are managed by the user's operating system as expected. They are very small because they use the OS's webview. They do not ship a runtime since the final binary is compiled from Rust.

### What Tauri is Not (même fichier)

> Tauri is not a lightweight kernel wrapper. Instead, it directly uses WRY and TAO to do the heavy lifting in making system calls to the OS.
>
> Tauri is not a VM or virtualized environment. Instead, it is an application toolkit that allows making Webview OS applications.

## Core Ecosystem (même fichier)

- `tauri` : major crate, reads `tauri.conf.json` at compile time, handles script injection, hosts the API, manages updating. ([View on GitHub](https://github.com/tauri-apps/tauri/tree/dev/crates/tauri))
- `tauri-runtime` : glue layer between Tauri itself and lower-level webview libraries.
- `tauri-macros` : macros for the context, handler, and commands via `tauri-codegen`.
- `tauri-utils` : parsing configuration files, detecting platform triples, injecting the CSP, managing assets.
- `tauri-build` : applies the macros at build-time to rig special features needed by `cargo`.
- `tauri-codegen` : embeds, hashes, compresses assets; parses `tauri.conf.json` at compile time and generates the Config struct.
- `tauri-runtime-wry` : direct systems-level interactions for WRY (printing, monitor detection, windowing tasks).

## Tauri Tooling (même fichier)

- API (JavaScript / TypeScript) : `cjs` and `esm` endpoints so the Webview can call and listen to backend activity via webview message passing.
- Bundler (Rust / Shell) : builds a Tauri app for the detected platform (macOS, Windows, Linux).
- `cli.rs` (Rust) : full interface to required CLI activities; runs on macOS, Windows, Linux.
- `cli.js` (JavaScript) : wrapper around `cli.rs` using `napi-rs`.
- `create-tauri-app` : scaffolds a new project with the frontend framework of choice.

## Upstream Crates (même fichier)

> The Tauri-Apps organization maintains two "upstream" crates from Tauri, namely TAO for creating and managing application windows, and WRY for interfacing with the Webview that lives within the window.

- TAO : cross-platform application window creation library in Rust (Windows, macOS, Linux, iOS, Android), fork of `winit` extended for menu bar and system tray.
- WRY : cross-platform WebView rendering library in Rust (desktop Windows, macOS, Linux). Tauri uses WRY as the abstract layer responsible to determine which webview is used.

## Plugins (même fichier)

> Generally speaking, plugins are authored by third parties (even though there may be official, supported plugins). A plugin generally does 3 things:
> 1. Enables Rust code to do "something".
> 2. Provides interface glue to make it easy to integrate into an app.
> 3. Provides a JavaScript API for interfacing with the Rust code.

## Index (index.mdx)

> Tauri has a variety of topics that are considered to be core concepts, things any developer should be aware of when developing their applications.
> Topics: Tauri Architecture, Inter-Process Communication (IPC), Security, Process Model, App Size.
