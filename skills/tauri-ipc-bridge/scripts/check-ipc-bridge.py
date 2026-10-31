#!/usr/bin/env python3
"""Check deterministe de l'echange Rust <-> frontend Tauri v2 (seam basse tauri-ipc-bridge)."""
import argparse
import json
import pathlib
import re
import sys

CMD_RE = re.compile(r"#\[tauri::command[^\]]*\]\s*(pub\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)")
HANDLER_RE = re.compile(r"(?:invoke_handler|generate_handler)!\s*\[([^\]]+)\]")
INVOKE_RE = re.compile(r"""invoke\s*\(\s*['"]([A-Za-z_][A-Za-z0-9_]*)['"]""")
EMIT_RUST_RE = re.compile(r"""\.emit(?:_to|_filter)?\s*\(\s*"([^"]+)"|\.emit(?:_to|_filter)?\s*\(\s*'([^']+)'""")
LISTEN_FRONT_RE = re.compile(r"""(?:listen|once|emit|emitTo)\s*\(\s*['"]([^'"]+)['"]""")
SIDECAR_RUST_RE = re.compile(r"""\.sidecar\s*\(\s*"([^"]+)"|\.sidecar\s*\(\s*'([^']+)'""")
SIDECAR_JS_RE = re.compile(r"""Command\.sidecar\s*\(\s*['"]([^'"]+)['"]""")
CHANNEL_RE = re.compile(r"(?:tauri::ipc::Channel|new\s+Channel)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rust", default=None)
    ap.add_argument("--frontend", default=None)
    ap.add_argument("--config", default=None)
    args = ap.parse_args()
    if not args.rust and not args.frontend and not args.config:
        print("FAIL: fournir --rust et/ou --frontend et/ou --config")
        return 1
    errors: list[str] = []
    info: list[str] = []
    rust_cmds: list[tuple[str, bool]] = []
    rust_handlers: list[str] = []
    rust_sidecars: list[str] = []
    rust_emits: list[str] = []
    front_invokes: list[str] = []
    front_events: list[str] = []
    front_sidecars: list[str] = []
    front_has_channel = False
    if args.rust:
        rp = pathlib.Path(args.rust)
        try:
            text = rp.read_text(encoding="utf-8")
        except Exception as e:
            print(f"FAIL {rp}: illisible ({e})")
            return 1
        for m in CMD_RE.finditer(text):
            rust_cmds.append((m.group(2), bool(m.group(1))))
        names = [n for n, _ in rust_cmds]
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            errors.append(f"command names must be unique (doublons: {', '.join(dupes)})")
        for m in HANDLER_RE.finditer(text):
            for tok in m.group(1).split(","):
                tok = tok.strip()
                if tok:
                    rust_handlers.append(tok.split("::")[-1].strip())
        if rust_cmds and not rust_handlers:
            errors.append("missing invoke_handler/generate_handler (enregistrer via tauri::generate_handler![...])")
        for name, _ in rust_cmds:
            if rust_handlers and name not in rust_handlers:
                errors.append(f"command '{name}' not registered in invoke_handler/generate_handler")
        if rp.name == "lib.rs":
            for name, is_pub in rust_cmds:
                if is_pub:
                    errors.append(f"pub fn '{name}' forbidden in lib.rs (commands in lib.rs cannot be marked as pub)")
        for m in SIDECAR_RUST_RE.finditer(text):
            val = m.group(1) or m.group(2)
            if val:
                rust_sidecars.append(val)
        for m in EMIT_RUST_RE.finditer(text):
            val = m.group(1) or m.group(2)
            if val:
                rust_emits.append(val)
        info.append(f"rust: {len(rust_cmds)} command(s) {[n for n, _ in rust_cmds]}")
        if rust_emits:
            info.append(f"rust emits: {sorted(set(rust_emits))}")
        if rust_sidecars:
            info.append(f"rust sidecars: {sorted(set(rust_sidecars))}")
    if args.frontend:
        fp = pathlib.Path(args.frontend)
        try:
            text = fp.read_text(encoding="utf-8")
        except Exception as e:
            print(f"FAIL {fp}: illisible ({e})")
            return 1
        front_invokes = INVOKE_RE.findall(text)
        front_events = LISTEN_FRONT_RE.findall(text)
        front_sidecars = SIDECAR_JS_RE.findall(text)
        front_has_channel = bool(CHANNEL_RE.search(text))
        if args.rust and not (front_invokes or front_events or front_sidecars or front_has_channel):
            errors.append("no frontend IPC call (invoke/emit/listen/Channel/Command.sidecar attendu)")
        for inv in front_invokes:
            if rust_cmds and inv not in [n for n, _ in rust_cmds]:
                errors.append(f"invoke '{inv}' has no matching Rust command ({sorted(n for n, _ in rust_cmds)})")
        info.append(f"frontend invokes: {sorted(set(front_invokes)) or '—'}")
        if front_events:
            info.append(f"frontend events: {sorted(set(front_events))}")
        if front_sidecars:
            info.append(f"frontend sidecars: {sorted(set(front_sidecars))}")
    if args.rust and args.frontend:
        rust_names = {n for n, _ in rust_cmds}
        matched_invoke = bool(set(front_invokes) & rust_names)
        matched_event = bool(set(front_events) & set(rust_emits))
        if not matched_invoke and not matched_event and not front_has_channel:
            if front_invokes or front_events:
                errors.append("no complete Rust<->frontend exchange (aucun invoke apparie ni event commun emit/listen)")
    if args.config:
        cp = pathlib.Path(args.config)
        try:
            data = json.loads(cp.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"FAIL {cp}: JSON illisible ({e})")
            return 1
        bundle = data.get("bundle") or {}
        if "externalBin" in bundle:
            eb = bundle["externalBin"]
            if not isinstance(eb, list) or not eb or not all(isinstance(x, str) and x.strip() for x in eb):
                errors.append("bundle.externalBin must be a non-empty list of strings")
            else:
                for _e in eb:
                    base = pathlib.PurePosixPath(_e).name
                    if any(t in base for t in ("x86_64", "aarch64", "i686", "unknown-linux", "apple-darwin", "pc-windows", "universal-apple")):
                        errors.append(
                            f"bundle.externalBin entry '{_e}' must not contain the -$TARGET_TRIPLE suffix "
                            "(triple on disk only, e.g. binaries/my-sidecar-x86_64-unknown-linux-gnu)"
                        )
                info.append(f"externalBin: {eb}")
                eb_basenames = {pathlib.PurePosixPath(x).name for x in eb}
                for s in front_sidecars:
                    if s not in eb:
                        errors.append(f"sidecar JS '{s}' not in bundle.externalBin {eb} (Command.sidecar must match externalBin entry)")
                for s in rust_sidecars:
                    if s not in eb_basenames and s not in eb:
                        errors.append(f"sidecar Rust '{s}' matches no bundle.externalBin basename {sorted(eb_basenames)} (shell().sidecar(name) sans chemin)")
        if "resources" in bundle:
            res = bundle["resources"]
            if isinstance(res, list):
                if not res or not all(isinstance(x, str) and x.strip() for x in res):
                    errors.append("bundle.resources list must be non-empty list of strings")
                else:
                    info.append(f"resources: {len(res)} entree(s)")
            elif isinstance(res, dict):
                if not res or not all(isinstance(k, str) and k.strip() for k in res.keys()):
                    errors.append("bundle.resources map must have non-empty string keys")
                else:
                    info.append(f"resources: map {len(res)} entree(s)")
            else:
                errors.append("bundle.resources must be a list or a map")
        if "externalBin" not in bundle and "resources" not in bundle:
            build = data.get("build") or {}
            info.append(f"config sans bundle.externalBin/resources (build keys: {sorted(build.keys()) or '—'})")
    label_parts = []
    if args.rust:
        label_parts.append(str(args.rust))
    if args.frontend:
        label_parts.append(str(args.frontend))
    if args.config and not label_parts:
        label_parts.append(str(args.config))
    elif args.config:
        label_parts.append(f"+ {args.config}")
    label = " + ".join(label_parts)
    if errors:
        print(f"FAIL {label}")
        for e in errors:
            print(f" - {e}")
        for i in info:
            print(f"   {i}")
        return 1
    print(f"OK {label}")
    for i in info:
        print(f" - {i}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
