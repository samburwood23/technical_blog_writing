# Common Pitfalls in Technical Blog Writing

The [blog templates](../readme.md#blog-style-templates) show you what good looks like. This doc
shows what bad looks like — the patterns that make posts fall flat even when the underlying work
was genuinely interesting.

---

## Finding Topics Worth Writing About

The hardest part for most engineers isn't writing — it's knowing which experiences are worth
documenting. Reliable signals:

- Explained the same thing twice on Slack → **Tool Deep Dive or Debugging Guide**
- An incident retrospective exists → **Debugging Guide or Problem-Solution Case Study**
- A PR description grew into an essay → **Refactoring Story or Problem-Solution Case Study**
- A decision kept resurfacing in planning → **Technology Comparison**
- A bug took more than a day to find → **Debugging Guide**
- An optimisation surprised you with where the bottleneck was → **Performance Story**
- "I wish someone had told me this when I started" → **Tool Deep Dive**
- You tried three approaches before finding one that worked → **Problem-Solution Case Study**

> If you have to invent a hypothetical to make your topic concrete, it's not ready.

---

## Anti-Patterns to Avoid

### 1. The Documentation Dump

- **Symptom:** Reads like a release note or ADR reformatted with headers — no story, no decisions explained
- **Why it fails:** Describes *what* was built but not *why* or what it cost to get there
- **Fix:** Ask "what would I tell a colleague over lunch?" — that's the post; the doc is reference material

---

### 2. The Tutorial That Isn't

- **Symptom:** Walks through a technology's features but adds nothing beyond the official docs
- **Why it fails:** No point of view, no real experience — readers can find it elsewhere
- **Fix:** Focus on what *your team* learned that isn't obvious; make that the centre of the post

---

### 3. The Missing Middle

- **Symptom:** Jumps from "we had this problem" directly to "here's the solution" in two paragraphs
- **Why it fails:** The wrong hypotheses and failed attempts are the most reusable part — readers can't apply the reasoning without them
- **Fix:** Write the investigation like a detective story — what you checked first, why it was wrong, what finally shifted your thinking

---

### 4. The Generic Conclusion

- **Symptom:** Lessons section ends with "always test your assumptions" or "invest in observability"
- **Why it fails:** If the lesson applies to every engineering project ever, it carries no information
- **Fix:** Every lesson must be traceable back to a specific moment in *this* project — "we should have run EXPLAIN ANALYZE before assuming the index was being used" is a lesson; "profile before optimising" is a textbook

---

### 5. The Weak Opening

- **Symptom:** Opens with "In this blog post, I will explain..." or several paragraphs of background
- **Why it fails:** Engineers scan — a reader who isn't hooked in the first few sentences won't reach the interesting part
- **Fix:** Start in the middle of the problem; put the hook first and the background second

---

### 6. The Unmarked Opinion

- **Symptom:** Team preferences or context-specific decisions presented as objective technical facts
  - *e.g. "PostgreSQL is better than MongoDB" / "Kubernetes is overkill for small services"*
- **Why it fails:** True under some conditions, false under others — damages credibility with readers who know the nuance
- **Fix:** Mark opinions explicitly and scope the conditions: "For our use case... teams with different constraints may reach a different conclusion"

---

### 7. The Incomplete Code Example

- **Symptom:** Code calls undefined helpers, imports internal modules, or would throw an error if copy-pasted
- **Why it fails:** Readers can't tell what's essential vs. environment-specific; they give up or implement it wrong
- **Fix:** Either make examples fully self-contained, or mark dependencies explicitly: `# Assumes: DATABASE_URL set, order_events topic exists`

---

### 8. The Abstract Example

- **Symptom:** Code uses `foo`, `bar`, `doSomething()`, `MyClass`, `process()`
- **Why it fails:** Abstract names make the pattern harder to see and signal it came from a textbook, not a real system
- **Fix:** Use realistic domain names — `process_checkout_event()` teaches the same pattern as `process()` while showing when to use it

---

### 9. The Hedge Spiral

- **Symptom:** Every claim is qualified until no guidance is actually communicated — *"this might work for some teams, though your mileage may vary..."*
- **Why it fails:** Reader finishes knowing nothing actionable; signals either uncertainty or fear of being wrong
- **Fix:** Be direct, then scope — "we use this for all services above 100 RPS; below that the overhead isn't worth it"

---

### 10. The Buried Lede

- **Symptom:** The most interesting finding — the counterintuitive result, the surprising root cause — appears in section 5 or 6
- **Why it fails:** Engineers scan; if the most interesting thing is past headers a reader doesn't recognise as relevant, they won't reach it
- **Fix:** Surface the surprising thing early — in the TL;DR, the intro, or a callout near the top

---

### 11. The Asymmetric Comparison

- **Symptom:** Technology comparison lists the chosen option's strengths against the rejected option's weaknesses
- **Why it fails:** Reads as post-hoc rationalisation; readers who know the space lose trust immediately
- **Fix:** Apply the same lens to both options — if you can't articulate the genuine strengths of what you didn't choose, you didn't evaluate it fairly

---

### 12. Metrics Without Method

- **Symptom:** "We improved performance by 60%" / "Build times are much faster now"
- **Why it fails:** A number without a measurement method is an anecdote — it can't be reproduced, challenged, or compared
- **Fix:** Always pair a metric with its method — *what* was measured, *how*, under *what conditions*, at *which percentile*

---

## Quick Self-Review Checklist

Before handing a draft to a reviewer, run through this:

- [ ] Does the opening hook a reader in the first 3 sentences?
- [ ] Does every section heading tell me what I'll learn, not just the topic name?
- [ ] Is there a concrete "what we tried first and why it failed" moment?
- [ ] Are all metrics paired with a measurement method?
- [ ] Can I copy-paste each code example and have it run, or is it clearly marked as partial?
- [ ] Is the conclusion specific to this project, or could it apply to any project ever?
- [ ] Are opinions marked as opinions, or are preferences stated as facts?
- [ ] Have I said what I'd do differently next time?
- [ ] Would a reader who skims the headers and the first sentence of each paragraph still understand the core message?
