# LinkedIn Post: Adding Visuals to the Live Coding Kit

**Follows:** [A Practical Guide to Live Coding Music with Strudel and TidalCycles](live-coding-algorave-kit.md)
**Repo:** https://github.com/samburwood23/live_coding (patterns 60–73)
**Attach:** a 30–60 second screen recording of pattern 64 or 66 in projector mode, with sound

---

My live coding kit makes music. Now it makes visuals too, and they move with the beat.

At an algorave the performer's code is projected behind them. So I added a projector mode and some visuals to sit behind the code.

The visuals use Hydra, a browser video synth that's live coded in the same way. The best part is one function, H(). It takes the same pattern notation that drives the music and turns it into a value for the visuals:

shape(H("<3 4 5 6>"))   → a new shape on every chord
.scale(H("[1.5 1 1 1]*4"))   → a jump on every kick

There's no audio analysis and no beat detection. The visuals and the music read from the same clock, so they can't drift apart.

Three things I had to fix along the way:

1. Strudel and Hydra both draw on full-screen canvases that covered the editor. I moved them behind it and gave each line of code a dark backing so it stays readable.
2. Hydra keeps running after you press Stop or switch patterns. Strudel doesn't clear it, so the old visuals lingered. Now the kit clears it on both.
3. 15px code is unreadable from a dancefloor. Projector mode goes full screen with just the code at 24px over the visuals. Esc exits.

There are 14 new patterns. They include a scrolling pianoroll, a feedback tunnel that zooms on the kick, and seven full tracks with a scene per section, timed to change on the same bar as the music.

It runs in a browser, with nothing to install: [link to repo]

#LiveCoding #CreativeCoding #Strudel #Hydra #Algorave #JavaScript
