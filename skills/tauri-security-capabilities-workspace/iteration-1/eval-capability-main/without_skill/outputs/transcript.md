# Transcript — eval-capability-main (without_skill)

1. Vérifié que le dossier outputs existe (`read` → 0 entrées, dossier vide).
2. Écrit `capability.json` depuis la connaissance générale du format Tauri v2 :
   - `$schema`, `identifier: main-capability`, `description`, `windows: ["main"]`, `permissions` avec les 7 defaults core demandés + `core:window:allow-set-title`.
3. Écrit `answer.md` avec le JSON, l'explication des champs et la justification least-privilege.
4. Écrit le présent `transcript.md` décrivant les étapes.
