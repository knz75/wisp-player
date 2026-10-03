# Wisp - echo on your shoulder

**Wisp** is a free browser player where *you* decide where the sound lives: on your shoulder, ahead of you, far away - or flying around your head.

👉 **Try it:** [wispplayer.com](https://wispplayer.com) - put on headphones, open an audiobook, music or a radio stream, and drag the parrot.

## Why

Almost all music, films and "3D audio" are made for a listener who sits still and gives the sound *all* of their attention. The sound scene is designed by the author; the listener only accepts it.

Wisp flips that. Move the sound out of the center of your head - a little to the side and a bit further away - and it stops taking over. It becomes background, like a radio on a windowsill while you work. And because the "speaker" is tied to your head, it walks with you: around the room, down the street.

Let it fly in orbits, and it does the opposite: a gentle, living point that keeps a small part of your attention outward, on the world around you, instead of down into a screen.

## Features

- **Radar** - drag the parrot to place the sound: shoulder, ahead, behind, up to 3 m away.
- **Distance** - farther means quieter and duller, plus optional "room" ambience.
- **Orbits** - circle, oval, square, triangle, star, figure 8, spiral, comet (Kepler-style), pendulum, wander. Speed, size and direction are adjustable.
- **Audiobooks** - open files or a whole folder; the player remembers your position in every chapter.
- **Internet radio** - add any direct `https://` stream. Stations that don't allow processing still play in plain stereo.
- **Sleep timer, speed 1-1.5×, radar lock**, and a **3D off** switch to compare with normal stereo.
- **Skins** that change the whole player (Drone HUD, Watch, Classic '99) - a skin is a JSON file you can save, edit and share.
- **10 languages**, picked automatically from your device.
- **Installable app (PWA)**, works offline for local files.

## How it works

Everything runs in the browser with the built-in **Web Audio API**. No server processing: your files never leave your phone.

1. Downmix to **mono** - a stereo track becomes a single point.
2. Place the point with an **HRTF panner** (a generic model of how the head and ears shape sound from each direction).
3. Add **distance**: lower volume, a low-pass filter (down to ~5 kHz at 3 m) and a short, dark reverb.
4. Move **smoothly** (`setTargetAtTime`) to avoid clicks.

```javascript
const ctx = new AudioContext();
const src = ctx.createMediaElementSource(audio);

const mono = ctx.createGain();          // stereo → mono: the sound becomes a point
mono.channelCount = 1;
mono.channelCountMode = 'explicit';

const far = ctx.createBiquadFilter();   // distance: soften the highs
far.type = 'lowpass';

const panner = ctx.createPanner();      // place the point in space
panner.panningModel = 'HRTF';

src.connect(mono).connect(far).connect(panner).connect(ctx.destination);

// parrot on the right shoulder, slightly ahead (metres: x → right, z → back)
panner.positionX.value = 0.6;
panner.positionZ.value = -0.2;
```

The whole player is one HTML file (`index.html`) plus a manifest, a small offline service worker and icons. No build step, no frameworks.

## Also inside: Call and Companion

Two experiments built on the same sound engine as the player:

- **Wisp Call** ([/call.html](https://wispplayer.com/call.html)) - voice calls by link, up to 4 people. Every voice gets its own place around your head and slowly wanders inside its zone, like someone walking next to you. No accounts. Built on WebRTC; the server in [`call-server/`](call-server/) only introduces the phones to each other and relays audio when a direct connection is impossible (coturn).
- **Wisp Companion** ([/ai.html](https://wispplayer.com/ai.html)) - a personal voice AI on your shoulder, built on Gemini Live. You bring your own free Gemini API key: it is stored only in your browser and goes straight to Google. Pocket mode keeps the microphone alive while the screen is dark.

## Honest limitations

- **Headphones required.**
- **Everyone hears differently.** Left/right works for everyone; some people confuse ahead/behind with generic HRTF. Moving sources help, and it tends to get easier with practice.
- **Head-locked by design.** The sound turns with your head - the companion is part of you, not part of the room.
- **Radio:** 3D works only if the station allows cross-origin access (CORS); otherwise it plays in stereo.
- **Fast orbits** can make some people slightly dizzy after a few minutes.

## Privacy

No accounts, no cookies, no trackers. The hosted version sends tiny anonymous pings (`/e/open`, `/e/play`, `/e/orbit`…) with only the UI language and "app or web" - to count how the player is used. Your files, station names and positions are never sent anywhere. Calls go phone-to-phone (or through the relay) and are never recorded. Companion talks to Google directly with your own key.

## Feedback

Telegram: [@WispPlayer_bot](https://t.me/WispPlayer_bot) - bugs, ideas, translation fixes are very welcome.

## License

[MIT](LICENSE) © 2026 knz75. Use it, fork it, build on it - just keep the credit.

---

## --ру.

**Wisp - эхо на плече.** Бесплатный плеер в браузере, где вы сами решаете, где звучит звук: на плече, впереди, вдали или по орбите вокруг головы. Попробовать: [wispplayer.com](https://wispplayer.com), в наушниках.

Главная находка: если вывести звук из центра головы в сторону и немного вдаль, он перестаёт забирать всё внимание и работает как фон - как радио на подоконнике, пока вы работаете. А орбита, наоборот, превращает прогулку в ощущение: звук живёт вокруг вас, и взгляд остаётся на улице, а не в экране.

Всё работает на встроенном в браузер Web Audio, файлы никуда не уходят. Внутри ещё два эксперимента на том же звуке: **Звонок** - разговор по ссылке, где у каждого собеседника своё место вокруг головы, и **Попутчик** - голосовой ИИ на плече (Gemini Live, со своим бесплатным ключом).

Отзывы и идеи - в Telegram [@WispPlayer_bot](https://t.me/WispPlayer_bot).
