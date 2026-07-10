var C='eg-cache-v11';
var URLS=['index.html','sw.js'];
self.addEventListener('install',function(e){
  e.waitUntil(caches.open(C).then(function(c){return c.addAll(URLS)}));
  self.skipWaiting();
});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(kk){return kk!=C}).map(function(kk){return caches.delete(kk)}))}));
  self.clients.claim();
});
self.addEventListener('fetch',function(e){
  e.respondWith(
    caches.match(e.request).then(function(r){
      return r||fetch(e.request).then(function(res){
        if(res&&res.ok&&res.type=='basic'){
          var c2=caches.open(C);
          c2.then(function(c){c.put(e.request,res.clone())});
        }
        return res;
      });
    })
  );
});
