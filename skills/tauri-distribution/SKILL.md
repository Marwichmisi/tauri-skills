---
name: tauri-distribution
description: Package, sign and auto-update a Tauri v2 app per OS (installers, stores, pipelines, updater). Use me whenever the agent bundles, signs, publishes to stores, wires CI release pipelines, or configures the updater — I own distribution doctrine with per-OS sub-routing (no per-OS skill); config schema lives in tauri-config-cli-reference, permission doctrine in tauri-security-capabilities.
---

# Tauri Distribution

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust linkée, jamais copiée.
> Gabarit commun aux 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (installer desktop vs store vs signature vs pipeline/updater).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Lancer `scripts/check-distribution.py` avec le mode du tableau pour valider tout artefact.
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Packager Linux (deb/rpm/appimage/AUR/flatpak/snap, `bundle > linux > * > files`) | `references/installers-linux.md` | `examples/tauri.conf.bundle.json` | `scripts/check-distribution.py --bundle` |
| Packager desktop Windows/macOS (msi/nsis/webviewInstallMode, app/dmg, split build/bundle) | `references/installers-desktop.md` | `examples/tauri.conf.bundle.json` | `scripts/check-distribution.py --bundle` |
| Publier en store (App Store / Microsoft Store / Google Play, AAB/APK, keystore.properties) | `references/stores.md` | `examples/signing.env` | `scripts/check-distribution.py --sign` |
| Signer par OS (WINDOWS_*/APPLE_*/SIGN*/IOS_*/keytool, SmartScreen/notarisation) | `references/signing.md` | `examples/signing.env` | `scripts/check-distribution.py --sign` |
| Pipeline + updater (tauri-action, CrabNebula, `signer generate`, pubkey/endpoints/installMode) | `references/pipelines-updater.md` | `examples/tauri.conf.updater.json`, `examples/publish-github.yml` | `scripts/check-distribution.py --updater` |
| Doute inter-skill (schéma config complet, capability/permission, fiche plugin) | voir Frontières | — | — |

## Frontières

- `tauri-config-cli-reference` : schéma `tauri.conf.json`/`gen/schemas` complet et CLI (`build/bundle/sign`). Ici on ne montre que `bundle.targets/createUpdaterArtifacts`, `plugins.updater`, `webviewInstallMode`.
- `tauri-security-capabilities` : seule autorité capabilities/permissions/scopes. Ici aucune permission inventée ; l'updater exige `<plugin>:default` côté capability, doctrine là-bas.
- `tauri-plugins-catalogue` : les 30 fiches `plugin/*` hors updater vivent là-bas (décision #3) ; `plugin/updater.mdx` est rattaché ici (voir TRACABILITE.md), les fiches catalogue renvoient ici pour l'auto-update.
- `tauri-start`, `tauri-migrate`, `tauri-core-concepts`, `tauri-ipc-bridge`, `tauri-dev-quality`, `tauri-plugin-dev`, `tauri-ui-recettes`, `tauri-frontend-bindings` : hors périmètre distribution ; renvoyer si le besoin réel y bascule.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucun contenu inventé. Bundle targets doc seuls (`app,dmg,msi,nsis,deb,rpm,appimage`), endpoints `https` sauf `dangerousInsecureTransportProtocol`, vars doc seules (`TAURI_SIGNING_*`, `APPLE_*`, `WINDOWS_*`, `IOS_*`, `SIGN*`/`APPIMAGETOOL_*`, plus `GITHUB_TOKEN` pipeline documenté en Pipelines/github).
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Updater signé : `examples/tauri.conf.updater.json` + `examples/publish-github.yml`.
Valider avec `python3 scripts/check-distribution.py --updater examples/tauri.conf.updater.json` et `--bundle examples/tauri.conf.bundle.json` et `--sign examples/signing.env`.
