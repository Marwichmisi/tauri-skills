#!/usr/bin/env python3
"""Check déterministe config/CLI/env Tauri v2 (seam basse tauri-config-cli-reference).

Valide le comportement externe de l'agent sur des artefacts reproductibles
fidèles à la doc locale commit ec113a50 (EN canonique seule), sans inventer
de schéma ni de commande. Ne prouve PAS à lui seul la couverture doc : les
pointeurs source se vérifient dans la réponse.

Règles issues de tauri-docs (domaine tauri-config-cli-reference) :
- config : JSON valide ; pas de `cli` racine (doit être `plugins.cli`,
  plugin/cli.mdx Base Configuration) ; `plugins.cli` exige `description`
  non-vide, `args[]` exige `name` (clés doc seules : name/short/description/
  takesValue/multiple/possibleValues/index), `subcommands{}` même forme ;
  `$schema` éventuel contient `gen/schemas` (security/capabilities.mdx).
  Schéma complet généré `reference/config.md` absent au commit (voir
  reference/.gitignore + packages/config-generator/build.ts) : ce check ne
  valide que la forme `plugins.cli` documentée, le reste renvoie au schéma.
- cli : distingue CLI dev (`<pm> tauri <cmd>` : dev/build/bundle/icon/init/
  migrate/add/android/ios/...) de l'usage in-app (`getMatches`, `CliExt`,
  `tauri_plugin_cli`, `plugins.cli`, `cli:default`) ; `tauri cli` comme
  commande dev est inexistante et rejetée (homonyme : `tauri add cli`
  installe le plugin, `plugins.cli` le configure).
- env : noms seuls documentés dans reference/environment-variables.mdx
  (+ TAURI_DEV_HOST / TAURI_DEV_ROOT_CERTIFICATE_PATH documentés dans
  reference/_cli_ios.mdx) ; priorité flag sur variable (même fichier).

Usage (un mode par appel) :
  python3 scripts/check-config-cli.py --config examples/tauri.conf.cli.json
  python3 scripts/check-config-cli.py --cli examples/cli-commands.sh
  python3 scripts/check-config-cli.py --env examples/env.sh
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ARG_ALLOWED = {
    "name",
    "short",
    "description",
    "takesValue",
    "multiple",
    "possibleValues",
    "index",
}
CLI_ALLOWED = {"description", "args", "subcommands"}

DEV_CMDS = {
    "dev",
    "build",
    "bundle",
    "icon",
    "init",
    "migrate",
    "add",
    "android",
    "ios",
    "signer",
    "plugin",
    "help",
}
PM_TAURI_RE = re.compile(
    r"(?:npm run|yarn|pnpm|deno task|bun|cargo)\s+tauri\s+([a-z-]+)"
)
TAURI_CLI_RE = re.compile(r"(?:^|\s)tauri\s+cli(?:\s|$)")
INAPP_PATTERNS = [
    re.compile(r"getMatches"),
    re.compile(r"CliExt"),
    re.compile(r"tauri_plugin_cli"),
    re.compile(r"plugins\.cli"),
    re.compile(r"cli:default"),
    re.compile(r"ArgData"),
]

ENV_ALLOWED = {
    "CI",
    "TAURI_CLI_CONFIG_DEPTH",
    "TAURI_CLI_PORT",
    "TAURI_CLI_WATCHER_IGNORE_FILENAME",
    "TAURI_CLI_NO_DEV_SERVER_WAIT",
    "TAURI_LINUX_AYATANA_APPINDICATOR",
    "TAURI_BUNDLER_WIX_FIPS_COMPLIANT",
    "TAURI_BUNDLER_TOOLS_GITHUB_MIRROR",
    "TAURI_BUNDLER_TOOLS_GITHUB_MIRROR_TEMPLATE",
    "TAURI_SKIP_SIDECAR_SIGNATURE_CHECK",
    "TAURI_SIGNING_PRIVATE_KEY",
    "TAURI_SIGNING_PRIVATE_KEY_PASSWORD",
    "TAURI_SIGNING_RPM_KEY",
    "TAURI_SIGNING_RPM_KEY_PASSPHRASE",
    "TAURI_WINDOWS_SIGNTOOL_PATH",
    "APPLE_CERTIFICATE",
    "APPLE_CERTIFICATE_PASSWORD",
    "APPLE_ID",
    "APPLE_PASSWORD",
    "APPLE_TEAM_ID",
    "APPLE_API_KEY",
    "API_PRIVATE_KEYS_DIR",
    "APPLE_API_ISSUER",
    "APPLE_API_KEY_PATH",
    "APPLE_SIGNING_IDENTITY",
    "APPLE_PROVIDER_SHORT_NAME",
    "APPLE_DEVELOPMENT_TEAM",
    "TAURI_WEBVIEW_AUTOMATION",
    "TAURI_ANDROID_PROJECT_PATH",
    "TAURI_IOS_PROJECT_PATH",
    "TAURI_ENV_DEBUG",
    "TAURI_ENV_TARGET_TRIPLE",
    "TAURI_ENV_ARCH",
    "TAURI_ENV_PLATFORM",
    "TAURI_ENV_PLATFORM_VERSION",
    "TAURI_ENV_FAMILY",
    # Documentés dans reference/_cli_ios.mdx (domaine) et start/frontend/vite.mdx (frère) :
    "TAURI_DEV_HOST",
    "TAURI_DEV_ROOT_CERTIFICATE_PATH",
}
ENV_LINE_RE = re.compile(
    r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:=\s*(.*))?$"
)


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def check_args(args, where: str, errors: list[str]) -> None:
    if not isinstance(args, list):
        errors.append(f"{where}: 'args' doit être une liste")
        return
    for i, a in enumerate(args):
        loc = f"{where}.args[{i}]"
        if not isinstance(a, dict):
            errors.append(f"{loc}: entrée doit être un objet")
            continue
        if not a.get("name") or not isinstance(a.get("name"), str):
            errors.append(f"{loc}: 'name' (string non-vide) requis")
        for k in a:
            if k not in ARG_ALLOWED:
                errors.append(
                    f"{loc}: clé '{k}' non documentée "
                    f"(doc : {sorted(ARG_ALLOWED)})"
                )


def check_config(path: pathlib.Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return fail(f"{path}: JSON illisible ({e})")
    if not isinstance(data, dict):
        return fail(f"{path}: racine doit être un objet")
    errors: list[str] = []
    if "cli" in data:
        errors.append("clé 'cli' racine interdite : utiliser 'plugins.cli' (plugin/cli.mdx)")
    schema = data.get("$schema")
    if schema is not None and (
        not isinstance(schema, str) or "gen/schemas" not in schema
    ):
        errors.append("$schema doit contenir 'gen/schemas' (ex ../gen/schemas/desktop-schema.json)")
    plugins = data.get("plugins", {})
    if not isinstance(plugins, dict):
        errors.append("'plugins' doit être un objet")
        plugins = {}
    if "cli" in plugins:
        cli = plugins["cli"]
        if not isinstance(cli, dict):
            errors.append("'plugins.cli' doit être un objet")
        else:
            for k in cli:
                if k not in CLI_ALLOWED:
                    errors.append(
                        f"plugins.cli: clé '{k}' non documentée "
                        f"(doc : {sorted(CLI_ALLOWED)})"
                    )
            if not cli.get("description") or not isinstance(
                cli.get("description"), str
            ):
                errors.append("plugins.cli: 'description' (string non-vide) requise")
            if "args" in cli:
                check_args(cli["args"], "plugins.cli", errors)
            subs = cli.get("subcommands", {})
            if not isinstance(subs, dict):
                errors.append("plugins.cli: 'subcommands' doit être un objet")
            else:
                for name, sub in subs.items():
                    if not isinstance(sub, dict):
                        errors.append(
                            f"plugins.cli.subcommands.{name}: doit être un objet"
                        )
                        continue
                    for k in sub:
                        if k not in CLI_ALLOWED:
                            errors.append(
                                f"plugins.cli.subcommands.{name}: clé '{k}' "
                                f"non documentée (doc : {sorted(CLI_ALLOWED)})"
                            )
                    if "args" in sub:
                        check_args(
                            sub["args"],
                            f"plugins.cli.subcommands.{name}",
                            errors,
                        )
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    cli = plugins.get("cli")
    n_args = len(cli.get("args", [])) if isinstance(cli, dict) else 0
    print(f"OK {path}: JSON valide, plugins.cli conforme (args={n_args})")
    return 0


def check_cli(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    errors: list[str] = []
    if TAURI_CLI_RE.search(text):
        errors.append(
            "'tauri cli' n'est pas une commande dev (homonyme) : "
            "installer avec 'tauri add cli', configurer via 'plugins.cli'"
        )
    devs: list[str] = []
    for m in PM_TAURI_RE.finditer(text):
        cmd = m.group(1)
        if cmd.startswith("-"):
            continue
        if cmd not in DEV_CMDS:
            errors.append(
                f"commande dev '{cmd}' non documentée "
                f"(doc : {sorted(DEV_CMDS)} + ios init/dev/build/run)"
            )
        else:
            devs.append(cmd)
    inap = sorted({r.pattern for r in INAPP_PATTERNS if r.search(text)})
    if not devs and not inap:
        errors.append("aucun marqueur dev (<pm> tauri <cmd>) ni in-app (getMatches/CliExt) trouvé")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"OK {path}: dev={sorted(set(devs)) or '—'}, in-app={inap or '—'}")
    return 0


def check_env(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    errors: list[str] = []
    found: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        m = ENV_LINE_RE.match(line)
        if not m:
            continue
        key = m.group(1)
        if key in ("if", "then", "fi", "export", "echo"):
            continue
        if key not in ENV_ALLOWED:
            # Ignore les variables shell génériques du snippet (ex PATH/HOME) :
            if key in {"PATH", "HOME", "PWD"}:
                continue
            errors.append(f"ligne {lineno}: variable '{key}' non documentée")
        else:
            found.append(key)
    if not found and not errors:
        return fail(f"{path}: aucune variable documentée trouvée")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"OK {path}: variables={sorted(set(found))}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None)
    ap.add_argument("--cli", default=None)
    ap.add_argument("--env", default=None)
    args = ap.parse_args()
    if args.config:
        return check_config(pathlib.Path(args.config))
    if args.cli:
        return check_cli(pathlib.Path(args.cli))
    if args.env:
        return check_env(pathlib.Path(args.env))
    print("FAIL: fournir un mode : --config OU --cli OU --env")
    return 1


if __name__ == "__main__":
    sys.exit(main())
