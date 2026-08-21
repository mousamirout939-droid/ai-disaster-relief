// Note: In production the VitePWA plugin auto-generates the real service worker
// via Workbox (see vite.config.js). This file is kept as a documented fallback
// entrypoint for environments building without the Vite PWA plugin.
const CACHE_NAME = 'disaster-relief-shell-v1';
const APP_SHELL = ['/', '/index.html', '/offline.html'];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)));
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request).then((r) => r || caches.match('/offline.html')))
  );
});
