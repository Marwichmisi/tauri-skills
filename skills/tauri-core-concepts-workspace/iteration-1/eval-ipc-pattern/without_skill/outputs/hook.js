// dist-isolation/hook.js - hook minimal, zero dependance
// Charge depuis dist-isolation/index.html via <script src="hook.js"></script>
const ALLOWED_CMDS = new Set(["read_file", "http_fetch"]);

const ALLOWED_API_ORIGIN = "https://api.example.com";

window.__TAURI_ISOLATION_HOOK__ = async (message) => {
  const cmd = message?.cmd ?? message?.action?.cmd;
  const payload = message?.payload ?? message?.action?.payload ?? {};

  if (!cmd || !ALLOWED_CMDS.has(cmd)) {
    throw new Error("[isolation] commande bloquee: " + String(cmd));
  }

  if (cmd === "read_file") {
    if (typeof payload.path !== "string" || payload.path.includes("..")) {
      throw new Error("[isolation] chemin fichier invalide");
    }
    if (payload.path.length > 256) {
      throw new Error("[isolation] chemin trop long");
    }
  }

  if (cmd === "http_fetch") {
    let url;
    try {
      url = new URL(payload.url);
    } catch {
      throw new Error("[isolation] URL invalide");
    }
    if (url.origin !== ALLOWED_API_ORIGIN) {
      throw new Error("[isolation] origine HTTP non autorisee");
    }
  }

  return message;
};
