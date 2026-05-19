# How to Use AI to Write Better Technical Blog Posts (Without Losing Your Voice)

**TL;DR:** AI tools like Claude, ChatGPT, and Gemini are genuinely useful for technical writing — but only if you prompt them correctly. The blank page and first-draft grind are where AI earns its keep. Your actual technical knowledge, the real numbers, the war stories, and the "we were wrong because…" moments? Those are yours to bring.

---

## The Problem With Most AI-Assisted Technical Writing

The typical engineer's experience with AI-assisted writing goes like this: open a chat window, type "write a blog post about the database bug I fixed", and get back something that sounds vaguely authoritative but is subtly wrong about how PostgreSQL connection pooling actually behaves. You fix the obvious errors, but the result still feels generic. It could have been written by anyone, about any system, at any company.

The tool isn't the problem. The prompting is.

AI models are not technical writers who've read your codebase. They're pattern-matchers that produce plausible prose based on what you give them. Give them nothing, get nothing. Give them your actual notes, the real error messages, the before-and-after code, and the uncomfortable admission that your first three hypotheses were wrong — and you get something worth editing.

This post is a practical guide to prompting AI tools for technical blog posts: what to give them, how to structure your requests, and how to iterate toward a draft worth publishing.

---

## The Mental Model: AI Handles Structure, You Handle Truth

Before getting into specific prompts, it helps to have a clear picture of where AI adds value and where it doesn't.

```
Your knowledge + notes
        ↓
  AI generates draft       ← prompt engineering
        ↓
  You review + fill gaps
        ↓
  AI refines sections      ← iterative editing prompts
        ↓
  Technical peer review
        ↓
  Published
```

AI is fast and competent at:
- Generating structure and section templates
- Writing transitions between ideas
- Producing common technical explanations
- Turning bullet points into readable prose
- Reformatting and shortening sections on request

You are irreplaceable for:
- The actual technical details and whether they're correct
- The real metrics — from your monitoring tools, not from AI's confident-sounding estimates
- The "war stories" — what you tried first and why it failed
- The judgment calls specific to your system, your team's constraints, your scale
- Knowing which edge cases matter

This division of labour is the key insight. When engineers try to get AI to do the second list, they end up with technically plausible but subtly wrong content that's harder to fix than a blank page.

---

## The Five Principles of Good Technical Prompts

### 1. Give Context, Not Just Instructions

The more context you provide, the less generic the output.

| Less useful | More useful |
|-------------|-------------|
| "Write a blog about fixing a bug" | "Write a blog about the connection pool exhaustion bug we fixed in checkout-api. Background: [paste notes]" |
| "Explain how we use Docker" | "Explain our Docker setup for a new hire who knows Python but has never used containers" |
| "Write about our refactoring" | "Write about how we removed 400 lines of duplicated ORM code from the billing service, triggered by a production incident where a schema change broke three independent copies of the same query" |

The difference isn't length — it's specificity. A good prompt gives the AI enough to make decisions without you.

### 2. Specify Your Audience Precisely

Who you're writing for changes everything: vocabulary, assumed knowledge, the level of explanation needed for each concept.

- **"Our team"** — assumes familiarity with your stack; no need to explain why you're using FastAPI or what ECS is
- **"Other internal teams"** — needs your stack explained; knows general software engineering concepts
- **"New hires (0–12 months experience)"** — needs foundational concepts linked or briefly explained
- **"External / public"** — no internal jargon; everything must be self-contained; scrub internal system names and hostnames

Setting the audience explicitly in your prompt prevents the AI from producing something that simultaneously over-explains async Python to your senior engineers while under-explaining why a particular AWS configuration matters.

### 3. Paste Your Raw Notes

This is the single biggest lever. AI transforms bullet points and raw notes into prose far more reliably than it invents accurate technical details from scratch.

Before you write your prompt, gather:
- Your notes, Slack messages, and PR descriptions
- The actual error messages and stack traces (copy-pasted, not paraphrased)
- The before-and-after code snippets
- The incident retrospective or ADR, if one exists
- The real numbers from your monitoring tools

Dump all of it in. AI's ability to turn raw technical material into structured prose is where it genuinely saves time. Its ability to invent plausible-sounding numbers is where it creates problems.

### 4. Iterate, Don't Regenerate

A weak first draft isn't a prompt failure — it's the start of a conversation. Asking AI to "make it better" rarely works. Telling it *specifically* what's wrong with a section and asking it to fix that thing works consistently.

Instead of: *"This doesn't feel right, can you redo it?"*

Try: *"The root cause explanation is too abstract. A reader who hasn't seen this problem should be able to understand exactly what was happening technically. Here's more detail: [paste notes]. Rewrite that section with a concrete technical explanation."*

This approach — working section by section rather than regenerating the whole draft — gives you more control and produces better output at every step.

### 5. Always Verify Technical Content

AI can confidently produce plausible-sounding but subtly wrong technical explanations. It may describe a PostgreSQL locking mechanism in terms that are mostly right but miss a detail that matters for your specific version. It may suggest a Kubernetes configuration that works in principle but not with your networking setup.

Treat AI output as a first draft from a smart generalist, not a source of truth. Your technical review step is non-negotiable, and the peer reviewer should be someone who can catch the subtle errors, not just the obvious ones.

---

## The Quick-Start Prompt

If you want a working first draft without further setup, use this:

```
You are helping me write a technical blog post for our engineering team.

CONTEXT:
- Topic: [what you solved or built]
- Template type: [Problem-Solution / Tool Deep Dive / Refactoring / Comparison / Debugging / Performance]
- Target audience: [our team / other teams / new hires]
- Our stack: [list your main technologies]
- Approximate length: 1,200 words

MY NOTES:
[Paste everything: bullet points, error messages, code snippets, what you tried, what worked]

Please write a first draft. Use the notes above for all technical details — do not invent
facts. Flag any section where you need more information from me with [NEEDS INPUT].
```

The `[NEEDS INPUT]` instruction is important. It tells the AI to be honest about gaps rather than fill them with plausible-sounding invention.

---

## Template-Specific Prompting

Different post types need different structures and different emphasis. Here's a rundown of the six most common technical blog formats and how to prompt each one effectively.

### Problem-Solution Case Study

Use when you solved a specific technical challenge and want others to learn from your approach.

**Structure to request:**
1. TL;DR (symptom + fix, two sentences)
2. The Challenge (background, what was wrong, business impact, what you tried first)
3. Root Cause (the actual cause once found)
4. Solution (approach rationale, step-by-step implementation with real code)
5. Results (metrics table with actual numbers)
6. Lessons Learned (specific to *this* incident, not generic advice)

**What usually goes wrong:** The "what we tried first" section is thin or missing. This is a mistake — the wrong hypotheses and failed attempts are the most reusable part of any post. A reader facing the same problem needs to know why the obvious explanation was wrong, not just what the right answer turned out to be.

If this section is thin, prompt specifically: *"The 'What We Tried First' section feels generic. Here are the actual first attempts: [paste your notes]. Rewrite this section with these specific details and include why each attempt failed."*

### Tool / Technology Deep Dive

Use when you've adopted a new tool and want to teach others how to use it in your context.

**Key prompt elements to include:**
- The version number (tool APIs change; a post without a version number goes stale immediately)
- Why you adopted this tool — the specific pain point that triggered the evaluation, not "we needed a better solution"
- The common errors you actually hit, copy-pasted from your terminal

**What usually goes wrong:** The getting-started example grows to 50 lines and is no longer minimal. A minimal example should be ≤20 lines, fully self-contained, and copyable in under five minutes. Everything else — migration setup, config loading, production configuration — belongs in a comment pointing to your setup docs.

### Before / After Refactoring Story

Use when you improved a significant piece of code and want to document the process.

**Critical rule:** The "before" code must be the real code, not a cleaned-up strawman. Its messiness is the entire point of the section. If the before code looks like a reasonable implementation that someone made a sensible simplification for, readers won't understand why it needed refactoring.

Include the inline comments, the TODOs, the commented-out lines — all of it. Then describe specifically what makes each part problematic.

### Technology Comparison / Evaluation

Use when your team evaluated multiple technologies and made a decision that other teams will face too.

**The part most comparisons get wrong:** They document what you chose but not when a different team should choose differently. The "what would change our decision" section is mandatory. Your scale, timeline, existing expertise, and budget shaped your evaluation — teams with different constraints may legitimately reach a different conclusion, and a useful post tells them when that applies.

Also: always include the decision date. Technology landscapes change, and a reader needs to know whether your evaluation was done last quarter or three years ago.

### Debugging / Troubleshooting Guide

Use when you've just resolved a difficult bug and want to save the next engineer hours of investigation.

**The TL;DR rule:** Write the TL;DR as if it will be read at 2am by someone already stressed. It needs to be useful to a person with no context who is staring at an alert. That means: exact symptom, root cause, one-line fix. Not "there was a connectivity issue" — the actual error message and the command that fixed it.

**The "What This Is NOT" section:** One of the most time-saving things you can include. During the incident you probably wasted time chasing red herrings. Document those, explain why they seemed relevant, and explain the specific check that rules each one out. This section prevents the next person from repeating your wrong turns.

### Performance Optimization Story

Use when you completed a performance improvement and want to share the methodology and results.

**The common failure mode:** Jumping straight from "we had a performance problem" to "here's the fix". The most valuable part of a performance post is the investigation methodology — how you found the bottleneck, what you checked first, what the profiler output showed, what made you look in the right direction.

For each optimisation, include:
- **Effort:** hours or days of engineering time
- **Impact:** percentage improvement in which specific metric
- **Method:** how the impact was measured

"We made it faster" is not a useful lesson. "Adding an index on `(user_id, created_at)` reduced P99 latency from 480ms to 22ms on the user activity feed endpoint, measured with k6 against production data volume" is a lesson someone can apply.

---

## Prompting for Refinement

Once you have a first draft, targeted refinement prompts are more effective than asking for a general rewrite. Here are the most useful patterns:

### When the opening is weak

```
The current opening is factual but doesn't give the reader a reason to keep reading.

CURRENT OPENING:
[paste]

Rewrite it using one of these approaches:
1. Start with the moment the problem became undeniable — the alert, the incident, the complaint
2. Start with the counterintuitive finding — "We assumed X. We were wrong."
3. Start with the direct value proposition — "If you've ever spent 3 hours debugging X,
   this post will save you that time"
```

### When a section is too abstract

```
This explanation is accurate but abstract. A reader can follow the words but can't
picture what's actually happening.

[paste section]

Add a concrete example that uses our actual tech stack. Take no more than 3–5 lines of
code or 2–3 sentences of prose. Don't replace the abstract explanation — add the example after it.
```

### When the lessons section is generic

The most common failure in a "Lessons Learned" section is writing things that apply to every engineering project ever: "invest in observability", "always test your assumptions", "communicate early". These carry no information.

```
The "Lessons Learned" section reads like general advice.

Here's what we actually learned — including where our assumptions were wrong:
- We initially thought [X] was the cause. We were wrong because [Y].
- The fix that seemed obvious ([Z]) didn't work because [reason].
- If we faced this again, we'd [specific change to approach].

Rewrite using these specific details. Each lesson should be traceable back to
something that actually happened.
```

### When the draft is too long

```
This draft is [X] words and needs to be under [Y] words.

Analyse the draft and recommend:
1. The 2–3 sections or paragraphs that contribute least to the core message
2. Any repeated explanations that could be merged
3. Any examples that duplicate each other

Don't make the cuts yet — tell me what to consider cutting and why, so I can
make the final call.
```

---

## Model-Specific Notes

### Claude

Works well with long context — paste your full notes, PR description, and retrospective at once rather than feeding them in pieces. Ask it to "identify any technical claims you're uncertain about" at the end of a draft to surface potential accuracy issues before your technical review.

### ChatGPT (GPT-4)

Good at restructuring and shortening verbose drafts. Use the custom instructions feature to set your team's stack as persistent context — this removes the need to repeat your environment in every prompt.

### Gemini

Strong at summarising long documents, which makes it useful for turning incident retrospectives or long PRs into a blog post foundation. Ask it to "cite specific sections of my notes" in the output to reduce the risk of it drifting from your actual content.

---

## What AI Can't Do (and Where Engineers Get Into Trouble)

**For the metrics:** Always use real numbers from your monitoring tools. AI-generated numbers will be plausible-sounding and wrong. A post that says "we improved P99 latency by 40%" when your actual improvement was 12% damages your credibility with the first reader who goes to check.

**For the final code examples:** AI-generated code can have subtle bugs. Test every example yourself before publishing, especially anything involving concurrency, error handling, or external services.

**For the post-hoc rationalisation check:** AI will write a confident, well-structured rationale for whatever decision you made. It won't tell you whether the decision was actually correct or whether you evaluated the alternatives fairly. That's what peer review is for.

**For security-sensitive content:** Don't paste internal credentials, hostnames, architecture diagrams, or customer data into AI tools. The convenience isn't worth the risk.

---

## A Quick Self-Review Before You Publish

Before sending a draft to a reviewer, run through this:

- [ ] Does the opening hook a reader in the first three sentences?
- [ ] Does every section heading tell me what I'll learn, not just the topic?
- [ ] Is there a concrete "what we tried first and why it failed" moment?
- [ ] Are all metrics paired with a measurement method and measurement conditions?
- [ ] Can I copy-paste each code example and have it run, or is it clearly marked as partial?
- [ ] Is the conclusion specific to this project, or could it apply to any project ever?
- [ ] Are opinions marked as opinions, not stated as universal facts?
- [ ] Have I said what I'd do differently next time?
- [ ] Would a reader who skims the headers and the first sentence of each paragraph still get the core message?

---

## The Bottom Line

AI-assisted technical writing works when you treat the AI as a fast first-drafter and editor, not as a subject matter expert. Your job is to bring the raw material — the notes, the error messages, the real numbers, the wrong turns — and to verify that what comes out the other end is technically accurate.

The blank page problem is real and AI solves it well. The "I spent a day on this and the result is generic and slightly wrong" problem is also real, and it's almost always a prompting problem, not a model problem.

Give AI what it needs. Keep what's yours.
