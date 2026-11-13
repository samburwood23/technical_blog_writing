# LinkedIn Post: Adding Visuals to the Live Coding Kit

**Follows:** [A Practical Guide to Live Coding Music with Strudel and TidalCycles](live-coding-algorave-kit.md)
**Repo:** https://github.com/samburwood23/live_coding (patterns 60–73)
**Attach:** the 17-second clip of pattern 71 (New Monkey V) in projector mode, with the levelled audio

---

My live coding kit makes music. Now it makes visuals too, and they move with the beat.

At an algorave the performer's code is projected behind them. So I added a projector mode and some visuals to sit behind the code.

The visuals use Hydra, a browser video synth that's live coded in the same way. The best part is one function, H(). It takes the same pattern notation that drives the music and turns it into a value for the visuals:

shape(H("<3 4 5 6>"))   → a new shape on every chord
.scale(H("[1.5 1 1 1]*4"))   → a jump on every kick

There's no audio analysis and no beat detection. The visuals and the music read from the same clock, so they can't drift apart. In the clip, the stars' size, number and spin all come from patterns like that.

You don't need Strudel to use Hydra, though. It runs on its own at hydra.ojack.xyz, which is handy if you play music from something else, like TidalCycles, a DJ deck or a band. Without H(), you sync it one of two ways:

bpm = 174
shape([3, 4, 5, 6], 0.35)   → steps through the list at the tempo you set
.scale(() => 1 + a.fft[0])   → reacts to the bass through your microphone

Setting the tempo keeps it on the beat until you drift out of time. Listening through the mic follows whatever's playing, but it reacts a moment late, and a loud crowd can set it off. Running both in one tab with Strudel avoids that trade-off.

Three things I had to fix along the way:

1. Strudel and Hydra both draw on full-screen canvases that covered the editor. I moved them behind it and gave each line of code a dark backing so it stays readable.
2. Hydra keeps running after you press Stop or switch patterns. Strudel doesn't clear it, so the old visuals lingered. Now the kit clears it on both.
3. 15px code is unreadable from a dancefloor. Projector mode goes full screen with just the code at 24px over the visuals. Esc exits.

There are 14 new patterns. They include a scrolling pianoroll, a feedback tunnel that zooms on the kick, and seven full tracks with a scene per section, timed to change on the same bar as the music.

It runs in a browser, with nothing to install: https://github.com/samburwood23/live_coding

#LiveCoding #CreativeCoding #Strudel #Hydra #Algorave #JavaScript
