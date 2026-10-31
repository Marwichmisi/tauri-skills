# Transcript — eval bundle-desktop (with skill)

1. Lu `skills/tauri-distribution/SKILL.md` → routage intention « Packager desktop Windows/macOS » → `references/installers-desktop.md`, exemple `examples/tauri.conf.bundle.json`, script `--bundle`.
2. Lu `references/installers-desktop.md` (Sources : `distribute/windows-installer.mdx`, `distribute/dmg.mdx`, `distribute/macos-application-bundle.mdx`, `distribute/index.mdx`, commit `ec113a50`) : MSI = WiX v3, NSIS = .exe, `webviewInstallMode` 4 modes, macOS `app` puis `dmg`, split `--no-bundle` + `tauri bundle`.
3. Écrit `outputs/bundle.json` avec `targets: [msi, nsis, app, dmg]` + `windows.webviewInstallMode.embedBootstrapper`.
4. Check exécuté :

```
$ python3 skills/tauri-distribution/scripts/check-distribution.py --bundle skills/tauri-distribution-workspace/iteration-1/eval-bundle-desktop/with_skill/outputs/bundle.json
OK skills/tauri-distribution-workspace/iteration-1/eval-bundle-desktop/with_skill/outputs/bundle.json: targets=msi,nsis,app,dmg
```

5. Pas de skill par OS : un seul routage manifeste, une seule passe.
