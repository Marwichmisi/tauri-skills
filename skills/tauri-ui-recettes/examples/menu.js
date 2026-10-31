import { Menu } from '@tauri-apps/api/menu';

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
      id: 'check_item',
      text: 'Check Item',
      checked: true,
    },
    {
      item: 'Separator',
    },
  ],
});

// If a window was not created with an explicit menu or had one set explicitly,
// this menu will be assigned to it.
await using prev = await menu.setAsAppMenu();

// Update individual menu item text
await using statusItem = await menu.get('status');
if (statusItem) {
  await statusItem.setText('Status: Ready');
}
