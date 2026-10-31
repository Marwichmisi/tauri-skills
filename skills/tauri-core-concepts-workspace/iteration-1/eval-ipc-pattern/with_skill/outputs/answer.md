# Recommandation IPC : passer en isolation

## Verdict : isolation (pas brownfield)

Votre cas cumule les deux déclencheurs documentés du pattern isolation :

1. **Dépendances frontend profondément imbriquées (centaines)** : le pattern isolation protège contre les appels frontend indésirables ou malveillants provenant de contenu non fiable / dépendances frontend profondément imbriquées (Development Threats, voir Security Threat Models).
2. **API Tauri externes (lecture fichier, fetch HTTP)** : la doc suggère fortement de verrouiller l'application dès qu'on utilise des API Tauri externes. L'application Isolation sécurisée permet de vérifier les entrées IPC pour s'assurer qu'elles respectent les paramètres attendus.

Référence : `concept/Inter-Process Communication/isolation.md`, commit `ec113a50` (via `references/ipc-patterns.md`).

Le pattern brownfield est le pattern par défaut, le plus simple et le plus compatible avec un frontend web existant, sans option de configuration supplémentaire (`concept/Inter-Process Communication/brownfield.md`). Il convient à un frontend maîtrisé et sans API sensible. Ce n'est pas votre cas : surface d'attaque supply-chain + API système → brownfield insuffisant.

> Tauri recommande fortement d'utiliser le pattern isolation chaque fois que c'est possible. Parce que l'application Isolation intercepte **tous** les messages du frontend, il peut **toujours** être utilisé.

## Config `tauri.conf.json` (pattern choisi)

Snippet `app.security.pattern` seul (schéma complet : voir skill `tauri-config-cli-reference`). Copie de `examples/isolation-pattern.json` :

```json
{
  "build": {
    "frontendDist": "../dist"
  },
  "app": {
    "security": {
      "pattern": {
        "use": "isolation",
        "options": {
          "dir": "../dist-isolation"
        }
      }
    }
  }
}
```

Fonctionnement : `<iframe>` sandboxé injecté entre le frontend et le Core ; tout l'IPC y transite d'abord, est chiffré en AES-GCM via `SubtleCrypto` avec une clé générée au runtime (nouvelles clés à chaque exécution), puis transmis au Core pour déchiffrement.

## Hook minimal (`hook.js`)

Copie de `examples/isolation-hook.js` — point de départ à durcir avec vos règles de validation :

```javascript
window.__TAURI_ISOLATION_HOOK__ = (payload) => {
  // let's not verify or modify anything, just print the content from the hook
  console.log('hook', payload);
  return payload;
};
```

En production, remplacez le `console.log` par une vérification des entrées IPC (commande autorisée ? arguments dans les bornes attendues ? sinon rejeter le message). Les appels concernés ici (lecture fichier, fetch HTTP) sont des **Commands** : abstraction style `fetch`/`invoke` de fonctions Rust avec arguments/retour sérialisables JSON (`concept/Inter-Process Communication/index.mdx`). Les changements d'état lifecycle fire-and-forget émis des deux côtés relèveraient des **Events** — hors sujet ici.

## Limites du pattern isolation (à accepter avant de migrer)

1. **Surcoût chiffrement systématique** : même si le hook ne fait rien, chaque message est chiffré ; généralement négligeable (AES-GCM rapide).
2. **Entropie pour la génération de clé** : si headless, installer `haveged` ; Linux 5.6+ OK.
3. **Windows + `<iframe>` sandboxé** : les fichiers externes ne se chargent pas → inlining des scripts au build ; `<script src="index.js">` fonctionne, les **ES Modules ne se chargeront PAS**.
4. **Simplicité obligatoire de l'app Isolation** : la garder aussi simple que possible, dépendances et étapes de build minimales (éviter les attaques supply-chain sur l'app Isolation elle-même). Ne pas y réintroduire vos centaines de dépendances.

## Frontières (renvois)

- Permissions/scopes/CSP/capabilities pour `fs` et `http` : skill `tauri-security-capabilities` (ici aucune permission déclarée).
- Code d'appel `invoke`/`listen`/`emit` et scopes : skill `tauri-ipc-bridge`.
- Schéma complet `tauri.conf.json` : skill `tauri-config-cli-reference`.
