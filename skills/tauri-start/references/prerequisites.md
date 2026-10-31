# Prérequis — extrait doc

Sources (toutes commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/start/prerequisites.mdx` (titre `Prerequisites`)
- `tauri-docs/src/content/docs/start/index.mdx` (titre `What is Tauri?`, § Why Tauri rappelé en fin)

> In order to get started building your project with Tauri you'll first need to install a few dependencies:
> 1. [System Dependencies](#system-dependencies)
> 2. [Rust](#rust)
> 3. [Configure for Mobile Targets](#configure-for-mobile-targets) (only required if developing for mobile)

## System Dependencies

> Follow the link to get started for your respective operating system:
> - [Linux](#linux) (see below for specific distributions)
> - [macOS Catalina (10.15) and later](#macos)
> - [Windows 7 and later](#windows)

### Linux (extraits Debian/Arch/Fedora, même fichier)

```sh
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev \
  build-essential curl wget file libxdo-dev libssl-dev \
  libayatana-appindicator3-dev librsvg2-dev
```

```sh
sudo pacman -Syu
sudo pacman -S --needed webkit2gtk-4.1 base-devel curl wget file openssl \
  appmenu-gtk-module libappindicator-gtk3 librsvg xdotool
```

```sh
sudo dnf check-update
sudo dnf install webkit2gtk4.1-devel openssl-devel curl wget file \
  libappindicator-gtk3-devel librsvg2-devel libxdo-devel
sudo dnf group install "c-development"
```

Autres variantes même fichier : Gentoo, OSTree, openSUSE, Alpine (`build-base`, `webkit2gtk-4.1-dev`, note fonts `font-dejavu`, note musl `*-static`), NixOS (renvoi wiki). Si distribution absente : voir Awesome Tauri.

### macOS

> Tauri uses [Xcode](https://developer.apple.com/xcode/resources/) and various macOS and iOS development dependencies.
> Download and install Xcode from Mac App Store or Apple Developer website. Be sure to launch Xcode after installing.

Desktop seul : `xcode-select --install` suffit.

### Windows

> Tauri uses the Microsoft C++ Build Tools for development as well as Microsoft Edge WebView2.

- C++ Build Tools : cocher "Desktop development with C++".
- WebView2 : déjà présent sur Windows 10 (1803+) et ultérieur, sinon installer "Evergreen Bootstrapper".
- MSI uniquement : activer la fonctionnalité optionnelle VBSCRIPT (`failed to run light.exe` sinon).

## Rust (même fichier)

> Tauri is built with [Rust](https://www.rust-lang.org) and requires it for development.

- Linux/macOS : `curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh`
- Windows : https://www.rust-lang.org/tools/install ou `winget install --id Rustlang.Rustup`
- Windows MSVC par défaut : `rustup default stable-msvc` (requis pour `trunk`).
- Redémarrer Terminal/système après installation.

## Node.js (même fichier, écosystème JS uniquement)

1. Installer Node LTS depuis nodejs.org.
2. Vérifier : `node -v` / `npm -v`.
3. Optionnel : `corepack enable` pour pnpm/yarn.

## Mobile (même fichier, seulement si Android/iOS)

- Android : Android Studio, `JAVA_HOME`, SDK (Platform, Platform-Tools, NDK Side by side, Build-Tools, Command-line Tools), `ANDROID_HOME`/`NDK_HOME`, puis `rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android`.
- iOS (macOS + Xcode complet uniquement) : `rustup target add aarch64-apple-ios x86_64-apple-ios aarch64-apple-ios-sim`, `brew install cocoapods`.

Dépannage : voir `develop/debug/` (skill `tauri-dev-quality`) ou Discord Tauri.

## Pourquoi Tauri (rappel `start/index.mdx`, pas de décision ici)

> Tauri is a framework for building tiny, fast binaries for all major desktop and mobile platforms. Developers can integrate any frontend framework that compiles to HTML, JavaScript, and CSS.

3 avantages : secure foundation (Rust + audits), smaller bundle (<600KB via webview système), flexible architecture (tout frontend + bindings `invoke`, TAO/WRY). Détail architecture : skill `tauri-core-concepts`.
