# Process Model — extrait doc

Source : `tauri-docs/src/content/docs/concept/process-model.md`, commit `ec113a50`, titre `Process Model`.

> Tauri employs a multi-process architecture similar to Electron or many modern web browsers.

## Why Multiple Processes? (même fichier)

> Applications began running different components in different processes. This makes much better use of modern multi-core CPUs and creates far safer applications. A crash in one component doesn't affect the whole system anymore, as components are isolated on different processes. If a process gets into an invalid state, we can easily restart it.
>
> We can also limit the blast radius of potential exploits by handing out only the minimum amount of permissions to each process, just enough so they can get their job done. This pattern is known as the Principle of Least Privilege.

## The Core Process (même fichier)

> Each Tauri application has a core process, which acts as the application's entry point and which is the only component with full access to the operating system.
>
> The Core's primary responsibility is to use that access to create and orchestrate application windows, system-tray menus, or notifications. Tauri implements the necessary cross-platform abstractions to make this easy. It also routes all Inter-Process Communication through the Core process, allowing you to intercept, filter, and manipulate IPC messages in one central place.
>
> The Core process should also be responsible for managing global state, such as settings or database connections. This allows you to easily synchronize state between windows and protect your business-sensitive data from prying eyes in the Frontend.
>
> We chose Rust to implement Tauri because of its concept of Ownership [which] guarantees memory safety while retaining excellent performance.

## The WebView Process (même fichier)

> The Core process doesn't render the actual user interface (UI) itself; it spins up WebView processes that leverage WebView libraries provided by the operating system. A WebView is a browser-like environment that executes your HTML, CSS, and JavaScript.
>
> This means that most of your techniques and tools used in traditional web development can be used to create Tauri applications.
>
> Security best practices apply as well; for example, you must always sanitize user input, never handle secrets in the Frontend, and ideally defer as much business logic as possible to the Core process to keep your attack surface small.
>
> Unlike other similar solutions, the WebView libraries are **not** included in your final executable but dynamically linked at runtime. This makes your application _significantly_ smaller, but it also means that you need to keep platform differences in mind, just like traditional web development.

Footnote (même fichier) : Windows = Microsoft Edge WebView2, macOS = WKWebView, Linux = webkitgtk.

## Règle de conception (synthèse fidèle, rien d'inventé)

- Secrets, état global, connexions base de données → Core Rust, jamais Frontend.
- Entrées utilisateur → toujours assainies côté Frontend ; logique métier → Core autant que possible.
- IPC centralisé et filtrable au Core (voir `references/ipc-patterns.md` pour Events vs Commands).
