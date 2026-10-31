#!/usr/bin/env python3
"""PROTOTYPE THROWAWAY — check déterministe d'une capability JSON.

Usage:
  python3 scripts/check-capabilities.py examples/default-capability.json

Ne fait que valider la forme vue dans la doc (identifier, cible windows/webviews,
permissions type scope). Aucune logique métier.
"""
import json
import re
import sys

PERM_RE = re.compile(r"^[a-z0-9-]+:[a-z0-9-]+:(default|allow-[a-z0-9-]+|deny-[a-z0-9-]+|[a-z0-9-*]+)$")


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
                errors.append(f"bad permission format: {p!r} (attendu plugin:scope:cle, ex core:window:allow-set-title)")
    if errors:
        print("FAIL", path)
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"OK {path}: identifier={data['identifier']}, permissions={len(perms)}")
    for p in perms:
        print(f" - {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "examples/default-capability.json"))
