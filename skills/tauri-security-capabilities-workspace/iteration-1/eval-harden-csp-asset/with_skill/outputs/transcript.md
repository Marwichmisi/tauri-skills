# Transcript

- Lu `skills/tauri-security-capabilities/SKILL.md` → intention = durcissement → routage vers `references/hardening.md` + `examples/tauri.conf.json`.
- Lu `references/hardening.md` (CSP + asset-protocol formes tableau/objet, deny gagne, requireLiteralLeadingDot défaut true) et `examples/tauri.conf.json` (capabilities seules, non réutilisé tel quel).
- Vérifié commit local : `tauri-docs` HEAD = `ec113a50` (conforme à l'exigence).
- Vérifié fidélité contre sources canoniques EN : `tauri-docs/src/content/docs/security/csp.mdx` (titre `Content Security Policy (CSP)`) et `tauri-docs/src/content/docs/security/asset-protocol.mdx` (titre `Asset protocol scope`) — repris snippets `csp` minimal (sans hosts distants) et `assetProtocol` objet `allow $APPCACHE/**/*` / `deny $APPCACHE/**/secrets/**`.
- Écrit `outputs/tauri.conf.json` (snippet `app.security` uniquement) + `outputs/answer.md` (sources + frontière : schéma complet renvoyé à `tauri-config-cli-reference`, sans duplication).
