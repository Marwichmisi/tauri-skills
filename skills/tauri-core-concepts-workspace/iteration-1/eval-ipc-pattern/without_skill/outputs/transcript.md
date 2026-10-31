# Transcript (without_skill)

- No skill used (baseline, general knowledge only).
- No skill files read.
- Decision: isolation over brownfield due to large untrusted dependency tree + sensitive APIs (file read, HTTP).
- Wrote: answer.md, tauri.conf.json (pattern.use=isolation + tight allowlist/CSP), hook.js (whitelist read_file/http_fetch + arg validation).
