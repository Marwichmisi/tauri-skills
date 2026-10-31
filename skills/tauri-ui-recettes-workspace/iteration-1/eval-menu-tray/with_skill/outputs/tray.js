import { TrayIcon } from '@tauri-apps/api/tray';
import { Menu } from '@tauri-apps/api/menu';
import { defaultWindowIcon } from '@tauri-apps/api/app';

await using menu = await Menu.new({
  items: [
    {
      id: 'quit',
      text: 'Quit',
      action: () => {
        console.log('quit pressed');
      },
    },
    {
      item: 'Separator',
    },
  ],
});

const options = {
  icon: await defaultWindowIcon(),
  menu,
  menuOnLeftClick: true,
  action: (event) => {
    switch (event.type) {
      case 'Click':
        console.log(`mouse ${event.button} button pressed, state: ${event.buttonState}`);
        break;
      case 'DoubleClick':
        console.log(`mouse ${event.button} button pressed`);
        break;
      case 'Enter':
      case 'Move':
      case 'Leave':
        break;
    }
  },
};

const tray = await TrayIcon.new(options);
await menu.close();
