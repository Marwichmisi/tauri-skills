# Inventaire exhaustif tauri-docs v2 locale — ticket #2

- Source canonique : `tauri-docs/` local, commit `ec113a50` (`docs(distribute): mention Smart App Control in Windows signing guide (#4192)`).
- Vérifié par : `git -C tauri-docs rev-parse HEAD` → `ec113a503f1c195e3ccfda705f3f5cfe608093bd`.
- Périmètre : locale EN canonique = `tauri-docs/src/content/docs/**` hors traductions (`de es fr ja zh-cn…`), hors `blog/`, hors dossiers d'images. Les pages générées au build (`reference/config`, `reference/acl/*`, `reference/javascript/**`, `reference/cli` résolu) sont traitées en §5 car absentes de l'arbre local (submodules non initialisés).
- Méthode (skill `research`, faits filesystem uniquement) : `os.walk` + frontmatter `title:`, `wc` octets/mots, `astro.config.mjs` (sidebar topics), `llms-txt.config.mjs` (sections), `packages/*/build.ts` (références générées), `.gitmodules` + `submodule status`.
- Statut : cartographie **brute et non tranchée**. Le découpage final est au ticket #3.

## 1. Arborescence canonique (EN)

```
src/content/docs/
├── index.mdx, 404.md, rss.mdx                    (racine, 3)
├── _fragments/cta.mdx                            (fragment, 1)
├── start/ (15) : index, prerequisites, create-project, project-structure,
│                frontend/{index, vite, nextjs, nuxt, sveltekit, qwik, leptos, trunk},
│                migrate/{index, from-tauri-1, from-tauri-2-beta}
├── concept/ (7) : index, architecture, process-model, size,
│                  Inter-Process Communication/{index, brownfield, isolation}
├── security/ (11) : index, capabilities, permissions, scope, lifecycle,
│                     asset-protocol, csp, http-headers, ecosystem,
│                     runtime-authority, future
├── develop/ (25) : index, calling-rust, calling-frontend, configuration-files,
│                    state-management, resources, sidecar, updating-dependencies, icons,
│                    Debug/{index, vscode, neovim, rustrover, crabnebula-devtools, linux-graphics},
│                    Plugins/{index, develop-mobile},
│                    Tests/{index, mocking, WebDriver/{index, manual-setup, ci, Example/{selenium, webdriverio}}},
│                    _sections/frontend-listen.mdx (fragment inclus)
├── distribute/ (21) : index, windows-installer, dmg, macos-application-bundle,
│                      debian, rpm, appimage, aur, flatpak, snapcraft,
│                      app-store, microsoft-store, google-play, crabnebula-cloud,
│                      Pipelines/{github, crabnebula-cloud},
│                      Sign/{windows, macos, linux, android, ios}
├── learn/ (11) : index, window-customization, window-menu, system-tray, splashscreen,
│                 sidecar-nodejs, mobile-file-associations, mobile-multiwindow,
│                 Security/{using-plugin-permissions, writing-plugin-permissions,
│                           capabilities-for-windows-and-platforms}
├── plugin/ (31) : index + 30 fiches (voir §4)
├── reference/ (4 fichiers sources) : _cli.mdx, _cli_ios.mdx (partiels de template),
│                                     environment-variables.mdx, webview-versions.md
│                                     (+ acl/.gitkeep ; config/acl/js/cli générés au build, §5)
├── about/ (5) : index, philosophy, governance, trademark, book
└── contribute/index.mdx (1)
```

Sidebar officielle (`astro.config.mjs`, topics `Guides` + `References`) : Quick Start → Core Concepts → Security → Develop → Distribute → Learn → Plugins → About ; References → CLI, Security(acl), Configuration, Env Vars, Webview Versions, JavaScript, Rust (docs.rs externe). `llms-txt.config.mjs` confirme les 8 sections guides : `start concept security develop distribute learn plugin about`.

## 2. Comptes par grand domaine

| Domaine sidebar | Pages | ~Mots (brut regex `\S+`, frontmatter inclus) |
|---|---|---|
| (racine : index, 404, rss) | 3 | ~341 |
| _fragments (cta) | 1 | ~105 |
| about | 5 | ~2 650 |
| concept | 7 | ~4 246 |
| contribute | 1 | ~247 |
| develop (dont Debug 6, Plugins 2, Tests 6, _sections 1) | 25 | ~24 851 |
| distribute (dont Pipelines 2, Sign 5) | 21 | ~22 157 |
| learn (dont Security 3) | 11 | ~10 852 |
| plugin (index + 30 fiches) | 31 | ~23 728 |
| reference (sources locales : _cli, _cli_ios, env-vars, webview-versions) | 4 | ~3 754 |
| security | 11 | ~7 241 |
| start (dont frontend 8, migrate 3) | 15 | ~10 480 |
| **TOTAL local** | **135** | **~950 078 octets** |

Plus grosses pages (>15 Ko) : `start/migrate/from-tauri-1.mdx` (37,6 Ko), `distribute/windows-installer.mdx` (28,2 Ko), `plugin/updater.mdx` (27,1 Ko), `plugin/file-system.mdx` (23,8 Ko), `develop/calling-rust.mdx` (21,5 Ko), `develop/Plugins/develop-mobile.mdx` (19,2 Ko), `develop/Plugins/index.mdx` (19,3 Ko), `distribute/rpm.mdx` (18,7 Ko), `learn/window-menu.mdx` (17,7 Ko), `distribute/Sign/windows.mdx` (17,3 Ko), `plugin/deep-linking.mdx` (15,5 Ko).

## 3. Cartographie brute en domaines candidats (non contraignante, ticket #3 tranche)

| Code | Domaine candidat | Couverture indicative |
|---|---|---|
| A | demarrage-projet | `start/**` (15 p.) : install, prerequisites, create-project, structure, 8 frontends, migrate v1/beta |
| B | concepts-coeur | `concept/**` (7 p.) : architecture, process-model, IPC (index/brownfield/isolation), size |
| C | securite-capabilities | `security/**` (11 p.) + `learn/Security/**` (3 p.) : capabilities, permissions, scopes, lifecycle, CSP, headers, asset-protocol |
| D | bridge-rust-frontend | `develop/calling-rust.mdx`, `calling-frontend.mdx`, `_sections/frontend-listen.mdx`, `state-management.mdx`, `resources.mdx`, `sidecar.mdx`, `configuration-files.mdx`, `icons.mdx`, `develop/index.mdx` |
| E | qualite-dev | `develop/Debug/**` (6 p.), `develop/Tests/**` (6 p.), `updating-dependencies.mdx` |
| F | creation-plugins | `develop/Plugins/index.mdx`, `develop/Plugins/develop-mobile.mdx` |
| G | distribution-packaging | `distribute/**` (21 p.) : 14 cibles/formats/stores + `Sign/**` (5 p.) + `Pipelines/**` (2 p.) |
| H | recettes-ui-fenetres | `learn/window-customization.mdx`, `window-menu.mdx`, `system-tray.mdx`, `splashscreen.mdx`, `mobile-multiwindow.mdx`, `mobile-file-associations.mdx`, `sidecar-nodejs.mdx` |
| I | catalogue-plugins | `plugin/**` (31 p.) : index + 30 fiches dont `updater` (27 Ko), `file-system` (23,8 Ko), `deep-linking`, `sql`, `http-client`, `shell`, `store`, `dialog`, `notification`, etc. |
| J | reference-cli-env | `reference/_cli.mdx` + `_cli_ios.mdx` (templates, `$LIST_OF_COMMANDS`), `reference/environment-variables.mdx`, `reference/webview-versions.md` |
| K | reference-config-acl (généré, §5) | `reference/config.md`, `reference/acl/{capability, permission, scope, core-permissions}.md` — produits par `packages/config-generator/build.ts`, absents localement |
| L | reference-js-api (généré, §5) | core `@tauri-apps/api` (`packages/tauri`, branch dev) + 27 guest-js plugins (`packages/plugins-workspace`, branch v2) — produits par `packages/js-api-generator/build.ts`, absents localement |
| M | reference-rust-api (externe) | `https://docs.rs/tauri/~2/` linké depuis la sidebar, pas de source locale |
| N | meta-hors-perimetre-probable | `about/**` (5 p.), `contribute/index.mdx`, racine (`index`, `404`, `rss`), `_fragments/cta.mdx` |

## 4. Tableau traçabilité `doc-path → domaine candidat`

Chemins relatifs à `tauri-docs/src/content/docs/`. Titres = frontmatter `title:` local.

| doc-path | titre | domaine candidat |
|---|---|---|
| index.mdx | Tauri 2.0 | N |
| 404.md | 404 | N |
| rss.mdx | Tauri RSS Feeds | N |
| _fragments/cta.mdx | Create Tauri app | N |
| about/index.mdx | About Tauri | N |
| about/philosophy.md | Tauri Philosophy | N |
| about/governance.md | Tauri Governance | N |
| about/trademark.md | Trademark Guidelines | N |
| about/book.md | The Tauri Book | N |
| contribute/index.mdx | Contribute | N |
| start/index.mdx | What is Tauri? | A |
| start/prerequisites.mdx | Prerequisites | A |
| start/create-project.mdx | Create a Project | A |
| start/project-structure.mdx | Project Structure | A |
| start/frontend/index.mdx | Frontend Configuration | A |
| start/frontend/vite.mdx | Vite | A |
| start/frontend/nextjs.mdx | Next.js | A |
| start/frontend/nuxt.mdx | Nuxt | A |
| start/frontend/sveltekit.mdx | SvelteKit | A |
| start/frontend/qwik.mdx | Qwik | A |
| start/frontend/leptos.mdx | Leptos | A |
| start/frontend/trunk.mdx | Trunk | A |
| start/migrate/index.mdx | Upgrade & Migrate | A |
| start/migrate/from-tauri-1.mdx | Upgrade from Tauri 1.0 | A |
| start/migrate/from-tauri-2-beta.mdx | Upgrade from Tauri 2.0 Beta | A |
| concept/index.mdx | Core Concepts | B |
| concept/architecture.mdx | Tauri Architecture | B |
| concept/process-model.md | Process Model | B |
| concept/size.mdx | App Size | B |
| concept/Inter-Process Communication/index.mdx | Inter-Process Communication | B |
| concept/Inter-Process Communication/brownfield.md | Brownfield Pattern | B |
| concept/Inter-Process Communication/isolation.md | Isolation Pattern | B |
| security/index.mdx | Security | C |
| security/capabilities.mdx | Capabilities | C |
| security/permissions.mdx | Permissions | C |
| security/scope.mdx | Command Scopes | C |
| security/lifecycle.mdx | Application Lifecycle Threats | C |
| security/asset-protocol.mdx | Asset protocol scope | C |
| security/csp.mdx | Content Security Policy (CSP) | C |
| security/http-headers.mdx | HTTP Headers | C |
| security/ecosystem.mdx | Tauri Ecosystem Security | C |
| security/runtime-authority.mdx | Runtime Authority | C |
| security/future.mdx | Future Work | C |
| learn/Security/using-plugin-permissions.mdx | Using Plugin Permissions | C |
| learn/Security/writing-plugin-permissions.mdx | Writing Plugin Permissions | C |
| learn/Security/capabilities-for-windows-and-platforms.mdx | Capabilities for Different Windows and Platforms | C |
| develop/index.mdx | Develop | D |
| develop/calling-rust.mdx | Calling Rust from the Frontend | D |
| develop/calling-frontend.mdx | Calling the Frontend from Rust | D |
| develop/_sections/frontend-listen.mdx | Calling the Frontend from Rust | D |
| develop/state-management.mdx | State Management | D |
| develop/resources.mdx | Embedding Additional Files | D |
| develop/sidecar.mdx | Embedding External Binaries | D |
| develop/configuration-files.mdx | Configuration Files | D |
| develop/icons.mdx | App Icons | D |
| develop/updating-dependencies.mdx | Updating Dependencies | E |
| develop/Debug/index.mdx | Debug | E |
| develop/Debug/vscode.mdx | Debug in VS Code | E |
| develop/Debug/neovim.mdx | Debug in Neovim | E |
| develop/Debug/rustrover.mdx | Debug in JetBrains IDEs | E |
| develop/Debug/crabnebula-devtools.mdx | CrabNebula DevTools | E |
| develop/Debug/linux-graphics.md | Linux Graphics Issues | E |
| develop/Tests/index.mdx | Tests | E |
| develop/Tests/mocking.mdx | Mock Tauri APIs | E |
| develop/Tests/WebDriver/index.mdx | WebDriver | E |
| develop/Tests/WebDriver/manual-setup.mdx | Manual setup | E |
| develop/Tests/WebDriver/ci.md | Continuous Integration | E |
| develop/Tests/WebDriver/Example/selenium.mdx | Selenium | E |
| develop/Tests/WebDriver/Example/webdriverio.mdx | WebdriverIO | E |
| develop/Plugins/index.mdx | Plugin Development | F |
| develop/Plugins/develop-mobile.mdx | Mobile Plugin Development | F |
| distribute/index.mdx | Distribute | G |
| distribute/windows-installer.mdx | Windows Installer | G |
| distribute/dmg.mdx | DMG | G |
| distribute/macos-application-bundle.mdx | macOS Application Bundle | G |
| distribute/debian.mdx | Debian | G |
| distribute/rpm.mdx | RPM | G |
| distribute/appimage.mdx | AppImage | G |
| distribute/aur.mdx | AUR | G |
| distribute/flatpak.mdx | Flathub | G |
| distribute/snapcraft.mdx | Snapcraft | G |
| distribute/app-store.mdx | App Store | G |
| distribute/microsoft-store.mdx | Microsoft Store | G |
| distribute/google-play.mdx | Google Play | G |
| distribute/crabnebula-cloud.mdx | Distributing with CrabNebula Cloud | G |
| distribute/Pipelines/github.mdx | GitHub | G |
| distribute/Pipelines/crabnebula-cloud.mdx | CrabNebula Cloud | G |
| distribute/Sign/windows.mdx | Windows Code Signing | G |
| distribute/Sign/macos.mdx | macOS Code Signing | G |
| distribute/Sign/linux.mdx | Linux Code Signing | G |
| distribute/Sign/android.mdx | Android Code Signing | G |
| distribute/Sign/ios.mdx | iOS Code Signing | G |
| learn/index.mdx | Learn | H |
| learn/window-customization.mdx | Window Customization | H |
| learn/window-menu.mdx | Window Menu | H |
| learn/system-tray.mdx | System Tray | H |
| learn/splashscreen.mdx | Splashscreen | H |
| learn/mobile-multiwindow.mdx | Multi-Window on Mobile | H |
| learn/mobile-file-associations.mdx | File Associations on Mobile | H |
| learn/sidecar-nodejs.mdx | Node.js as a sidecar | H |
| plugin/index.mdx | Features & Recipes | I |
| plugin/autostart.mdx | Autostart | I |
| plugin/barcode-scanner.mdx | Barcode Scanner | I |
| plugin/biometric.mdx | Biometric | I |
| plugin/cli.mdx | Command Line Interface (CLI) | I |
| plugin/clipboard.mdx | Clipboard | I |
| plugin/deep-linking.mdx | Deep Linking | I |
| plugin/dialog.mdx | Dialog | I |
| plugin/file-system.mdx | File System | I |
| plugin/geolocation.mdx | Geolocation | I |
| plugin/global-shortcut.mdx | Global Shortcut | I |
| plugin/haptics.mdx | Haptics | I |
| plugin/http-client.mdx | HTTP Client | I |
| plugin/localhost.mdx | Localhost | I |
| plugin/logging.mdx | Logging | I |
| plugin/nfc.mdx | NFC | I |
| plugin/notification.mdx | Notifications | I |
| plugin/opener.mdx | Opener | I |
| plugin/os-info.mdx | OS Information | I |
| plugin/persisted-scope.mdx | Persisted Scope | I |
| plugin/positioner.mdx | Positioner | I |
| plugin/process.mdx | Process | I |
| plugin/shell.mdx | Shell | I |
| plugin/single-instance.mdx | Single Instance | I |
| plugin/sql.mdx | SQL | I |
| plugin/store.mdx | Store | I |
| plugin/stronghold.mdx | Stronghold | I |
| plugin/updater.mdx | Updater | I |
| plugin/upload.mdx | Upload | I |
| plugin/websocket.mdx | Websocket | I |
| plugin/window-state.mdx | Window State | I |
| reference/_cli.mdx | Command Line Interface (template `$LIST_OF_COMMANDS`) | J |
| reference/_cli_ios.mdx | (sans titre, partiel iOS) | J |
| reference/environment-variables.mdx | Environment Variables | J |
| reference/webview-versions.md | Webview Versions | J |
| reference/config.md (généré, absent localement) | — | K |
| reference/acl/capability.md (généré) | — | K |
| reference/acl/permission.md (généré) | — | K |
| reference/acl/scope.md (généré) | — | K |
| reference/acl/core-permissions.md (généré) | — | K |
| reference/javascript/** (généré : core + 27 plugins) | — | L |
| Rust API docs.rs (externe, linké) | — | M |

## 5. Références générées / externes (comptées à part, non dans les 135)

- `packages/config-generator/build.ts` → `reference/config.md` + `reference/acl/{capability, permission, scope, core-permissions}.md` (5 pages générées depuis le schéma ; seule trace locale = `reference/acl/.gitkeep`).
- `packages/js-api-generator/build.ts` → `reference/javascript/` : core (`packages/tauri/packages/api/src/index.ts`) + 27 guest-js plugins (`autostart barrel: autostart, barcode-scanner, biometric, cli, clipboard-manager, deep-link, dialog, fs, geolocation, global-shortcut, haptics, http, log, nfc, notification, opener, os, positioner, process, shell, sql, store, stronghold, updater, upload, websocket, window-state`) ; `packages/cli-generator/build.ts` résout `$LIST_OF_COMMANDS` dans `reference/_cli.mdx`.
- Submodules `packages/tauri`, `packages/plugins-workspace`, `packages/awesome-tauri` : **non initialisés localement** (`git submodule status` → `-` préfixe), donc les sources des références générées ne sont pas inventoriables 1:1 ici — à régénérer ou à wersji avant la spec (ticket #3).
- Rust API : uniquement un lien sidebar `https://docs.rs/tauri/~2/`, aucune source locale.

## 6. Zones floues renvoyées en fog (ticket #3 tranche, rien n'est décidé ici)

1. `security/**` vs `learn/Security/**` vs `reference/acl/**` vs permissions par fiche `plugin/*` (`#default-permission`, `#permission-table`) : 4 lieux parlent de permissions/capabilities, recouvrement à découper.
2. `learn/**` vs `develop/**` vs `plugin/**` : recettes (`window-menu`, `system-tray`, `sidecar-nodejs`) vs guides vs fiches plugins — frontière floue.
3. Mobile éclaté : `develop/Plugins/develop-mobile.mdx` + `learn/mobile-*.mdx` + `distribute/Sign/{android,ios}.mdx` + `distribute/google-play.mdx` + `reference/_cli_ios.mdx` — regrouper ou laisser dispersé ?
4. `plugin/updater.mdx` (27 Ko) vs `distribute/Pipelines/**` + stores : l'updater est-il distribution ou plugin ?
5. `plugin/cli.mdx` (usage du plugin CLI dans l'app) vs `reference/_cli.mdx` (CLI dev `tauri-cli`) : homonymes à désambiguïser.
6. Granularité `distribute/Sign/**` (5 p.) + `distribute/Pipelines/**` (2 p.) : 1 skill distribution monolithe ou skills par OS ?
7. `develop/sidecar.mdx` vs `learn/sidecar-nodejs.mdx` : doublon apparent binaire externe vs Node.js.
8. `develop/_sections/frontend-listen.mdx` + `develop/Debug/*` (outils externes : VS Code, Neovim, RustRover, CrabNebula, Linux graphics) : fragments/edges, périmètre skill incertain.
9. Références générées (K/L, §5) : périmètre exact (core JS = N modules depuis `packages/api/src/index.ts`) non vérifiable sans init des submodules — fog outillage.
10. `about/**`, `contribute`, racine, `_fragments`, `start/migrate/*`, `develop/updating-dependencies.mdx` : dans ou hors pack ? `migrate/from-tauri-1.mdx` (37,6 Ko, la plus grosse page) mérite-t-elle un skill à part ?
11. `reference/webview-versions.md` (22 Ko, matrice de compatibilité générée via `packages/compatibility-table`) : référence ou distribution ?
12. Traductions (`ja/**` quasi complet, `es/fr/zh-cn` partiels) : ignorées (EN canonique), mais la spec devra figer la règle source-de-vérité i18n.
