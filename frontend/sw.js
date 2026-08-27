self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open("ir-radar-v1").then((cache) => {
      return cache.addAll(["/frontend/index.html"]);
    })
  );
});

self.addEventListener("fetch", (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => {
      return res || fetch(e.request);
    })
  );
});
