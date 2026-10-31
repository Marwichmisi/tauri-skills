# Resources — extrait doc

Source : `tauri-docs/src/content/docs/develop/resources.mdx`, commit `ec113a50`, titre frontmatter `Embedding Additional Files`.

> You may need to include additional files in your application bundle that aren't part of your frontend (your `frontendDist`) directly or which are too big to be inlined into the binary. We call these files `resources`.

## Declarer (meme fichier)

Liste (syntaxe) — voir `examples/tauri.conf.resources.json` :

```json
{ "bundle": { "resources": ["./path/to/some-file.txt", "/absolute/path/to/textfile.txt", "../relative/path/to/jsonfile.json", "some-folder/", "resources/**/*.md"] } }
```

Explication (meme fichier, onglet Explanation) : `./x` -> `$RESOURCE/x` ; `/abs` -> `$RESOURCE/_root_/abs` ; `../rel` -> `$RESOURCE/_up_/rel` ; `dir/` = `dir/**/*` (recursif, structure preservee) ; globs `resources/**/*.md` preserves.

Map (ciblage fin) :

```json
{ "bundle": { "resources": { "/absolute/path/to/textfile.txt": "resources/textfile.txt", "relative/path/to/jsonfile.json": "resources/jsonfile.json", "resources/": "", "docs/**/*md": "website-docs/" } } }
```

> When using glob patterns [en map], all the matching files will be placed to the target directory without preserving the original file structures.

Source path syntax (meme fichier) : `dir/file.txt` (fichier) ; `dir/` (recursif, preserve) ; `dir/*` (non-recursif) ; `dir/**` et `dir/**/**` (erreur, `**` seul ne matche que des dossiers) ; `dir/**/*` (recursif fichiers).

## Resoudre (meme fichier)

> To resolve the path for a resource file, instead of manually calculating the path, use the following APIs.

Rust : `app.path().resolve("lang/de.json", BaseDirectory::Resource)`, en commande : `handle.path().resolve(...)`. JS : `resolveResource('lang/de.json')` (`@tauri-apps/api/path`). Meme regle `../` -> `_up_`, racine -> `_root_` qu'en config.

Android : ressources en assets APK, URI `asset://localhost/` via plugin `fs` (`FsExt::fs`) ; sinon copier vers FS reel via plugin `fs`.

## Lire (meme fichier)

Exemple i18n `lang/de.json` + `lang/*` : Rust `std::fs::read_to_string(&resource_path)` (ou `app.fs().read_to_string` sur Android) + `serde_json` ; JS : `invoke('hello')` ou plugin `fs` + `fs:allow-read-text-file` + `fs:allow-resource-read-recursive`.

## Permissions (meme fichier, renvoi securite)

> Since we replace `../` to `_up_` ... use `$RESOURCE/**/*` to allow recursive access. Ex `../relative/...` + `fs:scope allow ["$RESOURCE/**/*"] deny ["$RESOURCE/secret.txt"]`, ou `opener:allow-open-path allow [{ path: "$RESOURCE/**/*" }]`.

Regle pack : toute question de scope/permission remonte a `tauri-security-capabilities` (`references/scopes.md`, `references/permissions.md`). Ici : chemins + APIs seulement.

Lien `docs.rs` : `resource_dir`, `PathResolver`, `App`, `AppHandle`. Fiches plugins : `fs`, `opener` (voir catalogue).
