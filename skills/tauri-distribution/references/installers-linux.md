# Installers Linux — extraits doc

Source: `tauri-docs/src/content/docs/distribute/debian.mdx`, commit `ec113a50`, titre frontmatter `Debian`.
Source: `tauri-docs/src/content/docs/distribute/rpm.mdx`, commit `ec113a50`, titre frontmatter `RPM`.
Source: `tauri-docs/src/content/docs/distribute/appimage.mdx`, commit `ec113a50`, titre frontmatter `AppImage`.
Source: `tauri-docs/src/content/docs/distribute/aur.mdx`, commit `ec113a50`, titre frontmatter `AUR`.
Source: `tauri-docs/src/content/docs/distribute/flatpak.mdx`, commit `ec113a50`, titre frontmatter `Flathub`.
Source: `tauri-docs/src/content/docs/distribute/snapcraft.mdx`, commit `ec113a50`, titre frontmatter `Snapcraft`.

> `AppImage` is a distribution format that does not rely on the system installed packages and instead bundles all dependencies (distribute/appimage.mdx).

- Debian : paquet `.deb` via `tauri build` ; dépendances système via `tauri.conf.json > bundle > linux > deb` ; fichiers custom via `bundle > linux > deb > files` (map chemin paquet → fichier relatif à `tauri.conf.json`). Exemple doc :
```json
"deb": { "files": { "/usr/share/README.md": "../README.md" } }
```
- RPM : même gabarit via `bundle > linux > rpm` ; build ARM via `rust targets` + sysroot (voir distribute/rpm.mdx § ARM).
- AppImage : `chmod a+x MyProject.AppImage && ./MyProject.AppImage` ; média via `bundle > linux > appimage > bundleMediaFramework` ; fichiers custom via `bundle > linux > appimage > files`.
- AUR : publier via PKGBUILD qui télécharge le `.deb` release (`source_x86_64=("${url}/releases/download/v${pkgver}/appname_${pkgver}_amd64.deb")`), build `pnpm tauri build -b deb`, copie `target/release/bundle/deb/<project>_${pkgver}_*/data/*` vers `${pkgdir}`.
- Flatpak/Flathub + Snapcraft : empaquetage externe documenté dans leurs pages ; ne pas inventer de `targets` hors allowlist du check.

Bundle targets CLI documentés : `app,dmg,msi,nsis,deb,rpm,appimage` (voir distribute/index.mdx `--bundles app,dmg`). Valider avec `scripts/check-distribution.py --bundle`.
