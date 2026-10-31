# Placement Core vs Webview + Events vs Commands — App 2 fenêtres, secrets, état global

> Sources : `tauri-docs/` local, commit `ec113a50`, EN canonique seule (doctrine `tauri-core-concepts`).
> Références lues : `references/process-model.md`, `references/ipc-patterns.md`, `references/architecture.md`.

## 1. Où placer chaque chose

### Secrets d'API → Core Rust, jamais Webview

Règle de `references/process-model.md` (extrait de `concept/process-model.md`) :

> « never handle secrets in the Frontend, and ideally defer as much business logic as possible to the Core process to keep your attack surface small. »

> « The Core process should also be responsible for managing global state, such as settings or database connections. This allows you to easily synchronize state between windows and protect your business-sensitive data from prying eyes in the Frontend. »

Donc :
- Clés d'API, tokens, logique d'appel au service tiers : **Core Rust uniquement**.
- Le Webview ne voit que des données déjà traitées / expurgées, jamais le secret brut.
- Justification architecture : seul le Core « is the only component with full access to the operating system » (`concept/process-model.md` — The Core Process). Le Webview n'est qu'un « browser-like environment that executes your HTML, CSS, and JavaScript » utilisant la webview de l'OS (WebView2 / WKWebView / webkitgtk) — pas faite pour garder un secret.

À l'inverse, ne pas mettre les secrets en `localStorage`, en variable JS, ni les faire transiter en clair vers le frontend via Event/Command.

### État global partagé entre 2 fenêtres → Core Rust

Même source :

> « The Core process should also be responsible for managing global state, such as settings or database connections. This allows you to easily synchronize state between windows [...] »

Donc :
- Settings, connexion DB, cache partagé : **état détenu par le Core** (cf. `tauri-ipc-bridge` pour l'implémentation `State`/`Mutex`, hors périmètre conception ici).
- Les 2 Webviews (2 fenêtres = 2 WebView processes, architecture multi-process « similar to Electron or many modern web browsers », `concept/process-model.md`) ne détiennent qu'une **copie d'affichage**. Elles demandent/modifient via IPC, le Core arbitre.
- Bénéfices cités par la doc : isolation des crashs (« A crash in one component doesn't affect the whole system ») + moindre privilège (« Principle of Least Privilege [...] handing out only the minimum amount of permissions to each process »).

### UI, saisie utilisateur → Webview, avec assainissement

> « most of your techniques and tools used in traditional web development can be used » + « you must always sanitize user input » (`concept/process-model.md` — The WebView Process).

Donc : rendu HTML/CSS/JS et validation/sanitization d'entrée côté Webview, puis envoi au Core pour traitement métier.

## 2. Events vs Commands

Source : `references/ipc-patterns.md` (extraits de `concept/Inter-Process Communication/index.mdx`).

### Commands = appel requête/réponse

> « The primary API, `invoke`, is similar to the browser's `fetch` API and allows the Frontend to invoke Rust functions, pass arguments, and receive data. »
> « all arguments and return data must be serializable to JSON. »

Utiliser **Commands** quand :
- Le frontend demande une action ou une lecture au Core et attend un retour : `get_settings()`, `update_setting(key, value)`, `fetch_data_via_api(query)`.
- C'est du « foreign function interface-like abstraction on top of IPC messages », toujours du message-passing (pas de vrai FFI partagé — « they do not share the same security pitfalls as real FFI »).

Exemple pour ce cas : les 2 fenêtres appellent `invoke('get_state')` au démarrage et `invoke('set_state', ...)` pour modifier.

### Events = notification fire-and-forget de changement d'état

> « Events are fire-and-forget, one-way IPC messages that are best suited to communicate lifecycle events and state changes. Unlike Commands, Events can be emitted by both the Frontend _and_ the Tauri Core. »

Utiliser **Events** quand :
- Le Core notifie les frontends que l'état a changé : `state-changed`, `settings-updated`, lifecycle (`window-created`, etc.).
- Pas de réponse attendue, diffusion à 1 ou N fenêtres. C'est exactement le besoin « notifications de changement d'état vers le frontend ».
- Note : « Under the hood, events still utilize Commands » — le choix est sémantique (sens unique vs requête/réponse), pas un canal physiquement distinct.

### Tableau de décision pour cette app

| Besoin | Primitive | Sens |
|---|---|---|
| Fenêtre lit l'état global | Command `invoke` | Webview → Core, avec retour JSON |
| Fenêtre modifie l'état / appelle l'API tierce (clé restée au Core) | Command `invoke` | Webview → Core, Core exécute avec secret |
| Core prévient les 2 fenêtres que l'état a changé | Event `emit` | Core → Webviews (fire-and-forget) |
| Une fenêtre prévient l'autre d'un lifecycle local (optionnel) | Event | Webview → (Core) → Webview, les Events pouvant être émis des deux côtés |

Le routage IPC passe toujours par le Core : « It also routes all Inter-Process Communication through the Core process, allowing you to intercept, filter, and manipulate IPC messages in one central place. » (`concept/process-model.md`). Voir `references/ipc-patterns.md` + skill `tauri-ipc-bridge` pour le filtrage effectif.

## 3. Quel pattern IPC : brownfield (défaut) vs isolation

- **Défaut : brownfield.** « _This is the default pattern._ [...] tries to require nothing additional to what an existing web frontend might use » (`concept/Inter-Process Communication/brownfield.md`). « There are no additional configuration options ». Suffisant si frontend de confiance, dépendances maîtrisées.
- **Isolation si contenu / dépendances non fiables.** « protects against unwanted or malicious frontend calls from untrusted content / deeply-nested frontend dependencies » ; « Tauri highly recommends using the isolation pattern whenever it can be used. Because the Isolation application intercepts _all_ messages [...] it can _always_ be used » (`concept/Inter-Process Communication/isolation.md`). Fonctionnement : `<iframe>` sandboxée entre frontend et Core, hook `window.__TAURI_ISOLATION_HOOK__`, chiffrement AES-GCM à clé régénérée par run. Coût : overhead chiffrement (« usually negligible »), pas de modules ES externes dans l'app d'isolation, la garder « as simple as possible ».
- Pour cette app à secrets : brownfield acceptable en interne ; passer en isolation si les 2 fenêtres chargent du contenu tiers ou beaucoup de dépendances npm profondes, et y vérifier les entrées IPC (« verify IPC inputs [...] within some expected parameters »).

## 4. Hors périmètre (renvoyé aux skills frères)

- Permissions/scopes/CSP/capabilities exactes → `tauri-security-capabilities` (ici aucune permission déclarée, doctrine anti-drift).
- Code `invoke`/`listen`/`emit`, `State`, resources → `tauri-ipc-bridge`.
- Schéma complet `tauri.conf.json` → `tauri-config-cli-reference` (ici seuls les snippets `app.security.pattern` brownfield/isolation sont pertinents).
