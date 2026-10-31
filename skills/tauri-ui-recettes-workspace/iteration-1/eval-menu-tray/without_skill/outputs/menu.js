import { Menu, MenuItem, CheckMenuItem, PredefinedMenuItem } from '@tauri-apps/api/menu';

// Menu applicatif natif (desktop uniquement)
export async function createAppMenu() {
  // `await using` : libère le menu en fin de scope (Explicit Resource Management).
  // Nécessite ES2026 / TypeScript 5.2+ avec `lib: ["esnext.disposable"]`.
  await using menu = await Menu.new({
    items: [
      {
        id: 'file',
        text: 'File',
        items: [
          {
            id: 'new-file',
            text: 'New File',
            accelerator: 'CmdOrCtrl+N',
            action: () => console.log('new file'),
          },
          {
            item: 'Separator',
          },
          {
            id: 'quit',
            text: 'Quit',
            action: () => console.log('quit clicked'),
          },
        ],
      },
    ],
  });

  // Variante objet : quit / check / separator via builders
  const quitItem = await PredefinedMenuItem.new({
    text: 'Quit App',
    item: 'Quit',
  });

  const checkItem = await CheckMenuItem.new({
    id: 'show-statusbar',
    text: 'Show Status Bar',
    checked: true,
    action: (id) => console.log('toggled', id),
  });

  const sep = await PredefinedMenuItem.new({ item: 'Separator' });

  await using appMenu = await Menu.new({
    items: [quitItem, sep, checkItem],
  });

  // Définit comme menu natif de l'application (macOS: menu bar, Windows/Linux: menu fenêtre)
  await appMenu.setAsAppMenu();

  // get/setText sur un item existant
  const current = await checkItem.text();
  console.log('current text:', current);
  await checkItem.setText('Show Status Bar (enabled)');

  return appMenu;
}

// Exemple get/setText sur un MenuItem simple
export async function renameItem() {
  const item = await MenuItem.new({
    id: 'open',
    text: 'Open',
    accelerator: 'CmdOrCtrl+O',
    action: () => {},
  });
  console.log(await item.text());
  await item.setText('Open File…');
}
