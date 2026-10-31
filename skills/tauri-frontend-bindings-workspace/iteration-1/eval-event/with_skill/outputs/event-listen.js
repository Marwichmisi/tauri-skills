import { listen, emit, TauriEvent } from '@tauri-apps/api/event';

const unlisten = await listen(TauriEvent.WINDOW_DESTROYED, (event) => {
  console.log('a window was destroyed', event.payload);
});

await emit('frontend-loaded', { loggedIn: true, token: 'authToken' });
