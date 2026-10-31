# Stores desktop + mobile — extraits doc

Source: `tauri-docs/src/content/docs/distribute/app-store.mdx`, commit `ec113a50`, titre frontmatter `App Store`.
Source: `tauri-docs/src/content/docs/distribute/microsoft-store.mdx`, commit `ec113a50`, titre frontmatter `Microsoft Store`.
Source: `tauri-docs/src/content/docs/distribute/google-play.mdx`, commit `ec113a50`, titre frontmatter `Google Play`.

- App Store (macOS) : signing + notarisation Apple requis ; bundle `app` avec config dédiée `tauri.appstore.conf.json` et target `universal-apple-darwin` (voir distribute/app-store.mdx). Renvoi signature : `references/signing.md`.
- Microsoft Store : soumission MSIX/appx via build Windows signé ; SmartScreen sans signature = warning (voir distribute/microsoft-store.mdx + Sign/windows). Renvoi signature Windows : `references/signing.md`.
- Google Play : AAB/APK signé via keystore `keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload`, config `src-tauri/gen/android/keystore.properties` (`password/keyAlias/storeFile`). Voir distribute/Sign/android.mdx, résumé en `references/signing.md`.

Ne pas inventer de format store. Les pages stores décrivent la soumission, la signature vit en `references/signing.md`.
