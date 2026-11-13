# Syncing Live-Coded Visuals to Music Without Listening to It

**Author:** Sam Burwood
**Tags:** live-coding, webgl, javascript, strudel, hydra, creative-coding
**Template:** Tool / Technology Deep Dive
**Versions covered:** `@strudel/repl` 1.3.0 (bundles `@strudel/hydra` and `@strudel/draw` 1.2.6), `hydra-synth` (latest from unpkg)
**Reading time:** ~8 minutes
**Repo:** [github.com/samburwood23/live_coding](https://github.com/samburwood23/live_coding), patterns 60–73
**Follows:** [A Practical Guide to Live Coding Music with Strudel and TidalCycles](live-coding-algorave-kit.md)

---

## TL;DR

> Most music visualisers listen to the audio and react to it: run an FFT, watch the bass bin, pulse when it crosses a threshold. That's always a little late, and it can't tell a kick from a loud crowd. When the music is generated from code, you don't need to listen. Strudel's `H()` function turns a music pattern into a function that [Hydra](https://hydra.ojack.xyz) calls on every frame, so the visuals ask the music's scheduler what's happening *now* instead of guessing from the sound. This post covers how that works (it's one line of code), the two bugs I hit putting it in a page, a gotcha that throws on every frame, and how to sync Hydra when Strudel isn't making the music.

---

## The Problem With Listening

The standard way to make visuals react to music is audio analysis. Hydra supports it out of the box: `a.fft[0]` gives you the level of the lowest frequency bin from the microphone.

```js
shape(4).scale(() => 1 + a.fft[0]).out()
```

It works with any music, but it has three costs:

1. **Latency.** An FFT needs a window of samples before it can say anything, the signal gets smoothed so it doesn't flicker, and the mic adds its own buffering. The visual lands after the beat, not on it.
2. **It hears everything.** A crowd, a mic too close to the PA, or a bassline in the same band as the kick all move the same number.
3. **It only knows loudness.** The FFT can tell you *something* is loud. It can't tell you "this is the third bar of the breakdown" or "the chord just changed to G".

In my kit the music is a Strudel pattern, so the information the FFT is trying to recover already exists, exactly, in the pattern.

---

## How `H()` Works: One Line

This is the whole implementation, from `@strudel/hydra`:

```js
export const H = (p) => () => reify(p).queryArc(getTime(), getTime())[0].value;
```

Three ideas are packed in there.

**Patterns are functions of time.** A Strudel pattern isn't a list of notes. It's a function you query with a time span (an *arc*), and it returns the events that happen in that span. `reify` turns a string like `"[1.2 1 1 1]*4"` into a pattern. `queryArc(t, t)` asks for a zero-width span at the current time `t`, which returns the single event active at that instant, and `.value` is its value.

**`getTime()` is the scheduler's clock.** It's the same clock that schedules the audio, in cycles. It's not `Date.now()` and it's not the audio input.

**`H()` returns a function, not a value.** Hydra accepts a function anywhere it accepts a number, and calls it once per frame. So `H(...)` hands Hydra a closure, and every frame (60 times a second) Hydra asks the pattern "what's your value right now?"

```js
await initHydra()

shape(H("<3 4 5 6>"), 0.35, 0.02)    // a new shape on every chord
  .scale(H("[1.5 1 1 1]*4"))         // jumps on every kick, then settles
  .out()
```

`"<3 4 5 6>"` plays one value per cycle, so the shape changes on the same cycle the chord does. `"[1.5 1 1 1]*4"` is four beats with a 1.5 on each downbeat, the same rhythm as a `bd*4` kick. Because both read the same clock as the audio, they can't drift apart. There's no detection step, so there's nothing to tune and nothing to be late.

### Composing them

Because `H()` gives you a function, you can combine several with plain JavaScript. In pattern 71 the kick pulse should only appear in sections that have a kick:

```js
const kickIn = H("<1@8 1@8 1@16 1@8 0@8 1@4 1@16>")  // 1 = this section has a kick
const pulse  = H("[1.2 1 1 1]*4")
const kickPulse = () => 1 + kickIn() * (pulse() - 1)

shape(4, starSize, 0.01).scale(kickPulse).out()
```

When `kickIn()` is 0 the pulse is multiplied out to a steady 1.

### Scene changes on the bar

The full tracks (67–73) change scene when the music changes section. Each Hydra setting holds one value per section, using `@` weights so a value lasts that many cycles:

```js
// intro 8, skip bounce 8, bell riff 16, offbeat pianos 8, breakdown 8, kick roll 4, drop 16
const grid = H("<2@8 3@8 5@16 6@8 8@8 3@4 6@16>")

arrange(
  [8,  stack(kick, hats)],
  [8,  stack(kick, hats, claps, bass)],
  [16, stack(kick, hats, claps, bass, bells)],
  // ...
)
```

At 4 beats per cycle, one cycle is one bar, so `2@8` is "a 2×2 grid for the 8-bar intro".

> **Trade-off:** the bar counts live in two places, the `H()` strings and `arrange()`. Change one without the other and the visuals change scene on the wrong bar. A tidier version would build both from one list of `[bars, music, visuals]`. I haven't done that yet.

---

## Gotcha: No Rests in `H()`

Look at the end of the one-liner again: `[0].value`. If the pattern has no event at the current instant, `queryArc` returns an empty array, `[0]` is `undefined`, and `.value` throws a `TypeError`. Hydra calls the function every frame, so it throws every frame.

That's why `kickIn` above uses `0@8` for the breakdown and not `~@8`. **In `H()` patterns, use `0` (or whatever your "off" value is), never a rest.**

---

## Putting It in a Page: Two Bugs

### 1. The canvas covered the editor

Strudel's draw module creates its canvases like this (from `@strudel/draw`):

```js
canvas.style = 'pointer-events:none;width:100%;height:100%;position:fixed;top:0;left:0';
document.body.prepend(canvas);
```

`position: fixed` makes the canvas a positioned element with `z-index: auto`. The kit's header, sidebar and editor were ordinary, non-positioned elements, and in CSS stacking order positioned elements paint *above* non-positioned ones, whatever their order in the DOM. So the full-screen visuals painted over the code. `pointer-events: none` meant you could still click through it, which made it look like a rendering glitch rather than a layering one.

The fix is to make the UI positioned too, and put it on a higher layer:

```css
#hydra-canvas, #test-canvas { z-index: 0 !important; pointer-events: none; }
header, nav, main { position: relative; z-index: 1; }
```

Then make the editor background transparent, and give each line of code its own dark backing so it's readable over a bright frame:

```css
#editor-host .cm-line {
  width: fit-content;
  background: rgba(13, 13, 18, 0.72);
}
```

### 2. Visuals kept playing after Stop

Hydra runs its own `requestAnimationFrame` loop, separate from the audio scheduler. Stopping Strudel stops the sound but leaves Hydra rendering, so the last pattern's visuals stayed on screen after Stop, and when you switched patterns. The kit now calls `clearHydra()` on both:

```js
function clearVisuals() { window.clearHydra?.(); }

stopButton.onclick = () => { repl.editor?.stop(); clearVisuals(); };
```

`clearHydra()` turned out to do more than I expected:

```js
export function clearHydra() {
  if (hydra) hydra.hush();
  globalThis.s0?.clear();
  document.getElementById('hydra-canvas')?.remove();
  globalThis.speed = controls.speed;
  globalThis.shape = controls.shape;
}
```

The last two lines fix a **name collision**. Hydra puts its functions on `window`, and two of them, `shape` and `speed`, have the same names as Strudel functions (Strudel's `shape` is waveshaping distortion, Hydra's draws a polygon). Loading Hydra replaces Strudel's globals. Clearing it puts them back. Method calls like `.shape(0.6)` on a pattern are unaffected, but a bare `shape(...)` call means a different thing depending on whether Hydra is loaded.

---

## Projector Mode

At an algorave the screen is the show, and 15px code is unreadable from the back of a room. Projector mode is a CSS class plus the Fullscreen API:

```js
function setProjector(on) {
  document.body.classList.toggle('projector', on);
  if (on && !document.fullscreenElement) document.documentElement.requestFullscreen?.().catch(() => {});
  if (!on && document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
}
```

The class hides the sidebar and the help text, and sets the editor to 24px. One detail matters: pressing Esc exits full screen at the browser level *without* a `keydown` event reaching the page in some browsers, so the kit also listens for `fullscreenchange` and drops projector mode when full screen ends. Otherwise you get a full-screen layout in a normal window.

A note on resolution: `initHydra()` defaults to `pixelRatio: 1` and `pixelated: true`. On a high-DPI screen, Hydra renders at CSS-pixel resolution and lets the browser scale it up. That's a sensible trade-off for a laptop driving a projector at 60 fps, and you can raise it with `initHydra({ pixelRatio: 2 })` if your GPU has room.

---

## Running Hydra Without Strudel

Hydra doesn't need Strudel. It runs on its own at [hydra.ojack.xyz](https://hydra.ojack.xyz), which is what you want if the music comes from TidalCycles, a DJ deck or a band. Without `H()`, there are two ways to sync.

**1. A tempo clock.** In Hydra, an array argument is a sequence that steps at the global `bpm`:

```js
bpm = 174
shape([3, 4, 5, 6], 0.35).out()
```

It's tight as long as both sides agree on the tempo and started together. It doesn't know where the downbeat is, though, and nothing pulls it back if it drifts.

**2. The microphone.** Back to `a.fft`, with all three costs from the start of this post:

```js
a.setBins(4)   // fewer bins: each one covers a wider band
shape(4).scale(() => 1 + a.fft[0]).out()
```

You can mix the two: use `bpm` for the structure (shapes, colours) and the mic for the energy (size, brightness). The structure stays on the beat, and the mic only changes things where a late reaction isn't noticeable.

> **Gotcha:** inside Strudel, `initHydra()` sets `detectAudio: false` by default, so `a.fft` doesn't work there unless you pass `initHydra({ detectAudio: true })`. If the music is already a pattern, you don't need it. Use `H()` instead.

| | `H()` in Strudel | `bpm` arrays | Mic (`a.fft`) |
| --- | --- | --- | --- |
| Timing | Same clock as the audio | Tight until it drifts | Late by the analysis window |
| Knows the structure (bars, sections, chords) | Yes | Only what you write in | No |
| Works with any music | No: Strudel only | Yes, if you know the tempo | Yes |
| Affected by the room | No | No | Yes |

---

## What I'd Do Next

- **One source of truth for sections.** Generate both `arrange()` and the `H()` strings from a single list so they can't disagree.
- **A safe `H()`.** Wrap it so a rest returns a default value instead of throwing: `const Hs = (p, d = 0) => () => reify(p).queryArc(getTime(), getTime())[0]?.value ?? d;`
- **Tidal to Hydra over OSC.** For the native setup, Tidal could send its events to the browser as well as to SuperDirt, which would give Hydra the same "ask the music" timing without Strudel.

---

## Further Reading

- [Hydra documentation](https://hydra.ojack.xyz/docs/)
- [Strudel: visual feedback](https://strudel.cc/learn/visual-feedback/) (pianoroll, punchcard, scope, Hydra)
- [`@strudel/hydra` source](https://codeberg.org/uzu/strudel/src/branch/main/packages/hydra)
- [The kit](https://github.com/samburwood23/live_coding): patterns 60–73, and press **⛶ Projector**

---

## LinkedIn Post (to share the article)

> Most music visualisers listen to the audio: run an FFT, watch the bass, pulse when it's loud. It's always a bit late, and it can't tell a kick from a loud crowd.
>
> When the music is code, you don't have to listen. In Strudel, this one line syncs Hydra visuals to the music:
>
> const H = (p) => () => reify(p).queryArc(getTime(), getTime())[0].value
>
> It turns a music pattern into a function that the visuals call every frame, asking the scheduler "what's playing right now?" Same clock as the audio, so there's nothing to detect and nothing to drift.
>
> I wrote up how it works, the CSS stacking bug that put the visuals on top of my code, a name collision between Strudel's shape() and Hydra's, the gotcha that throws on every frame, and how to sync Hydra when Strudel isn't making the music.
>
> 🎥 Clip: New Monkey V, with the stars' size, number and spin all driven by the music's patterns.
>
> [link to article]
>
> #LiveCoding #CreativeCoding #WebGL #JavaScript #Strudel #Hydra

---

### Publishing Checklist

- [x] Versions stated in the header; `H()`, `clearHydra()` and `getDrawContext()` quoted from `@strudel/hydra` / `@strudel/draw` 1.2.6
- [ ] Run the standalone Hydra examples at hydra.ojack.xyz (`bpm` arrays, `a.setBins`, `a.fft`)
- [ ] Confirm the rest-in-`H()` error in the browser console (open pattern 64, change a value in an `H()` string to `~`)
- [ ] Check the Esc / `fullscreenchange` behaviour in the browser you'll demo in
- [ ] Attach the levelled clip
