# LinkedIn Post: Adding Visuals to the Live Coding Kit

**Follows:** [A Practical Guide to Live Coding Music with Strudel and TidalCycles](live-coding-algorave-kit.md)
**Repo:** https://github.com/samburwood23/live_coding (patterns 60–73)
**Attach:** the 17-second clip of pattern 71 (New Monkey V, "Bells") in projector mode, with the levelled audio

---

Howay. My live coding kit makes visuals now, and they move with the beat. The clip is a New Monkey tune I wrote in code. 🐒

If you grew up in the North East in the early 2000s, you'll know the New Monkey. If you didn't: it was a club in Sunderland with its own sound. Take makina from Spain, make it bouncier, add a bassline that jumps an octave on every offbeat, pianos and a pitched-up vocal hook, and run it at about 170 BPM.

You didn't need to go to hear it, either. Tapes and CDs of the sets went round every car, bus and school yard from Blyth to Hartlepool, copies of copies. Yes, it was in Sunderland. Every Geordie who went has made their peace with that.

So the kit has seven New Monkey tunes of my own, built up layer by layer in code. This week I gave each one a light show.

The visuals use Hydra, a browser video synth that's live coded in the same way. The best part is one function, H(). It takes the same pattern notation that drives the music and turns it into a value for the visuals:

shape(H("<3 4 5 6>"))   → a new shape on every chord
.scale(H("[1.5 1 1 1]*4"))   → a jump on every kick

There's no audio analysis and no beat detection. The visuals and the music read from the same clock, so they can't drift apart. In the clip, the stars' size, number and spin all come from patterns like that, so they change on the same bar as the tune.

Three things I had to fix along the way:

1. Strudel and Hydra both draw on full-screen canvases that covered the editor. I moved them behind it and gave each line of code a dark backing so it stays readable.
2. Hydra keeps running after you press Stop or switch patterns. Strudel doesn't clear it, so the old visuals lingered. Now the kit clears it on both.
3. 15px code is unreadable from a dancefloor. Projector mode goes full screen with just the code at 24px over the visuals. Esc exits.

It runs in a browser, with nothing to install. Have a gan: https://github.com/samburwood23/live_coding

And if you've still got a Monkey CD in the glovebox, I want to hear about it in the comments.

#LiveCoding #CreativeCoding #Strudel #Hydra #NorthEast #Newcastle #JavaScript
