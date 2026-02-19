# Refinement and Editing Prompts

Use these prompts *after* you have a first draft. They're designed to be applied to specific sections, not the whole post at once. Working section by section gives you more control and produces better results than asking the AI to "make the whole thing better".

---

## Table of Contents

- [Structural Improvements](#structural-improvements)
- [Clarity and Readability](#clarity-and-readability)
- [Technical Depth](#technical-depth)
- [Code Examples](#code-examples)
- [Opening and Closing](#opening-and-closing)
- [Audience Calibration](#audience-calibration)
- [Tone and Voice](#tone-and-voice)
- [Length Reduction](#length-reduction)

---

## Structural Improvements

### Add a Clearer Problem Statement

```
The opening of this blog doesn't make the problem concrete enough. A reader who skims the first paragraph should immediately know:
1. What was broken or missing
2. Who was affected
3. Why it mattered

Here is my current opening:
[Paste current opening]

Rewrite it to front-load the problem. Start with the symptom or the user impact, not the background.
```

### Improve Section Flow

```
These two sections feel disconnected — the reader jumps from [Section A] to [Section B] without a clear link.

[Paste the two sections]

Add a 1–2 sentence transition that:
- Closes the thought from Section A
- Sets up why Section B follows logically

Don't add padding — the transition should carry information, not just be a signpost.
```

### Add a Missing "So What?" to a Section

```
This section describes what we did but doesn't explain why it matters to the reader.

[Paste the section]

After the technical explanation, add 2–3 sentences answering: "So what? What should the reader do with this information? When would they apply this?"
```

### Restructure for Skimmability

```
This section is a dense block of prose. Engineers who are troubleshooting or learning often skim.

[Paste the section]

Restructure it so a reader can get the key point in 10 seconds by skimming. Options:
- Break into a bulleted list if items are parallel
- Use a table if comparing options
- Add a callout box for the single most important point
- Use a numbered list if there's a sequence

Choose the format that best matches the content type, and apply it.
```

---

## Clarity and Readability

### Simplify a Dense Technical Paragraph

```
This paragraph is technically accurate but hard to follow on first read. It tries to explain too much at once.

[Paste the paragraph]

Rewrite it by:
1. Splitting into shorter sentences (aim for ≤25 words per sentence)
2. Moving the most important point to the first sentence
3. Using an analogy or concrete example if the concept is abstract

Keep all the technical content — just make the path through it clearer.
```

### Replace Jargon With Plain Language

```
This section uses jargon that readers outside our team might not know.

[Paste the section]

For each of these terms, either define it inline (in parentheses) or replace it with plain language:
- [Term 1]
- [Term 2]
- [Term 3]

Don't over-explain concepts that are genuinely assumed knowledge for our audience — only the ones listed above.
```

### Make an Abstract Concept Concrete

```
This explanation is accurate but abstract. A reader can follow the words but can't picture what's actually happening.

[Paste the section]

Add a concrete example that illustrates the concept. The example should:
- Use our actual tech stack (Python/FastAPI/PostgreSQL/Kubernetes)
- Be something a team member would recognise from their own work
- Take no more than 3–5 lines of code or 2–3 sentences of prose

Don't replace the abstract explanation — add the example after it.
```

---

## Technical Depth

### Add Context Around Why We Chose This Approach

```
This section explains what we did but not why we chose it over alternatives. Readers who face the same decision need the reasoning, not just the answer.

[Paste the section]

Add a short paragraph explaining:
1. What we considered doing instead (1–2 alternatives)
2. Why we rejected them (be specific — "it was too slow" is less useful than "it added 400ms to our P99 at our request rate")
3. The main trade-off we accepted with our chosen approach

Keep it to 3–5 sentences — this is a footnote, not another section.
```

### Add Failure Modes and Edge Cases

```
This section makes the approach look clean and problem-free. It needs to be honest about when it breaks down.

[Paste the section]

Add a callout (use a > blockquote with a ⚠️ prefix) covering:
- The scenario where this approach stops working
- The warning signs that you're approaching that limit
- What to do when you hit it

Base this on real limits: [paste any relevant constraints, benchmarks, or known issues from your notes].
```

### Expand a Thin Explanation

```
This explanation is too brief — it tells the reader what to do but not enough about how or why.

[Paste the section]

Expand it to cover:
1. The mechanism — what is actually happening under the hood?
2. A concrete working example with code
3. The specific behaviour to watch for in production

Target: 150–250 words for this section. Don't pad — add substance.
```

---

## Code Examples

### Add Comments to Complex Code

```
This code example is correct but the non-obvious parts aren't explained.

[Paste the code]

Add inline comments to:
- Any line where the "why" isn't obvious from the code itself
- The first occurrence of any pattern that recurs
- Any line that differs meaningfully from the "obvious" way to write it

Don't comment things that are self-explanatory (e.g., don't add `# open file` above `open(file)`).
```

### Add a "Before" to an "After" Example

```
This code example shows the solution but not the problem it replaces. Without the before, readers can't assess whether their own code has the same issue.

THE AFTER CODE:
[Paste the solution code]

THE PROBLEM IT SOLVES:
[Describe what was wrong with the original, or paste the original code]

Write a side-by-side before/after example with:
- The problematic code first, with a comment explaining what's wrong with it
- The improved code after, with a comment explaining what changed and why
- A one-sentence summary of the key difference
```

### Simplify an Overly Complex Example

```
This code example is doing too many things at once. A reader seeing this for the first time will be overwhelmed.

[Paste the code]

Simplify the example by:
1. Removing anything that isn't directly relevant to the concept being demonstrated
2. Replacing real infrastructure details (hostnames, ports, credentials) with obvious placeholders
3. Adding a comment at the top listing what's been simplified: "# Simplified: assumes X, Y, Z — see [link] for production setup"

Target: ≤20 lines for a concept example, ≤50 lines for a real-world example.
```

### Add Error Handling to an Example

```
This code example is clean but doesn't show what happens when things go wrong. Readers will copy this code and wonder why it's silent on errors.

[Paste the code]

Add appropriate error handling that:
- Catches the specific exceptions that are likely (not bare `except Exception`)
- Logs a useful message (what went wrong + enough context to debug)
- Either retries if that makes sense, or raises with a clear error message

Use our standard error handling pattern: [describe your team's convention, or paste an example].
```

---

## Opening and Closing

### Strengthen the Opening Paragraph

```
The current opening is factual but doesn't give the reader a reason to keep reading.

CURRENT OPENING:
[Paste current first paragraph]

Rewrite the opening using one of these approaches (pick the most appropriate):
1. Start with the moment the problem became undeniable — the alert, the incident, the user complaint
2. Start with the counterintuitive finding — "We assumed X. We were wrong."
3. Start with the direct value proposition — "If you've ever spent 3 hours debugging X, this post will save you that time"

The opening should make a reader think "yes, that's exactly my situation" or "I didn't know that was possible".
```

### Write a Stronger Conclusion

```
The current conclusion summarises what we did but doesn't give the reader a next step.

CURRENT CONCLUSION:
[Paste current conclusion]

Rewrite the conclusion to:
1. Summarise the key takeaway in one sentence (not a full recap)
2. Give the reader one concrete next action ("if you want to try this, start by...")
3. Open a question or suggest a follow-up angle ("we're now exploring whether this approach also works for...")
4. Invite feedback ("have you solved this a different way? We'd love to know in the comments")

Keep it to 3–5 sentences.
```

### Write Multiple TL;DR Versions

```
Write three versions of the TL;DR for this post:

THE POST:
[Paste the full post or a summary]

VERSION 1 (2 sentences): For someone deciding whether to read the post
VERSION 2 (1 sentence): For a Slack message sharing the link
VERSION 3 (tweet-length): For an external audience

For each version, focus on the most surprising or actionable thing in the post. Don't just describe the topic — tell them what they'll get from reading it.
```

---

## Audience Calibration

### Adjust for a Less Experienced Audience

```
This post is written for experienced engineers on our team. I also want it to be accessible to newer engineers (6–18 months experience).

[Paste the section that needs adjustment]

Revise this section by:
1. Adding a one-sentence plain English explanation before the technical one
2. Linking to a foundational resource for any concept a new hire might not know: [list the concepts]
3. Replacing undefined acronyms: [list any in the section]

Don't dumb it down — just add on-ramps so someone newer can follow along without losing the depth for experienced readers.
```

### Adjust for an External Audience

```
I want to publish this externally (company blog / dev.to / etc.). The current version assumes internal knowledge.

[Paste the section or full post]

Revise it to be self-contained for an external reader:
1. Replace internal system names with generic descriptions: [list: "checkout-api" → "our checkout service", etc.]
2. Remove references to internal tooling that can't be linked: [list them]
3. Add 1–2 sentences of company context where needed: [paste approved description of our company/team]
4. Flag any metrics or architecture details that need approval before external publication: [list any you're unsure about]
```

---

## Tone and Voice

### Remove Marketing Language

```
Some of this language sounds like marketing copy rather than engineering writing.

[Paste the section]

Replace any of the following patterns:
- Superlatives without evidence ("dramatically", "incredibly", "revolutionary") → specific measurements
- Passive voice hiding who did what → active voice
- Hedging that undermines the message ("kind of", "sort of", "might possibly") → direct statements
- Corporate filler ("in order to", "it is important to note that") → delete or rephrase

Keep the technical accuracy — only change the tone.
```

### Make the Writing More Direct

```
This section buries the lead. The most important point appears in the third paragraph.

[Paste the section]

Rewrite it using the "inverted pyramid" structure:
1. Most important point first (what the reader needs to know)
2. Supporting detail second
3. Background and context last

A reader who stops after the first paragraph should still understand the key takeaway.
```

---

## Length Reduction

### Cut a Section by 30%

```
This section is longer than it needs to be. I want to cut it by approximately 30% without losing technical accuracy.

[Paste the section — target: [X] words currently, aiming for [Y] words]

Cut by:
1. Removing sentences that restate something already said
2. Removing background that the audience already knows
3. Combining short sentences that cover the same point
4. Cutting examples down to the most illustrative one if there are multiple similar ones

Show me the reduced version and a brief note on what was cut and why.
```

### Identify What to Cut

```
This draft is [X] words and needs to be under [Y] words. Rather than cutting randomly, I want to cut the least valuable content.

[Paste the full draft]

Analyse the draft and recommend:
1. The 2–3 sections or paragraphs that contribute least to the core message
2. Any repeated explanations that could be merged
3. Any examples that duplicate each other

Don't make the cuts yet — just tell me what to consider cutting and why, so I can make the final call.
```
