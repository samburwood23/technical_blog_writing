# Common Pitfalls in Technical Blog Writing

The [blog templates](../readme.md#blog-style-templates) show you what good looks like. This doc
shows what bad looks like — the patterns that make posts fall flat even when the underlying work
was genuinely interesting.

---

## Finding Topics Worth Writing About

The hardest part for most engineers isn't writing — it's knowing which experiences are worth
documenting. A few reliable signals:

| Signal | Blog type |
|--------|-----------|
| You explained the same thing twice on Slack | Tool Deep Dive or Debugging Guide |
| An incident retrospective exists | Debugging Guide or Problem-Solution Case Study |
| A PR description grew into an essay | Refactoring Story or Problem-Solution Case Study |
| A decision kept resurfacing in planning sessions | Technology Comparison |
| A bug took more than a day to find | Debugging Guide |
| An optimisation surprised you with where the bottleneck actually was | Performance Story |
| "I wish someone had told me this when I started" | Tool Deep Dive |
| You tried three approaches before finding one that worked | Problem-Solution Case Study |

If you have to invent a hypothetical to make your topic concrete, it's not ready. Real experience
is what separates a useful internal post from a blog post that reads like public documentation.

---

## Anti-Patterns to Avoid

### 1. The Documentation Dump

**What it looks like:** A release note, ADR, or internal design doc reformatted as a blog post
with headers and bullet points but no narrative or decisions explained.

**Why it fails:** Readers feel like they're reading a spec. There's no story, no tension, no
"we tried X and it didn't work because Y". The post describes what was built but not why or what
it cost to get there.

**Fix:** Ask "what would I tell a colleague over lunch about this work?" That's your blog post.
The doc is just reference material; the post is the story of the decisions.

---

### 2. The Tutorial That Isn't

**What it looks like:** A post walking through a technology's features with code examples —
but without sharing a real decision, a failure, or anything the official docs don't already cover.

**Why it fails:** If the reader could find everything in it on the official docs page, the post
adds no value. It has no point of view and no experience embedded in it.

**Fix:** A good internal post answers "why *we* use this" and "what *we* learned that isn't
obvious". Pick the one thing the official docs gloss over and make that the centre of the post.

---

### 3. The Missing Middle

**What it looks like:** The post moves from "we had this problem" directly to "here's the
solution" in two paragraphs, as if the solution was obvious once the problem was stated.

**Why it fails:** The most valuable part of a case study is the investigation — the wrong
hypotheses, the failed attempts, the moment the real cause became clear. Without this,
readers can't apply the same reasoning to their own problems.

**Fix:** Write the investigation like a detective story. What made you look at X first? Why
was that wrong? What did you look at next? What evidence shifted your thinking? The messy
middle is the teachable content.

---

### 4. The Generic Conclusion

**What it looks like:** The lessons section ends with "always test your assumptions",
"performance matters", "invest in observability", or "communication is key".

**Why it fails:** If the lesson applies to every engineering project ever undertaken, it
provides no information. It signals that you didn't extract the actual specific learning
from the specific experience.

**Fix:** Each lesson should be traceable back to a specific moment in the project. "We
should have run EXPLAIN ANALYZE before assuming the index was being used" is a lesson.
"Profile before optimising" is a textbook.

---

### 5. The Weak Opening

**What it looks like:** The post opens with "In this blog post, I will explain..." or
three paragraphs of background before getting to why the reader should care.

**Why it fails:** Engineers scan. A reader who isn't hooked in the first few sentences
will skip to the code or close the tab. Starting with meta-commentary ("this post covers")
or slow context-setting loses them before they reach the interesting part.

**Fix:** Start in the middle of the problem. "At 2am on a Tuesday, our checkout service
was returning 503s to 30% of users. The cause took us 6 hours to find and 10 minutes to
fix." That's a hook. The background can come in paragraph two.

---

### 6. The Unmarked Opinion

**What it looks like:** Presenting a team decision, preference, or context-specific
conclusion as an objective technical fact.

> "PostgreSQL is better than MongoDB for this use case."
> "You should always use connection pooling."
> "Kubernetes is overkill for small services."

**Why it fails:** These statements are true under specific conditions and false under others.
Stating them without qualification damages credibility with readers who know the nuance,
and misleads readers who don't.

**Fix:** Mark your opinions and constraints explicitly. "For our use case (high-write,
complex queries, existing Postgres expertise), we found Postgres significantly easier to
operate than Mongo. Teams with different constraints may reach a different conclusion."

---

### 7. The Incomplete Code Example

**What it looks like:** A code block that calls undefined helpers, references unshown
config, imports non-standard internal modules, or would throw an error if copy-pasted.

```python
# Example of what NOT to do
result = process_order(order_id, config=get_internal_config())  # where does get_internal_config come from?
validate_and_publish(result, topic=CHECKOUT_TOPIC)  # CHECKOUT_TOPIC is never defined
```

**Why it fails:** Readers trying to apply the example can't tell what's essential and
what's specific to your environment. They give up or implement it wrong.

**Fix:** Either make examples fully self-contained and runnable (add the imports, the
constants, the dependencies), or clearly mark what's environment-specific with a comment:

```python
# Assumes: DATABASE_URL env var set, order_events Kafka topic exists
# See: internal docs link for setup
result = process_order(order_id, db_url=os.environ["DATABASE_URL"])
```

---

### 8. The Abstract Example

**What it looks like:** Code using `foo`, `bar`, `doSomething()`, `MyClass`, `process()`.

**Why it fails:** Abstract names make it harder to see the pattern. The example reads like
it came from a textbook rather than a real system, which makes it harder to apply to
real code. It also signals that the author didn't trust the reader to handle real context.

**Fix:** Use realistic names from your domain. `process_checkout_event()` communicates
the same pattern as `process()` while also telling the reader something about when to
use it. If real names are sensitive, use plausible domain names, not placeholders.

---

### 9. The Hedge Spiral

**What it looks like:** Every claim is qualified to the point where no guidance is
actually communicated.

> "This approach might work for some teams, though of course it depends on your specific
> context. You should evaluate whether this is right for your situation. Your mileage may
> vary, and there are many ways to approach this problem."

**Why it fails:** The reader finishes the post knowing nothing actionable. The hedging
signals either uncertainty in the author's position or a fear of being wrong. Both
undermine the post's usefulness.

**Fix:** Be direct, then scope your claim. "We use this approach for all services with
> 100 RPS. Below that threshold, the operational overhead isn't worth it." That's specific,
useful, and honestly scoped — without hedging everything into mush.

---

### 10. The Buried Lede

**What it looks like:** The most interesting finding — the counterintuitive result, the
surprising root cause, the number that changed the team's assumptions — appears in the
fifth or sixth section of the post.

**Why it fails:** Engineers scan. If the most interesting thing in the post is buried past
the headers a reader doesn't recognise as relevant, they won't reach it.

**Fix:** Surface the most interesting finding early — in the TL;DR, in the introduction,
or as a callout near the top. Let readers know what's interesting before asking them to
read the full explanation of how you got there.

---

### 11. The Asymmetric Comparison

**What it looks like:** A technology comparison that lists the strengths of the chosen
technology alongside the weaknesses of the rejected one, without honest coverage of both.

**Why it fails:** Readers who know the technology space immediately lose trust in the
author. The post reads as post-hoc rationalisation, not genuine evaluation.

**Fix:** Apply the same lens to both options. For each criterion, describe the best case
for each technology, then explain why your constraints broke the tie. If you're struggling
to articulate the genuine strengths of the option you didn't choose, you probably didn't
evaluate it fairly.

---

### 12. Metrics Without Method

**What it looks like:**

> "We improved performance by 60%."
> "The refactor reduced our error rate significantly."
> "Build times are much faster now."

**Why it fails:** A number without a measurement method is an anecdote. 60% improvement
in what metric? P50 or P99? Under what load? Measured how? Over what time period? Without
the method, the number can't be reproduced, challenged, or compared against.

**Fix:** Always pair a metric with its method:

| Metric | Before | After | Measurement method |
|--------|--------|-------|--------------------|
| API P99 latency | 2,400ms | 380ms | Datadog APM, 7-day rolling average, production traffic |
| Build time | 8m 42s | 3m 15s | CI run time, median over 50 builds, same runner type |

If you can't state the measurement method, the number isn't ready to publish.

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
- [ ] Would a reader who skims the headers and the first sentence of each paragraph still
      understand the core message?
