var C='eg-cache-v7';
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
    fetch(e.request).then(function(res){
      if(res&&res.ok&&res.type=='basic'){
        var c2=caches.open(C);
        c2.then(function(c){c.put(e.request,res.clone())});
      }
      return res;
    }).catch(function(){
      return caches.match(e.request);
    })
  );
});
