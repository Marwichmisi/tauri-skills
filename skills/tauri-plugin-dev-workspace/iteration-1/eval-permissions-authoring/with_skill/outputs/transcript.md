# Transcript — eval permissions authoring (with_skill)

## Steps

1. Lu `skills/tauri-plugin-dev/SKILL.md` (workflow + tableau routage + frontières + règle anti-drift).
2. Routé intention « Écrire permissions (allow/deny, scope, set, default, build.rs autogen) » vers `references/permissions.md`, lu en entier (sources : `tauri-docs/src/content/docs/develop/Plugins/index.mdx`, commit `ec113a50`, EN canonique).
3. Lu `references/plugin-basics.md` § Identifier Rules (rappel `[a-z0-9-]`, snake_case commandes) pour « sans identifiant inventé ».
4. Lu les exemples : `permission-allow-start-server.toml`, `permission-scope-spawn-node.toml`, `permission-set-websocket.toml`, `permission-default.toml`, `build-rs-autogen.rs`.
5. Lu `scripts/check-plugin-dev.py` (modes `--permission` / `--identifier`) pour connaître les règles de validation.
6. Écrit les artefacts dans `outputs/` :
   - `permissions-upload.toml` (allow-upload/deny-upload, `commands.allow`/`commands.deny = ["upload"]`, transposition fidèle de l'exemple `start_server` → `upload`)
   - `permissions-scope-spawn-node.toml` (allow-spawn-node, `[[permission.scope.allow]] binary = "node"`, identique à l'exemple)
   - `permissions-set-websocket.toml` (set allow-websocket → allow-connect + allow-send, identique à l'exemple)
   - `permissions-default.toml` (default → allow-request, identique à l'exemple)
   - `build.rs` (`COMMANDS = &["upload"]` + `global_scope_schema(schemars::schema_for!(scope::Entry))`, fusion autogen + schema de `references/permissions.md`)
   - `scope.rs` (`Entry { binary: String }` + `schemars::JsonSchema`)
7. Validé avec `scripts/check-plugin-dev.py --permission` (4 fichiers) + `--identifier` (my-plugin + 8 identifiants) — tous OK.
8. Rédigé `answer.md` (pointeurs source fichier + commit + titre + note frontière) + ce `transcript.md`.

Aucun identifiant inventé : seuls `my-plugin`, `upload`, `allow-upload`, `deny-upload`, `allow-spawn-node`, `allow-websocket`, `allow-connect`, `allow-send`, `allow-request`, `default`, `node` (binaire scope) sont utilisés — tous issus de la doc locale ou de la consigne.

## Checks with outputs

```
$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --permission .../outputs/permissions-upload.toml
OK .../outputs/permissions-upload.toml: permissions fidèles (2 permission(s), 0 set(s))
EXIT:0

$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --permission .../outputs/permissions-scope-spawn-node.toml
OK .../outputs/permissions-scope-spawn-node.toml: permissions fidèles (1 permission(s), 0 set(s))
EXIT:0

$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --permission .../outputs/permissions-set-websocket.toml
OK .../outputs/permissions-set-websocket.toml: permissions fidèles (0 permission(s), 1 set(s))
EXIT:0

$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --permission .../outputs/permissions-default.toml
OK .../outputs/permissions-default.toml: permissions fidèles (0 permission(s), 0 set(s), default)
EXIT:0

$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --identifier my-plugin
OK identifier 'my-plugin' valide (develop/Plugins/index.mdx)
EXIT:0

$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --identifier allow-upload
OK identifier 'allow-upload' valide (develop/Plugins/index.mdx)
EXIT:0

$ for id in deny-upload allow-spawn-node allow-websocket allow-connect allow-send allow-request default upload; do python3 .../check-plugin-dev.py --identifier "$id"; done
OK identifier 'deny-upload' valide (develop/Plugins/index.mdx)
OK identifier 'allow-spawn-node' valide (develop/Plugins/index.mdx)
OK identifier 'allow-websocket' valide (develop/Plugins/index.mdx)
OK identifier 'allow-connect' valide (develop/Plugins/index.mdx)
OK identifier 'allow-send' valide (develop/Plugins/index.mdx)
OK identifier 'allow-request' valide (develop/Plugins/index.mdx)
OK identifier 'default' valide (develop/Plugins/index.mdx)
OK identifier 'upload' valide (develop/Plugins/index.mdx)

$ diff examples/permission-scope-spawn-node.toml outputs/permissions-scope-spawn-node.toml
scope identical to example
$ diff examples/permission-set-websocket.toml outputs/permissions-set-websocket.toml
set identical to example
$ diff examples/permission-default.toml outputs/permissions-default.toml
default identical to example
```

## Frontier declaration

Capability côté app (`capabilities/*.json`) → skill `tauri-security-capabilities`, seule autorité. Ce transcript et `answer.md` restent côté auteur (`permissions/*.toml` + `build.rs`).
