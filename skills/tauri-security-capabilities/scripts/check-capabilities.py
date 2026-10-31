#!/usr/bin/env python3
"""Check déterministe d'une capability JSON (seam basse pilote).

Repris de l'étalon prototype throwaway (branch prototype/gabarit-skill,
prototypes/gabarit-tauri-security/scripts/check-capabilities.py), durci :
- valide identifier, cibles windows/webviews, forme des permissions
- cas OK et KO testés, aucune permission inventée.

Usage:
  python3 scripts/check-capabilities.py examples/default-capability.json
"""
import json
import re
import sys

PERM_RE = re.compile(
    r"^(?:[a-z0-9-]+:[a-z0-9-*]+(?::[a-z0-9-*]+)?|[a-z0-9]+-[a-z0-9-]+)$"
)


def main(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    errors = []
    if not data.get("identifier"):
        errors.append("missing 'identifier'")
    if not data.get("windows") and not data.get("webviews"):
        errors.append("missing 'windows' or 'webviews'")
    perms = data.get("permissions")
    if not isinstance(perms, list) or not perms:
        errors.append("missing non-empty 'permissions' list")
    else:
        for p in perms:
            if not isinstance(p, str) or not PERM_RE.match(p):
                errors.append(
                    f"bad permission format: {p!r} (attendu plugin:scope:cle, ex core:window:allow-set-title)"
                )
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"OK {path}: identifier={data.get('identifier')}, permissions={len(perms)}")
    for p in perms:
        print(f" - {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "examples/default-capability.json"))
