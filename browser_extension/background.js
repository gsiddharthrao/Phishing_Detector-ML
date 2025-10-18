// background service worker - currently minimal. Kept for future event handling.
self.addEventListener('install', (e) => {
  // skip waiting to activate immediately in dev
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  clients.claim();
});
