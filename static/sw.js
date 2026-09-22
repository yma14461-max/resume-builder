const CACHE_NAME = 'resume-builder-pwa-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/manifest.json',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png'
];

// 서비스 워커 설치 시 핵심 정적 자원 캐싱
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// 서비스 워커 활성화 및 이전 캐시 정리
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 네트워크 요청 처리: API 호출은 캐시하지 않고 통과, 정적 파일은 캐시 우선
self.addEventListener('fetch', (event) => {
  // AI 생성 API (/generate)는 캐시 제외하고 항상 네트워크로 전송
  if (event.request.method !== 'GET' || event.request.url.includes('/generate')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).catch(() => {
        // 오프라인일 때 기본 페이지 반환
        if (event.request.mode === 'navigate') {
          return caches.match('/');
        }
      });
    })
  );
});
