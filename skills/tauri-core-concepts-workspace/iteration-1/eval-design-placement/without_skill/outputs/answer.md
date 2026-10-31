# Placement Core Rust vs Webview + Events vs Commands — App Tauri 2 fenêtres, secrets, état partagé

## 1. Rappel architecture coeur

Tauri = 2 couches :
- **Core Rust (backend, process principal)** : accès système, réseau, fichiers, secrets, état partagé, logique métier. Tourne en dehors du web.
- **Webview (frontend)** : rendu UI HTML/JS, interaction utilisateur. Chaque fenêtre = une webview isolée, sans accès direct au système.

Communication pont IPC :
- **Commands** : appel RPC frontend -> backend avec réponse (`invoke()` JS -> `#[tauri::command]` Rust).
- **Events** : diffusion pub/sub asynchrone (`emit` / `listen`), dans les deux sens, utile pour notifier plusieurs fenêtres.

## 2. Où placer chaque chose

### a) Secrets d'API -> Core Rust uniquement

**Ne jamais mettre un secret en Webview.**
Le code frontend (JS, variables d'env build-time via Vite, `localStorage`) est inspectable via DevTools et extrait du bundle. Tout appel API direct depuis le frontend expose la clé.

Placement recommandé :
- Stocker en Rust : variable d'environnement au runtime, fichier de config OS, ou trousseau système (keyring) via crate dédiée.
- Charger au `setup()` et garder en `State` ou config interne, jamais renvoyé tel quel au frontend.
- Exposer uniquement des Commands métier limitées, ex. `fetch_weather(city)` qui injecte la clé côté Rust et renvoie seulement le résultat utile.
- Verrouiller les capacités (Tauri v2 `capabilities` / v1 `allowlist`) : pas de `http` / `fs` / `shell` côté frontend si le backend s'en charge.

### b) État global partagé entre 2 fenêtres -> Core Rust (Managed State)

**Ne pas dupliquer l'état dans chaque Webview** (divergence, race conditions, `localStorage` non synchronisé).

Placement recommandé :
- Struct Rust, ex. `struct AppState { counter: Mutex<AppData> }`, enregistré avec `app.manage(AppState::default())` dans `Builder::setup`.
- Les 2 fenêtres accèdent au même objet via `State<AppState>` injecté dans les Commands : `get_state()`, `update_state(new_val)`.
- Frontend = état local dérivé / cache d'affichage uniquement (ex. React state miroir), re-synchronisé depuis le backend.
- Protéger avec `Mutex` / `RwLock` car les Commands tournent sur un pool async multi-thread.

### c) UI et interaction -> Webview

- Rendu, formulaires, affichage des 2 fenêtres.
- Chaque fenêtre appelle `invoke('get_state')` au démarrage pour s'initialiser, puis `invoke('update_state', ...)` pour modifier.
- Pas de logique métier critique ni de secret en JS.

## 3. Quand utiliser Events vs Commands

| Besoin | Primitive | Sens | Pourquoi |
|---|---|---|---|
| Lire / modifier l'état, appeler une API avec secret, action avec résultat | **Command** | Frontend -> Backend (request/response) | Besoin de retour / erreur typée, appel ponctuel. Ex. `invoke('set_theme', {theme}) -> Result<...>` |
| Notifier les 2 fenêtres qu'un état a changé | **Event** | Backend -> Frontends (broadcast) | Une mutation via Command doit propager à N fenêtres sans polling. Backend fait `app.emit("state-changed", payload)` après mutation ; chaque fenêtre fait `listen("state-changed", ...)` pour se rafraîchir. |
| Signalement fire-and-forget frontend -> backend sans réponse attendue | **Event** | Frontend -> Backend | Ex. `emit("user-idle")`. Rare ; préférer Command si accusé nécessaire. |

**Pattern complet :**
1. Fenêtre A : `invoke('update_state', data)` (Command).
2. Rust : lock `State`, mute, puis `handle.emit("state-changed", new_snapshot)` (Event).
3. Fenêtres A + B : handler `listen("state-changed")` met à jour l'UI.

Ne pas utiliser Events pour transporter des secrets ; ne pas utiliser Commands en polling pour simuler du push (coûteux, latent).

## 4. Résumé décision

- Secrets : **Core Rust**, exposés via Commands métier, jamais en Webview.
- État partagé : **Core Rust `manage` + `State`**, source unique ; Webview = miroir.
- Mutation ponctuelle / lecture avec réponse : **Commands**.
- Diffusion changement d'état vers N fenêtres : **Events (`emit` backend -> `listen` frontend)**.

## Sources (connaissance générale Tauri)

- Tauri Docs — Architecture / Core Process vs Webview : `https://tauri.app/v1/references/architecture/` et `https://v2.tauri.app/concept/architecture/`
- Tauri Docs — State Management (`manage`, `State`) : `https://tauri.app/v1/guides/features/state-management/` / v2 `https://v2.tauri.app/develop/state-management/`
- Tauri Docs — Calling Rust from Frontend (Commands, `#[tauri::command]`, `invoke`) : `https://v2.tauri.app/develop/calling-rust/`
- Tauri Docs — Events (`emit`, `listen`, frontend/backend) : `https://v2.tauri.app/develop/calling-frontend/#events` et `https://tauri.app/v1/guides/features/events/`
- Tauri Docs — Security / Capabilities, jamais de secret frontend : `https://v2.tauri.app/reference/capabilities/` et guides security
