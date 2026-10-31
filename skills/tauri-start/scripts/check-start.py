#!/usr/bin/env python3
"""Check déterministe de démarrage Tauri v2 (seam basse tauri-start).

Valide le comportement externe de l'agent sur le bloc `build` de
`tauri.conf.json` : frontendDist/devUrl/commandes fidèles à la doc locale,
sans inventer de valeurs. Ne prouve PAS à lui seul le mode statique :
`output:'export'` (Next), `ssr:false` + adapter static (Nuxt/SvelteKit/Qwik)
se vérifient dans `next.config.mjs` / `nuxt.config.ts` / `svelte.config.js` /
`+layout.ts`, rappelés en `references/frontend-meta.md` et exigés par les
expectations d'eval (contenu réponse), pas par ce script.

Règles issues de tauri-docs commit ec113a50 (EN canonique seule) :
- vite      : frontendDist ../dist,  devUrl :5173, beforeDev *dev, beforeBuild *build
- nextjs    : frontendDist ../out,   devUrl :3000, output export (rappelé, non vérifié ici)
- nuxt      : frontendDist ../dist,  devUrl :3000, beforeBuild *generate (ssr:false)
- sveltekit : frontendDist ../build, devUrl :5173, adapter-static + ssr:false (rappelé)
- qwik      : frontendDist ../dist,  devUrl :5173, static adapter (rappelé)
- leptos    : frontendDist ../dist,  devUrl :1420, trunk serve/build + withGlobalTauri:true
- trunk     : frontendDist ../dist,  devUrl :8080, trunk serve/build + withGlobalTauri:true

Usage :
  python3 scripts/check-start.py examples/tauri.conf.vite.json --frontend vite
  python3 scripts/check-start.py src-tauri/tauri.conf.json --project-root .
"""
import argparse
import json
import pathlib
import sys

EXPECTED = {
    "vite": {"frontendDist": "../dist", "devPort": "5173"},
    "nextjs": {"frontendDist": "../out", "devPort": "3000"},
    "nuxt": {"frontendDist": "../dist", "devPort": "3000", "buildMustContain": "generate"},
    "sveltekit": {"frontendDist": "../build", "devPort": "5173"},
    "qwik": {"frontendDist": "../dist", "devPort": "5173"},
    "leptos": {
        "frontendDist": "../dist",
        "devPort": "1420",
        "devMustContain": "trunk serve",
        "buildMustContain": "trunk build",
        "withGlobalTauri": True,
    },
    "trunk": {
        "frontendDist": "../dist",
        "devPort": "8080",
        "devMustContain": "trunk serve",
        "buildMustContain": "trunk build",
        "withGlobalTauri": True,
    },
}

REQUIRED_STRUCTURE = [
    "src-tauri/tauri.conf.json",
    "src-tauri/Cargo.toml",
    "src-tauri/build.rs",
    "src-tauri/src/main.rs",
    "src-tauri/src/lib.rs",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("conf", help="chemin tauri.conf.json à valider")
    ap.add_argument("--frontend", default=None, choices=sorted(EXPECTED),
                    help="frontend documenté à vérifier strictement")
    ap.add_argument("--project-root", default=None,
                    help="racine projet pour vérifier la structure src-tauri/")
    args = ap.parse_args()

    conf_path = pathlib.Path(args.conf)
    try:
        data = json.loads(conf_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAIL {conf_path}: JSON illisible ({e})")
        return 1

    build = data.get("build") or {}
    errors: list[str] = []

    frontend_dist = build.get("frontendDist", "")
    dev_url = build.get("devUrl", "")
    before_dev = build.get("beforeDevCommand", "")
    before_build = build.get("beforeBuildCommand", "")

    if not frontend_dist:
        errors.append("missing 'build.frontendDist' (ex ../dist, ../out, ../build selon frontend)")
    if not dev_url:
        errors.append("missing 'build.devUrl' (ex http://localhost:5173)")
    if not before_dev:
        errors.append("missing 'build.beforeDevCommand'")
    if not before_build:
        errors.append("missing 'build.beforeBuildCommand'")

    if args.frontend:
        exp = EXPECTED[args.frontend]
        if frontend_dist != exp["frontendDist"]:
            errors.append(
                f"bad frontendDist pour {args.frontend}: vu {frontend_dist!r}, "
                f"attendu {exp['frontendDist']!r} (doc start/frontend/{args.frontend}.mdx)"
            )
        if exp["devPort"] not in str(dev_url):
            errors.append(
                f"bad devUrl pour {args.frontend}: vu {dev_url!r}, "
                f"port {exp['devPort']} attendu (doc start/frontend/{args.frontend}.mdx)"
            )
        if "devMustContain" in exp and exp["devMustContain"] not in str(before_dev):
            errors.append(
                f"bad beforeDevCommand pour {args.frontend}: vu {before_dev!r}, "
                f"doit contenir {exp['devMustContain']!r}"
            )
        if "buildMustContain" in exp and exp["buildMustContain"] not in str(before_build):
            errors.append(
                f"bad beforeBuildCommand pour {args.frontend}: vu {before_build!r}, "
                f"doit contenir {exp['buildMustContain']!r} "
                f"(nuxt: generate, pas build — doc start/frontend/nuxt.mdx)"
            )
        if exp.get("withGlobalTauri"):
            if not (data.get("app") or {}).get("withGlobalTauri"):
                errors.append(
                    f"missing 'app.withGlobalTauri: true' pour {args.frontend} "
                    f"(doc start/frontend/{args.frontend}.mdx, wasm-bindgen via window.__TAURI__)"
                )
        # next.config.mjs (output:'export') hors périmètre tauri.conf.json :
        # vérifié par les expectations d'eval (contenu réponse), voir references/frontend-meta.md.
        if args.frontend == "nextjs" and frontend_dist == "../out":
            print(
                "note: output:'export' à vérifier dans next.config.mjs "
                "(voir references/frontend-meta.md), hors tauri.conf.json"
            )
    else:
        allowed = {"../dist", "../out", "../build"}
        if frontend_dist and frontend_dist not in allowed:
            errors.append(
                f"bad frontendDist: vu {frontend_dist!r}, attendu l'un de {sorted(allowed)} "
                f"(valeurs documentées start/frontend/*.mdx, aucune autre inventée)"
            )

    if args.project_root:
        root = pathlib.Path(args.project_root)
        for rel in REQUIRED_STRUCTURE:
            if not (root / rel).is_file():
                errors.append(f"structure manquante: {rel} (doc start/project-structure.mdx)")

    if errors:
        print(f"FAIL {conf_path}")
        for e in errors:
            print(f" - {e}")
        return 1

    label = args.frontend or "generic"
    print(f"OK {conf_path}: frontend={label}, frontendDist={frontend_dist}, devUrl={dev_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
