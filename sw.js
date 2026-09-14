// Minimal offline cache so the PWA installs and opens without signal.
const FILES = ['./', 'index.html', 'manifest.json', 'icon.svg'];
self.addEventListener('install', e => e.waitUntil(caches.open('hr-v1').then(c => c.addAll(FILES))));
self.addEventListener('fetch', e => e.respondWith(fetch(e.request).catch(() => caches.match(e.request))));
