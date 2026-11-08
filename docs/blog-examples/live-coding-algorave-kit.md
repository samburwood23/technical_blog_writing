# A Practical Guide to Live Coding Music with Strudel and TidalCycles

**Author:** Sam Burwood
**Tags:** live-coding, creative-coding, javascript, haskell, audio, developer-tools
**Template:** Tool / Technology Deep Dive
**Versions covered:** Strudel (`@strudel/repl` 1.3.0), TidalCycles 1.10, SuperDirt v1.7.4, SuperCollider 3.13
**Reading time:** ~9 minutes
**Repo:** [github.com/samburwood23/live_coding](https://github.com/samburwood23/live_coding)

---

## TL;DR

> Live coding is making music by writing and editing code while it plays, often in front of an audience who can see your screen. TidalCycles is the language most of the algorave scene uses, and Strudel is its JavaScript port that runs in a browser tab. I built a small kit with both: a browser version you can run in two minutes, and a native setup that took me most of a day to get working on Ubuntu. **The surprise was that the hard part wasn't learning the language. It was the Linux audio stack.** If you're curious, start in the browser and only go native when you have a reason to.

---

## What Live Coding Actually Is

Here is a complete piece of music:

```js
setcps(0.55)

s("bd*4, ~ cp ~ cp, hh*8")
  .bank("RolandTR909")
```

That's a four-to-the-floor kick, claps on beats 2 and 4, and eighth-note hi-hats on a TR-909. Press `Ctrl+Enter` and it loops. Now change `hh*8` to `hh*16` and press `Ctrl+Enter` again. The hats double, **on the next cycle, without the music stopping**.

That's the whole idea. You don't compose a track and then press play. The code is the instrument, and editing it is how you play it. At an algorave the performer's screen is projected behind them, so the audience watches the code change as they hear it.

For an engineer, the closest thing is a REPL with a very short feedback loop. You write an expression, evaluate it, and get the result back in your ears a fraction of a second later.

---

## The Two Tools

### TidalCycles (the original)

[TidalCycles](https://tidalcycles.org) is a pattern language written as a Haskell library. You write patterns in a text editor, the editor sends them to a `ghci` session running Tidal, and Tidal sends timed messages over OSC to SuperDirt, a sampler and synth engine that runs inside SuperCollider:

```
editor ──(Ctrl+Enter)──▶ Tidal (ghci) ──OSC :57120──▶ SuperDirt (SuperCollider) ──▶ speakers
```

That's four moving parts: a Haskell toolchain, an editor plugin, an audio server and your operating system's sound system.

### Strudel (the browser port)

[Strudel](https://strudel.cc) is a port of Tidal's pattern engine to JavaScript. It runs in a browser tab, uses the Web Audio API for sound and loads samples over HTTP. There's nothing to install. The same idea looks almost the same in both:

```haskell
-- Tidal
d1 $ s "bd*4, ~ cp ~ cp, hh*8"
```

```js
// Strudel
s("bd*4, ~ cp ~ cp, hh*8")
```

---

## Why It's Worth an Engineer's Evening

- **It's the tightest feedback loop you'll find.** Most of us wait seconds to minutes for a build or test run. Here an edit is audible within a cycle, which is about two seconds at jungle tempo.
- **It makes you think in transformations, not instructions.** You don't write "play a kick at 0.0s, 0.5s, 1.0s". You describe a pattern and then apply functions to it: `every 4 (fast 2)`, `sometimesBy 0.3 (# speed 2)`, `jux rev`. It's functional programming you can hear.
- **Mistakes are cheap and audible.** A bad edit sounds wrong for one cycle and you fix it. That's a good environment for learning a new syntax.

**Good fit if you:**
- Like REPLs, functional composition or music, or ideally all three
- Want a creative side project you can finish an evening with something to show
- Already know a little JavaScript (for Strudel) or Haskell (for Tidal)

**Not a good fit if you:**
- Want to produce polished, mixed tracks. A DAW like Ableton or Logic is a much better tool for that.
- Need precise control over sound design. Live coding trades fine control for speed of change.
- Aren't willing to debug your OS audio setup, if you go native on Linux (more on that below)

---

## Getting Started in the Browser (2 Minutes)

The browser kit is a single `index.html` with a pattern list and an editor. It loads Strudel's web component from a CDN, so there's no build step:

```html
<script src="https://unpkg.com/@strudel/repl@1.3.0"></script>
```

To run it:

```bash
git clone https://github.com/samburwood23/live_coding.git
```

```bash
cd live_coding && python3 -m http.server 8000
```

Open `http://localhost:8000`, pick a pattern from the sidebar and press `Ctrl+Enter`. Use a local server rather than opening the file from disk, because browsers restrict some audio features on `file://` pages.

The kit has 17 starter patterns. The first ten teach the basics (mini-notation, layering, an acid bassline, polyrhythms, Euclidean rhythms, chords). The last seven are jungle styles, from amen rollers to drill'n'bass.

---

## Core Concepts

### 1. Everything is a cycle

Tidal and Strudel don't think in seconds or bars. They think in **cycles**, and every pattern in quotes is squeezed into one cycle. `"bd sd"` is two steps of half a cycle each. `"bd sd hh cp"` is four steps of a quarter cycle each. Tempo is set in cycles per second, so to get BPM you divide:

```js
setcps(170/60/4) // 170 BPM, 4 beats per cycle
```

> **Gotcha:** this tripped me up for the first hour. Adding steps to a pattern doesn't make it longer; it makes every step shorter. If you want something to last two cycles, use `.slow(2)` or the `<a b>` alternation syntax.

### 2. Mini-notation does most of the work

The string inside `s("...")` is a small language of its own. These cover about 90% of what I write:

| Syntax | Meaning | Example |
| --- | --- | --- |
| `a b c` | Divide the cycle into equal steps | `s("bd sd hh")` |
| `~` | Rest | `s("bd ~ sd ~")` |
| `*n` | Repeat | `s("hh*8")` |
| `[a b]` | Group steps into one step | `s("bd [sd sd]")` |
| `<a b>` | Play one per cycle, in turn | `s("bd <sd cp>")` |
| `a, b` | Play at the same time | `s("bd*4, hh*8")` |
| `(k,n)` | Euclidean rhythm: k hits spread over n steps | `s("bd(3,8)")` |

### 3. Transformations are what make it live

A static loop gets boring fast. Functions that change a pattern over time are what keep it moving without you touching it:

```js
n("0 2 4 <5 7> 4 2")
  .scale("D3:dorian")
  .s("gm_lead_2_sawtooth")
  .every(4, x => x.rev())                      // reverse every 4th cycle
  .sometimesBy(0.3, x => x.add(note(12)))      // up an octave, 30% of the time
  .jux(x => x.fast(2))                         // right channel plays double speed
```

### 4. Chopping breaks

This is the heart of jungle and the most satisfying thing in either tool. `splice` cuts a sample into slices and stretches each slice to fit its step, so a break always fits your tempo however fast it was recorded:

```js
setcps(170/60/4)

s("brk")
  .splice(16, "0 1 2 3 4 5 [6 6] 7 0 1 10 11 [12 13] 14 4 15")
  .lastOf(4, x => x.ply(2))   // a roll on every 4th bar
  .cut(1)                     // each slice cuts off the previous one
```

Reading the pattern: play slices 0–5 in order, double slice 6, then jump back to 0 and 1, skip ahead, and so on. Rewriting that string while it plays is what "live coding a jungle set" mostly means.

---

## Going Native: TidalCycles on Ubuntu

The browser is enough to learn with. I went native because SuperDirt has a much bigger sample library, built-in synths like `superreese` and `superhoover`, tighter timing, and the editor integration most performers use.

The kit's `tidal/` folder has an install guide, a one-command Ubuntu installer, a SuperDirt startup file and two sets (jungle and makina). The install itself is four steps: SuperCollider and `sc3-plugins` from apt, SuperDirt from SuperCollider's package manager, Haskell via GHCup, then `cabal install tidal --lib`. The guide estimates 30–45 minutes, most of it compiling Tidal.

It took me a lot longer than that. The git history is a fair record of where the time went: after the commit that added the install guide, the next two are both troubleshooting sections.

### What actually broke, and the fixes

| Symptom | Root cause | Fix |
| --- | --- | --- |
| `cabal update` fails: *root.json does not have enough signatures* | Ubuntu's packaged `cabal` (3.8) is too old to verify Hackage's current signing keys | Don't install `ghc`/`cabal-install` from apt. Use GHCup. |
| `no synth or sample named 'superreese'` | `supercollider` was installed without `sc3-plugins`, so SuperDirt silently skips all its `super*` synths | `sudo apt install sc3-plugins` |
| Server fails to boot: `jackdmp … could not initialize audio` | SuperCollider started a real JACK server, which tried to take the sound card from PipeWire (the default on Ubuntu 22.10+) | Start it through PipeWire's JACK layer: `pw-jack scide` |
| `Variable not in scope: d1` / `(#)` / `s` in the editor | The editor's `ghci` was Ubuntu's, not GHCup's, so Tidal wasn't installed for it | Remove the apt GHC, or point the editor's **Ghci Path** at `~/.ghcup/bin/ghci` |
| `SuperDirt installed` printed, then `SuperDirt` is an unknown class | SuperDirt moved to codeberg.org. When that download fails, the package manager still prints "installed". | Check the files actually arrived and fall back to the GitHub mirror |

That last one is my favourite, because the fix is a pattern I'd use anywhere: don't trust the installer's success message, check for the thing you needed. The kit's `install_superdirt.scd` does exactly that:

```supercollider
var ok = { File.exists(dir +/+ "SuperDirt.quark") };

Quarks.install("SuperDirt", version);

if(ok.value.not) {
    "Could not reach codeberg.org, installing from the GitHub mirror.".postln;
    Quarks.uninstall("SuperDirt");
    Quarks.install("https://github.com/musikinformatik/SuperDirt.git", version);
};
```

The install script ends the same way. Instead of "Done!", it checks each component and prints a ✓ or a ✗ with the command that fixes it:

```
==> Checking everything
  ✓ SuperCollider
  ✓ sc3-plugins
  ✓ SuperDirt
  ✓ Dirt-Samples
  ✓ Tidal
  ✓ Realtime audio limits
```

One more that looks scarier than it is: `Couldn't set realtime scheduling priority`. It's a warning, not an error. SuperCollider still makes sound, but timing can stutter under load. The fix is to add yourself to the `audio` group, enable realtime limits with `sudo dpkg-reconfigure jackd2`, and **log out and back in**. Group changes only apply to new logins, which I forgot the first time.

### A small quality-of-life fix

Tidal's tempo is in cycles per second, which nobody thinks in. The kit's `BootTidal.hs` adds two helpers:

```haskell
-- Tempo in BPM (4 beats per cycle): bpm 172
let bpm b = setcps (b / 60 / 4)

-- Chop a break so it always fits one cycle: d1 $ brk 16 "0 1 [2 3] 4" "breaks165"
let brk slices pat sample = splice slices pat $ s sample
```

---

## Playing a Set

Once it works, a performance is mostly a file of blocks that you evaluate one at a time, top to bottom, editing as you go. The makina set in the kit is laid out like a DJ set: intro, groove, riff, hoover, breakdown, build and drop.

The build is the most interesting bit of code in the repo. It's a snare roll that speeds up over four bars and then **brings the kick and bass back by itself** on bar five, so your hands are free at the drop:

```haskell
do
  d7 $ qtrigger $ seqP [ (0, 2, s "sn*4"), (2, 3, s "sn*8"), (3, 3.5, s "sn*16"), (3.5, 4, s "sn*32") ]
    # n 7 # speed (slow 4 $ range 1 1.8 saw) # gain 1.05 # orbit 6
  d1 $ qtrigger $ seqP [ (4, 100000, s "hardkick*4" # n 1 # cut 1 # shape 0.3 # orbit 0) ]
```

`seqP` schedules patterns over ranges of cycles, and `qtrigger` makes cycle 0 mean "the next bar" rather than "when Tidal started". The snare pitch rises over the four bars because `speed` is driven by a slow sawtooth.

---

## Strudel vs. TidalCycles

| | Strudel | TidalCycles |
| --- | --- | --- |
| Setup time | None: open a URL | 30–45 minutes if it goes well, longer on Linux if it doesn't |
| Language | JavaScript (method chaining) | Haskell (operators like `$` and `#`) |
| Sounds | Web Audio synths, General MIDI soundfonts, samples loaded over HTTP | SuperDirt: hundreds of sample banks and SuperCollider synths |
| Timing | Good; depends on the browser tab staying in focus | Tighter, with configurable latency and realtime priority |
| Sharing | Send a URL | Share a `.tidal` file; the other person needs the full stack |
| Editor | Built-in, in the browser | Your own (VS Code, Pulsar, Vim, Emacs) |

**My recommendation:** start with Strudel. You'll learn the pattern language, which is 90% of the skill, and it carries straight over to Tidal. Move to Tidal when you want SuperDirt's sounds, tighter timing for a gig, or to play from your own editor. If you're on Ubuntu, use GHCup instead of apt for Haskell, install `sc3-plugins` from day one, and start SuperCollider with `pw-jack`. Those three things would have saved me most of the day.

---

## Further Reading

- [Strudel workshop](https://strudel.cc/workshop/getting-started/): the best first hour
- [TidalCycles documentation](https://tidalcycles.org) and the [Tidal Club forum](https://club.tidalcycles.org)
- [Sonic Pi](https://sonic-pi.net): a Ruby-based alternative with a very friendly built-in tutorial
- [algorave.com](https://algorave.com) and [toplap.org](https://toplap.org): find events and streams
- [The kit](https://github.com/samburwood23/live_coding): 17 Strudel patterns, the Ubuntu installer, and jungle and makina sets for Tidal

*If you try it, I'd love to hear what you make. Drop a Strudel link in the comments.*

---

## LinkedIn Post (to share the article)

> I spent a weekend learning to make jungle music by writing code while it plays.
>
> It's called live coding. You write a pattern, press Ctrl+Enter, and edit it while it loops. The changes land on the next bar, so the music never stops. At an algorave the performer's screen is projected behind them.
>
> Three things I learned:
>
> 1. The browser version (Strudel) takes two minutes to start. The native one (TidalCycles + SuperCollider) took most of a day on Ubuntu, and none of it was the language. It was Hackage signing keys, a missing plugins package and PipeWire fighting JACK for the sound card.
> 2. It's functional programming you can hear. You don't schedule notes; you describe a pattern and transform it: reverse it every 4 bars, double the speed in one ear, chop a breakbeat into 16 slices and reorder them.
> 3. Never trust an installer that says "installed". One package manager printed success after its download had failed. The fix was to check that the files actually arrived.
>
> I wrote up a guide with a starter kit: 17 browser patterns, a one-command Ubuntu installer, and a jungle set.
>
> [link to article]
>
> #LiveCoding #CreativeCoding #TidalCycles #Strudel #Algorave

---

### Publishing Checklist

- [x] Version numbers stated in the header
- [x] Code examples taken from the kit at the stated versions
- [x] "Not a good fit" section included
- [x] Pitfalls section covers the issues actually hit (from the repo's troubleshooting commits)
- [ ] Check the "spent a weekend" / "most of a day" wording matches your actual experience
- [ ] Add a screenshot of the browser kit or a short screen recording with audio (LinkedIn favours video)
- [ ] Technical review
