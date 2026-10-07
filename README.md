# Wisp - echo on your shoulder

**Wisp** is a free browser player where *you* decide where the sound lives: on your shoulder, ahead of you, far away - or flying around your head.

👉 **Try it:** [wispplayer.com](https://wispplayer.com) - put on headphones, open an audiobook, music or a radio stream, and drag the parrot.

## Why

Almost all music, films and "3D audio" are made for a listener who sits still and gives the sound *all* of their attention. The sound scene is designed by the author; the listener only accepts it.

Wisp flips that. Move the sound out of the center of your head - a little to the side and a bit further away - and it stops taking over. It becomes background, like a radio on a windowsill while you work. And because the "speaker" is tied to your head, it walks with you: around the room, down the street.

Let it fly in orbits, and it does the opposite: a gentle, living point that keeps a small part of your attention outward, on the world around you, instead of down into a screen.

## A personal layer, not a window into another world

VR, AR and head tracking try to pin sound to the world: the forest stays behind the window, the voice stays in the corner of the room, and when you turn your head the sound stays put. That is a way of *replacing* reality or blending into it.

Wisp is the opposite on purpose. It is a **personal layer** between you and the world - a transparent dome, like a helmet or a shawl. The sounds live on its surface and move with you; the world outside stays the world. On a treadmill you are not *in* a cave - you are in your own dome that sounds like a cave. Your brain already has enough to do while you walk; it does not need to check whether the forest in your ears matches the window. That is why Wisp has no head tracking: not a missing feature, a different idea.

Inside the dome, **distance means closeness**, the way it does between people (the anthropologist Edward T. Hall called these proxemic zones):

| Layer | Distance | What lives there | How it feels |
| --- | --- | --- | --- |
| Intimate | at the ear, up to ~0.5 m | messages, the companion | personal, only for you |
| Personal | 0.5-1.2 m | an audiobook, a friend on a call | close, «with me» |
| Room | 1.2-3 m | music, radio | like furniture: there, but not in the way |
| Far | 3 m and beyond | rain, forest, city | background, air, a sense of place |

This is where «music steps aside» comes from: what matters moves into a nearer layer, the rest moves further out. Not louder or quieter - closer or further.

Screens cannot do this. A huge TV on the wall or a monitor in front of your eyes is still one flat surface: windows and tabs can only be stacked, and «nearer» or «further» can only be drawn. By ear, distance is felt at once - from loudness, from how the high frequencies fade, from how much room echo there is - with no effort at all. And sounds at different distances do not hide each other: the brain separates them by itself, the way you follow one voice in a noisy café.

**Calm, not immersive.** Dolby Atmos, games and films are made for immersion: they take you out of reality into an imagined scene - a battlefield, a desert, space - and that needs you to sit still and imagine. On the street this works against you: the scene in your ears argues with what your eyes see. Wisp does the opposite: it does not pretend to be another place, it only lays the sounds out around you, and reality stays in charge. This is what Mark Weiser and John Seely Brown called *calm technology* in the 1990s: it lives at the edge of attention and comes to the center only when needed. In Wisp that is literal - the far layer is the edge, the layer at your ear is the center. So the rule is simple: on the move, sound never argues with what your eyes see. No battlefields or caves by default - only places and distances. An «atmosphere» is something you switch on yourself, when reality can be let go - on a treadmill, at home with your eyes closed.

## Features

- **Radar** - drag the parrot to place the sound: shoulder, ahead, behind, up to 3 m away.
- **Distance** - farther means quieter and duller, plus optional "room" ambience.
- **Orbits** - five main shapes on screen (circle, behind, pendulum, wander, figure 8) and more under «⋯»: oval, square, triangle, star, spiral, comet (Kepler-style). Speed, size and direction are in the menu.
- **Living point** - a sound that stands still slowly sways around its place (±20°, ±15% distance), so it never feels like a nail in the air.
- **Behind sounds behind** - the further a sound goes behind your head, the softer its highs, the way your ears and the back of your head shape real sound.
- **Audiobooks** - open files or a whole folder; the player remembers your position in every chapter.
- **Internet radio** - add any direct `https://` stream, or **scan**: stations of your country (by time zone), the whole world or any other country from the open radio-browser.info catalog, each one checked automatically for 3D. Stations that don't allow processing still play in plain stereo.
- **Several sounds at once** - besides the main player, up to four extra sources (radio, files, a whole folder as a playlist, a browser tab on desktop). Each has its own color, place, orbit and volume; tap its circle above the radar or its dot on the radar to move it.
- **Hearing setup** - a front/back contrast slider and a 10-sound blind test, because generic 3D audio does not fit every pair of ears.
- **Demo for first visitors** - one tap plays a melody built right in the browser and sends it orbiting around your head.
- **Sleep timer, speed 1-1.5×, radar lock** (locked at start, so the page scrolls), and a **3D off** switch to compare with normal stereo.
- **Skins** that change the whole player (Drone HUD, Watch, Classic '99) - a skin is a JSON file you can save, edit and share.
- **10 languages**, picked automatically from your device.
- **Installable app (PWA)**, works offline for local files.
- **Sound scene studio** ([`studio.html`](studio.html)) - drop in your own clips, place them around the head, play them by tapping or as a numbered scenario, mark voices so everything else steps back while they speak. Made for recording demo videos.

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

## One radar, three voices: Player, Companion, Call

Wisp is not only a player. It is a small system that gives every sound stream its own place around your head. Three tabs switch only the top of the screen; the radar below is shared:

- **Player** - music, audiobooks, radio.
- **Companion** - a personal voice AI on your shoulder, built on Gemini Live. You bring your own free Gemini API key: it is stored only in your browser and goes straight to Google. It can search Google, knows the date and (if you allow) where you are, and remembers past conversations as short summaries kept on your device.
- **Call** - voice calls by link (`wispplayer.com/?call=…`), up to 4 people, no accounts. Every voice is its own dot on the radar; tap a person and move their voice anywhere. Built on WebRTC; the server in [`call-server/`](call-server/) only introduces the phones to each other and relays audio when a direct connection is impossible (coturn).

All of them can play at once, each as its own dot: radio orbiting behind you, the companion on your right shoulder, a friend ahead on the left.

**Music yields to voices.** When the companion or someone in the call speaks, the music does not stop - it steps back (at least 2.5 m) and gets quieter, then returns when they are done. Like turning to a friend in a café instead of switching the café off.

**Pocket mode** keeps the microphone alive for the companion and for calls: the screen stays on but fully black, touches are ignored, and you exit with a 2-second hold.

The old addresses `/call.html` and `/ai.html` now simply redirect into the player.

## Ideas for the future

*Published openly on 6 October 2026, so anyone can build on them and nobody can lock them up.*

- **Spoken notifications with a place.** A native Android companion app (Notification Listener access) turns each incoming notification into one short spoken line - who and what - played from a fixed place around the head chosen per source (for example, messages at the left shoulder, e-mail at the right). Whatever is playing is not paused: it moves away to at least 2.5 m and gets quieter, and comes back when the line ends; spoken content such as an audiobook pauses instead and resumes about 2 seconds earlier. The listener answers by voice («read it», «mark as read», «delete», «reply») and the app presses the notification's own action buttons. Importance (sender, app) maps to distance: important voices come closer.
- **Priority by distance as an audio-focus model.** Instead of the usual «duck or pause» when two apps want the ears, every stream gets a place; the less important stream moves back in space rather than being muted. Music steps back, speech pauses.
- **«Talk to me» gesture.** A tap or double tap on the earbuds (media keys) addresses the AI companion; the rest of the time its microphone stays closed, so it never answers what you say to someone else.
- **Soft head tracking.** When head orientation is available (AR/VR glasses, WebXR, earbuds that expose it), quick head movements shift the sources in the world - which gives the brain its front/back cue - while the whole scene slowly re-centres to the head within 1-3 seconds, so «the shoulder» stays the shoulder while walking.
- **Sector wandering in 3D.** The sphere around the head is split into 8 sectors (front/back × left/right × up/down); a source wanders inside its sector instead of standing still - the «living point» extended to height.

## Honest limitations

- **Headphones required.**
- **Everyone hears differently.** Left/right works for everyone; some people confuse ahead/behind with generic HRTF. Moving sources help, and it tends to get easier with practice.
- **Head-locked by design.** The sound turns with your head - the companion is part of you, not part of the room.
- **Radio:** 3D works only if the station allows cross-origin access (CORS); otherwise it plays in stereo.
- **Fast orbits** can make some people slightly dizzy after a few minutes.
- **Companion and call at the same time** both listen to your microphone, so the companion may answer what you say to your friend. A «talk to me» gesture (for example, a tap on the earbuds) is planned.
- **Screen off:** music keeps playing, but Android takes the microphone away from a web page when the screen locks - that is what pocket mode is for.

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

Всё работает на встроенном в браузер Web Audio, файлы никуда не уходят. Wisp - это не только плеер, а система, где у каждого звука своё место на одном общем радаре. Три вкладки: **Плеер** (музыка, книги, радио), **Попутчик** - голосовой ИИ на плече (Gemini Live, со своим бесплатным ключом) и **Звонок** - разговор по ссылке, где каждый собеседник - своя точка вокруг головы. Всё может звучать одновременно, а когда кто-то говорит, музыка не выключается, а отходит назад и становится тише.

**Личный слой, а не окно в другой мир.** VR и отслеживание головы привязывают звук к миру - чтобы заменить реальность. Wisp - наоборот: прозрачный купол между тобой и миром, как шлем или платок. Звуки живут на его поверхности и идут вместе с тобой. Внутри купола расстояние означает близость, как между людьми: у уха - сообщения и попутчик, рядом - книга, в комнате - музыка, вдали - дождь и город. Поэтому «музыка уступает» не тише, а дальше. Экран так не умеет: огромный телевизор или монитор перед глазами - всё равно одна плоскость, окна и вкладки можно только сложить стопкой, а «ближе-дальше» - только нарисовать. На слух расстояние чувствуется сразу и без усилий, а звуки на разных расстояниях не заслоняют друг друга.

**Спокойная технология, а не погружение.** Atmos, игры и кино уводят из реальности в выдуманную сцену - поле боя, пустыню, космос, - и для этого нужно сидеть и представлять. На улице такая картинка в ушах спорит с тем, что видят глаза. Wisp не изображает другое место: он только раскладывает звуки вокруг, а реальность остаётся главной. Это то, что Марк Вайзер и Джон Сили Браун ещё в 1990-х назвали «спокойной технологией»: она живёт на краю внимания и выходит в центр, только когда нужно. Поэтому в дороге - никаких пещер и полей боя по умолчанию, только места и расстояния. Атмосферу каждый включает сам, когда реальность можно отпустить: на беговой дорожке или дома с закрытыми глазами.

**Идеи на будущее** (опубликованы 6 октября 2026 года, подробно - в английском разделе «Ideas for the future»): уведомления голосом, у каждого источника своё место вокруг головы, при этом остальной звук не выключается, а отходит назад, книга встаёт на паузу, а ответ голосом нажимает кнопки уведомления; приоритеты расстоянием как замена обычному «приглушить или остановить»; жест «говорю с тобой» для ИИ; мягкое слежение за головой; блуждание звука по 8 секторам сферы.

Отзывы и идеи - в Telegram [@WispPlayer_bot](https://t.me/WispPlayer_bot).
