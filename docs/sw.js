/* ConfigForge V2Ray SW — stale-while-revalidate (simplified) */
const SW_VERSION = 'cfv2-2025-09-02-b';
const STATIC_CACHE = `static-${SW_VERSION}`;
const RUNTIME_CACHE = `runtime-${SW_VERSION}`;

const PRECACHE_URLS = [
  './',
  './index.html',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.addAll(PRECACHE_URLS)).then(()=>self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.map((k) => (k.startsWith('static-') || k.startsWith('runtime-')) && k !== STATIC_CACHE && k !== RUNTIME_CACHE ? caches.delete(k) : null))
    ).then(()=>self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET' && req.method !== 'HEAD') return;

  const url = new URL(req.url);
  const swrHosts = new Set(['raw.githubusercontent.com','ipapi.co','api.qrserver.com','cdn.jsdelivr.net']);

  if (swrHosts.has(url.hostname)) {
    event.respondWith((async () => {
      const cache = await caches.open(RUNTIME_CACHE);
      const cached = await cache.match(req);
      const fetchPromise = fetch(req).then((resp) => {
        if (resp && (resp.status === 200 || resp.status === 304)) cache.put(req, resp.clone());
        return resp;
      }).catch(() => cached);
      return cached || fetchPromise;
    })());
    return;
  }

  event.respondWith(fetch(req).catch(() => caches.match(req)));
});
