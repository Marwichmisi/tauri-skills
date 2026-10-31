# IPC Patterns — Events, Commands, Brownfield, Isolation

Sources (toutes commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/concept/Inter-Process Communication/index.mdx` (titre `Inter-Process Communication`)
- `tauri-docs/src/content/docs/concept/Inter-Process Communication/brownfield.md` (titre `Brownfield Pattern`)
- `tauri-docs/src/content/docs/concept/Inter-Process Communication/isolation.md` (titre `Isolation Pattern`)

## Message passing (index.mdx)

> Tauri uses a particular style of Inter-Process Communication called Asynchronous Message Passing, where processes exchange _requests_ and _responses_ serialized using some simple data representation.
>
> Message passing is a safer technique than shared memory or direct function access because the recipient is free to reject or discard requests as it sees fit. For example, if the Tauri Core process determines a request to be malicious, it simply discards the requests and never executes the corresponding function.

## Events (index.mdx)

> Events are fire-and-forget, one-way IPC messages that are best suited to communicate lifecycle events and state changes. Unlike Commands, Events can be emitted by both the Frontend _and_ the Tauri Core.

> Under the hood, events still utilize Commands, and the access to the events API is controlled by the Event permissions.

## Commands (index.mdx)

> Tauri also provides a foreign function interface-like abstraction on top of IPC messages. The primary API, `invoke`, is similar to the browser's `fetch` API and allows the Frontend to invoke Rust functions, pass arguments, and receive data.
>
> Because this mechanism uses a JSON-RPC like protocol under the hood to serialize requests and responses, all arguments and return data must be serializable to JSON.

Footnote (même fichier) : Commands still use message passing under the hood, they do not share the same security pitfalls as real FFI interfaces do.

## Brownfield — default pattern (brownfield.md)

> _**This is the default pattern.**_
>
> This is the simplest and most straightforward pattern to use Tauri with, because it tries to be as compatible as possible with existing frontend projects. In short, it tries to require nothing additional to what an existing web frontend might use inside a browser.

Configuration (même fichier) : default, pas d'option requise. Forme explicite (voir `examples/brownfield-pattern.json`) :

```json
{
  "app": {
    "security": {
      "pattern": {
        "use": "brownfield"
      }
    }
  }
}
```

> _**There are no additional configuration options for the brownfield pattern.**_

## Isolation — quand et comment (isolation.md)

> The Isolation pattern is a way to intercept and modify Tauri API messages sent by the frontend before they get to Tauri Core, all with JavaScript. The secure JavaScript code that is injected by the Isolation pattern is referred to as the Isolation application.

Why (même fichier) : protects against unwanted or malicious frontend calls from untrusted content / deeply-nested frontend dependencies (Development Threats, see Security Threat Models).

When (même fichier) :

> Tauri highly recommends using the isolation pattern whenever it can be used. Because the Isolation application intercepts _**all**_ messages from the frontend, it can _always_ be used.

> Tauri also strongly suggests locking down your application whenever you use external Tauri APIs. As the developer, you can utilize the secure Isolation application to try and verify IPC inputs, to make sure they are within some expected parameters.

How (même fichier) : sandboxed `<iframe>` injected between frontend and Core; all IPC routed through it first; message encrypted with AES-GCM via `SubtleCrypto` with a runtime-generated key (new keys each run), then passed to Core for decryption.

Approximate steps (même fichier) :

1. Tauri's IPC handler receives a message
2. IPC handler -> Isolation application
3. `[sandbox]` Isolation application hook runs and potentially modifies the message
4. `[sandbox]` Message is encrypted with AES-GCM using a runtime-generated key
5. `[encrypted]` Isolation application -> IPC handler
6. `[encrypted]` IPC handler -> Tauri Core

Performance (même fichier) : overhead from encryption even if hook does nothing; usually negligible (AES-GCM fast); key generation needs entropy (install `haveged` headless if needed; Linux 5.6+ OK).

Limitations (même fichier) : external files don't load in sandboxed `<iframe>` on Windows → build-time script inlining; `<script src="index.js">` works, ES Modules will _not_ load.

Recommendations (même fichier) : keep the Isolation application as simple as possible, minimal dependencies and build steps (avoid supply-chain attacks on the Isolation app itself).

Hook (même fichier, voir `examples/isolation-hook.js`) :

```javascript
window.__TAURI_ISOLATION_HOOK__ = (payload) => {
  // let's not verify or modify anything, just print the content from the hook
  console.log('hook', payload);
  return payload;
};
```

Configuration (même fichier, voir `examples/isolation-pattern.json`) :

```json
{
  "build": {
    "frontendDist": "../dist"
  },
  "app": {
    "security": {
      "pattern": {
        "use": "isolation",
        "options": {
          "dir": "../dist-isolation"
        }
      }
    }
  }
}
```

## Choix Events vs Commands (décision fidèle)

- Changement d'état / lifecycle, fire-and-forget, émis des deux côtés → Events.
- Appel de fonction Rust avec arguments/retour JSON, style `fetch`/`invoke` → Commands.
- Détail d'implémentation (code `invoke`, `listen`/`emit`, scopes) → `tauri-ipc-bridge`.
