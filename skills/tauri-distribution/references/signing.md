# Signing par OS — extraits doc

Source: `tauri-docs/src/content/docs/distribute/Sign/windows.mdx`, commit `ec113a50`, titre frontmatter `Windows Code Signing`.
Source: `tauri-docs/src/content/docs/distribute/Sign/macos.mdx`, commit `ec113a50`, titre frontmatter `macOS Code Signing`.
Source: `tauri-docs/src/content/docs/distribute/Sign/linux.mdx`, commit `ec113a50`, titre frontmatter `Linux Code Signing`.
Source: `tauri-docs/src/content/docs/distribute/Sign/android.mdx`, commit `ec113a50`, titre frontmatter `Android Code Signing`.
Source: `tauri-docs/src/content/docs/distribute/Sign/ios.mdx`, commit `ec113a50`, titre frontmatter `iOS Code Signing`.

> Code signing is required on Windows to allow your application to be listed in the Microsoft Store and to prevent a SmartScreen warning (Sign/windows.mdx).
> Code signing is required on macOS to allow your application to be listed in the Apple App Store (Sign/macos.mdx).

- Windows : certificat OV (`openssl pkcs12 -export -in cert.cer -inkey private-key.key -out certificate.pfx`), import `Import-PfxCertificate -CertStoreLocation Cert:\CurrentUser\My`, vars `WINDOWS_CERTIFICATE` (base64 pfx via `certutil -encode certificate.pfx base64cert.txt`), `WINDOWS_CERTIFICATE_PASSWORD`. Azure Key Vault en alternative (doc § custom sign command).
- macOS : Apple Developer (payant 99$/an, gratuit = test sans notarisation), `security find-identity -v -p codesigning` = signing identity, vars `APPLE_SIGNING_IDENTITY`, `APPLE_CERTIFICATE` (base64 p12), `APPLE_CERTIFICATE_PASSWORD`, notarisation `APPLE_ID` + `APPLE_PASSWORD` (app-specific) + `APPLE_TEAM_ID`, ou API key `APPLE_API_ISSUER` + `APPLE_API_KEY` + `APPLE_API_KEY_PATH`.
- Linux AppImage : `SIGN=1`, optionnel `SIGN_KEY` (GPG Key ID), `APPIMAGETOOL_SIGN_PASSPHRASE` (requis en CI), `APPIMAGETOOL_FORCE_SIGN=1` pour échouer au lieu de générer quand même.
- Android : `keytool -genkey ... -keystore ~/upload-keystore.jks`, fichier `src-tauri/gen/android/keystore.properties` (`password/keyAlias/storeFile`), ne jamais committer keystore/properties.
- iOS : `APPLE_API_ISSUER` + `APPLE_API_KEY` + `APPLE_API_KEY_PATH`, `IOS_CERTIFICATE` (base64 keychain) + `IOS_CERTIFICATE_PASSWORD`, `IOS_MOBILE_PROVISION` (base64 provisioning profile).
- Updater (tout OS) : `TAURI_SIGNING_PRIVATE_KEY` (+ `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`), `tauri signer generate -w ~/.tauri/myapp.key` (voir references/pipelines-updater.md).

Valider avec `scripts/check-distribution.py --sign examples/signing.env`. Noms hors allowlist = invention.
