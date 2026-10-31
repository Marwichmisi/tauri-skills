import { TrayIcon } from '@tauri-apps/api/tray';
import { Menu, CheckMenuItem, PredefinedMenuItem } from '@tauri-apps/api/menu';

// Tray icon native avec menu contextuel (desktop uniquement)
export async function createTray() {
  const showItem = await CheckMenuItem.new({
    id: 'tray-show',
    text: 'Show window',
    checked: true,
    action: () => console.log('show toggled'),
  });

  const quitItem = await PredefinedMenuItem.new({
    item: 'Quit',
    text: 'Quit',
  });

  const sep = await PredefinedMenuItem.new({ item: 'Separator' });

  await using trayMenu = await Menu.new({
    items: [showItem, sep, quitItem],
  });

  const tray = await TrayIcon.new({
    id: 'main-tray',
    // Chemin relatif vers `src-tauri/icons/` ou bytes chargés
    icon: 'icons/32x32.png',
    tooltip: 'My Tauri app',
    menu: trayMenu,
    menuOnLeftClick: true,
    action: (event) => {
      // event.type: 'Click' | 'DoubleClick' | 'RightClick' ...
      // event.button / event.buttonState selon plateforme
      if (event.type === 'Click' && event.button === 'Left') {
        console.log('tray left click');
      }
    },
  });

  return tray;
}

// get/set tooltip + visibilité (rappel API courante)
export async function updateTray(trayId = 'main-tray') {
  const { TrayIcon } = await import('@tauri-apps/api/tray');
  const tray = await TrayIcon.getById(trayId);
  if (!tray) return;
  await tray.setTooltip('Updated tooltip');
  await tray.setVisible(true);
}
