# Capabilities — extrait doc (prototype)

Source: `tauri-docs/src/content/docs/security/capabilities.mdx`, commit `ec113a50`, titre frontmatter `Capabilities`.

> Tauri provides application and plugin developers with a capabilities system,
> to granularly enable and constrain the core exposure to the application frontend running in the
> system WebView.
>
> Capabilities define which permissions are granted or denied for which windows or webviews.
> Capabilities can affect multiple windows and webviews and these can be referenced in multiple capabilities.
>
> Windows and WebViews which are part of more than one capability effectively merge the security boundaries and permissions of all involved capabilities.
>
> Capability files are either defined as a JSON or a TOML file inside the `src-tauri/capabilities` directory.
> All capabilities inside the `capabilities` directory are automatically enabled by default. Once capabilities are explicitly enabled in the `tauri.conf.json`, only these are used in the application build.

Exemple canonique (même fichier) : voir `examples/default-capability.json`.
Référence schéma complet : voir skill frère `tauri-config-cli-reference` (généré `reference/config.md`).
