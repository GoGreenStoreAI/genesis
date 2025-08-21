// Simple service worker: cache-first for app shell, network for API
const CACHE_NAME = 'genesis-v1';
const ASSETS = [
  '/genesis/',
  '/genesis/index.html',
  '/genesis/posts.html',
  '/genesis/uploads.html',
  '/genesis/about.html',
  '/genesis/docs/index.html',
  '/genesis/manifest.webmanifest'
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(clients.claim());
});

self.addEventListener('fetch', event => {
  const req = event.request;
  // network-first for api requests, cache-first for app shell
  if (req.method !== 'GET') return;
  event.respondWith(
    caches.match(req).then(cached => {
      if (cached) return cached;
      return fetch(req).then(res => {
        return caches.open(CACHE_NAME).then(cache => {
          try { cache.put(req, res.clone()); } catch(e){/* ignore */ }
          return res;
        });
      }).catch(() => caches.match('/genesis/index.html'));
    })
  );
});
