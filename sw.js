/* Service worker du Palazzo dell'italiano : mode hors-ligne.
   - l'app (page, données, three.js, icônes) est gardée dans un cache versionné ;
   - la page et data3d.json passent d'abord par le réseau (pour recevoir les mises à jour), puis par le cache ;
   - les sons (paquets mp3 par salle, versionnés par ?v=) restent dans un cache à part, gardé d'une version à l'autre ;
   - les polices et scripts externes sont servis depuis le cache puis rafraîchis en arrière-plan ;
   - la synchronisation de progression (Supabase) ne passe jamais par le cache. */
const VERSION = "02a0311533";
const CORE = "pmit-core-" + VERSION, EXT = "pmit-ext", AUDIO = "pmit-audio";
const FILES = ["./", "index.html", "data3d.json", "config.js", "offline.js", "manifest.json", "vendor/three.min.js",
  "validation.html", "apple-touch-icon.png", "icon-512.png", "favicon-32.png", "logo.svg"];

self.addEventListener("install", ev => {
  ev.waitUntil(caches.open(CORE).then(c => Promise.all(FILES.map(u => c.add(new Request(u, { cache: "reload" })).catch(() => null)))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", ev => {
  ev.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("pmit-core-") && k !== CORE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

const timeout = (p, ms) => Promise.race([p, new Promise((_, ko) => setTimeout(() => ko(new Error("lent")), ms))]);
async function networkFirst(req) {
  const c = await caches.open(CORE);
  try { const r = await timeout(fetch(req), 4000); if (r.ok) c.put(req, r.clone()); return r; }
  catch (e) { return (await c.match(req, { ignoreSearch: true })) || (req.mode === "navigate" ? c.match("index.html") : Response.error()); }
}
async function cacheFirst(req, name) {
  const c = await caches.open(name), hit = await c.match(req);
  if (hit) return hit;
  const r = await fetch(req); if (r.ok || r.type === "opaque") c.put(req, r.clone()); return r;
}
async function staleWhileRevalidate(req) {
  const c = await caches.open(EXT), hit = await c.match(req);
  const net = fetch(req).then(r => { if (r.ok || r.type === "opaque") c.put(req, r.clone()); return r; }).catch(() => null);
  return hit || (await net) || Response.error();
}

self.addEventListener("fetch", ev => {
  const req = ev.request, url = new URL(req.url);
  if (req.method !== "GET" || /supabase\.co$/.test(url.hostname)) return;   // progression : toujours en direct
  if (url.origin === location.origin) {
    if (url.pathname.includes("/audio/")) return ev.respondWith(cacheFirst(req, AUDIO));
    if (req.mode === "navigate" || /\/(index\.html|data3d\.json|config\.js|offline\.js|validation\.html)?$/.test(url.pathname)) return ev.respondWith(networkFirst(req));
    return ev.respondWith(cacheFirst(req, CORE));
  }
  ev.respondWith(staleWhileRevalidate(req));   // polices Google, supabase-js (jsDelivr)
});

/* Messages de la page : état du cache des sons, téléchargement de tous les sons, ménage des anciens paquets */
self.addEventListener("message", ev => {
  const m = ev.data || {}, port = ev.ports && ev.ports[0];
  const reply = x => port && port.postMessage(x);
  (async () => {
    const c = await caches.open(AUDIO);
    const urls = (m.urls || []).map(u => new URL(u, self.registration.scope).href);
    if (m.type === "audio-status" || m.type === "audio-fetch") {
      const keys = new Set((await c.keys()).map(r => r.url));
      for (const k of keys) if (!urls.includes(k)) await c.delete(k);   // paquets d'une version précédente
      let have = urls.filter(u => keys.has(u)).length;
      if (m.type === "audio-status") return reply({ have, total: urls.length });
      for (const u of urls) {
        if (keys.has(u)) continue;
        try { const r = await fetch(u); if (r.ok) { await c.put(u, r); have++; } } catch (e) {}
        reply({ have, total: urls.length, progress: true });
      }
      reply({ have, total: urls.length, done: true });
    }
  })();
});
