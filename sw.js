// Wisp - работа без интернета.
// Плеер (страница и иконки) сохраняется в телефоне. Сначала пробуем свежую версию из сети,
// а если сети нет или она слишком медленная (3.5 с) - открываем сохранённую. Музыка, книги и радио сюда не попадают.
const CACHE = 'wisp-v5';
const NET_WAIT_MS = 3500; // сколько ждём сеть, прежде чем открыть сохранённую копию
const SHELL = ['/', '/index.html', '/manifest.json', '/icon-192.png', '/icon-512.png', '/icon-maskable-512.png', '/apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  const url = new URL(req.url);
  // Чужие адреса (радиостанции) и не-GET запросы не трогаем вообще
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;
  // Аудио и запросы с диапазоном байт идут мимо
  if (req.headers.has('range') || req.destination === 'audio') return;
  // Отметки статистики - только в сеть
  if (url.pathname.startsWith('/e/')) return;
  // Звонок и попутчик живут сами по себе: их запросы не трогаем
  if (url.pathname.startsWith('/call') || url.pathname.startsWith('/ai')) return;

  e.respondWith((async () => {
    // Сохранённая копия: страница, а для переходов по ссылкам вида /?call=... - главная
    const cached = await caches.match(req) || (req.mode === 'navigate' ? await caches.match('/index.html') : undefined);
    const net = fetch(req).then(res => {
      if (res.ok && SHELL.includes(url.pathname)) {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    });
    // Копии нет (самый первый запуск) - ждём сеть сколько нужно
    if (!cached) return net;
    // Копия есть: свежая версия из сети - если ответила быстро. Сеть упала или зависла (слабый интернет) - открываем копию,
    // а запрос в фоне доделается и обновит копию к следующему запуску.
    return Promise.race([
      net.catch(() => cached),
      new Promise(resolve => setTimeout(() => resolve(cached), NET_WAIT_MS))
    ]);
  })());
});
