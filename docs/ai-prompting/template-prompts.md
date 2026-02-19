# Template-Specific Prompts

Ready-to-use prompts for generating a first draft of each blog type. Copy the relevant prompt, fill in the `[PLACEHOLDERS]`, and paste your notes into the `MY NOTES` section.

---

## Table of Contents

- [Problem-Solution Case Study](#1-problem-solution-case-study)
- [Tool / Technology Deep Dive](#2-tool--technology-deep-dive)
- [Before / After Refactoring Story](#3-before--after-refactoring-story)
- [Technology Comparison / Evaluation](#4-technology-comparison--evaluation)
- [Debugging / Troubleshooting Guide](#5-debugging--troubleshooting-guide)
- [Performance Optimization Story](#6-performance-optimization-story)

---

## 1. Problem-Solution Case Study

**Use when:** You solved a specific technical challenge and want others to learn from your approach.

### Initial Draft Prompt

```
You are helping me write a technical blog post for our engineering team.

BLOG TYPE: Problem-Solution Case Study
TARGET AUDIENCE: [Our team / Other internal teams / New hires]
GOAL: Help readers understand how we diagnosed and fixed [problem name] so they can apply the same approach or avoid the same issue.

OUR STACK: Python, FastAPI, PostgreSQL, AWS (ECS + RDS), Kubernetes
APPROXIMATE LENGTH: 1,200–1,500 words

MY NOTES:
[Paste everything: the symptom, what you tried first, the root cause, the fix, the metrics before and after]

STRUCTURE TO FOLLOW:
1. TL;DR (2 sentences: symptom + fix)
2. The Challenge (background, what was wrong, business/engineering impact, what we tried first)
3. Root Cause (the actual cause once found)
4. Our Solution (approach rationale, step-by-step implementation with code)
5. Results (metrics table, qualitative improvements)
6. Lessons Learned (3–4 bullets, including what you'd do differently)
7. Takeaways (when to use this approach, when not to)

RULES:
- Use my notes for all technical details. Do not invent facts or metrics.
- If a section needs information I haven't provided, write [NEEDS INPUT: what you need] in that spot.
- Include the actual error messages and code from my notes, not invented examples.
- Write in a direct, practical engineering tone — no marketing language.
```

### Prompts for Weak Sections

**If the "what we tried first" section is thin:**
```
The "What We Tried First" section feels generic. Here are the actual first attempts we made:
[paste your notes on failed attempts]

Rewrite this section using these specific details. Include why each attempt failed — this is the most useful part for readers.
```

**If the root cause explanation is too abstract:**
```
The root cause explanation needs to be more concrete. A reader who hasn't seen this problem should be able to understand exactly what was happening technically.

Here's more detail: [your technical notes]

Rewrite the Root Cause section with a clear technical explanation. A simple diagram description (e.g., "imagine three services in sequence...") would help if the flow is complex.
```

**If the code examples look wrong:**
```
The code examples need to be replaced with our actual implementation. Here is the real before/after code:

BEFORE:
[paste actual before code]

AFTER:
[paste actual after code]

Rewrite the implementation section using this exact code. Add inline comments explaining the key changes. Don't modify the code — only add comments.
```

---

## 2. Tool / Technology Deep Dive

**Use when:** You've adopted a new tool and want to teach others how to use it effectively in our stack.

### Initial Draft Prompt

```
You are helping me write a technical blog post for our engineering team.

BLOG TYPE: Tool / Technology Deep Dive
TARGET AUDIENCE: [Our team / Other internal teams / New hires]
GOAL: Teach readers how to use [tool name] for [specific use case], including the gotchas and best practices we discovered.

TOOL: [Tool name, version]
OUR STACK: Python, FastAPI, PostgreSQL, AWS (ECS + RDS), Kubernetes
APPROXIMATE LENGTH: 1,500–2,000 words

MY NOTES:
[Paste: what the tool does, why we adopted it, how we installed/configured it, the core concepts, a real example from our codebase, gotchas we hit, best practices we learned]

STRUCTURE TO FOLLOW:
1. TL;DR (what the tool is + the one thing it does best + who should read this)
2. Why [tool] Matters (the pain it solves, who should/shouldn't use it)
3. Getting Started (prerequisites, installation, minimal working example — ≤20 lines)
4. Core Concepts (2–4 key concepts, each with explanation + code example + gotcha callout)
5. Real-World Project (a realistic example from our codebase with a full working example)
6. Common Pitfalls (table: pitfall → why it happens → fix)
7. Best Practices (performance, security, production tips)
8. When to Use vs. Alternatives (comparison table)

RULES:
- State the version number prominently — tool APIs change.
- The "Getting Started" minimal example must be self-contained and runnable.
- Every Core Concepts code example must include an inline comment on the most non-obvious line.
- The "not a good fit" section must be honest. If [audience] shouldn't use this tool in some scenarios, say so.
- Flag any section where you need more information with [NEEDS INPUT: what you need].
```

### Prompts for Weak Sections

**If the getting started example is too complex:**
```
The "Getting Started" minimal example has grown to [X] lines — it should be ≤20.

Reduce it to the absolute minimum that works. Move any setup steps (migrations, config loading, etc.) to a comment like:
# Assumes: postgres running, DATABASE_URL set — see [link to our setup docs]

The reader should be able to copy-paste this and see a result in under 5 minutes.
```

**If the pitfalls section is too generic:**
```
The common pitfalls section is too generic — "check your configuration" isn't useful. Here are the actual errors we hit:

[Paste the actual error messages and how you solved them]

Rewrite the pitfalls table with these specific errors. The "why it happens" column should explain the technical reason, not just say "misconfiguration".
```

**To add a comparison table:**
```
Add a "When to Use vs. Alternatives" section comparing [tool] against [Alternative A] and [Alternative B].

For each alternative, base the comparison on these notes:
- [Alternative A]: [your notes]
- [Alternative B]: [your notes]

The comparison should reflect our team's context (stack, scale, team experience) — not a generic internet comparison.
```

---

## 3. Before / After Refactoring Story

**Use when:** You improved a significant piece of code and want to document the process and outcome.

### Initial Draft Prompt

```
You are helping me write a technical blog post for our engineering team.

BLOG TYPE: Before/After Refactoring Story
TARGET AUDIENCE: [Our team / Other internal teams]
GOAL: Show how we improved [component/system], documenting the real state of the code before, the refactoring process, and the measurable improvement.

OUR STACK: Python, FastAPI, PostgreSQL, AWS (ECS + RDS), Kubernetes
APPROXIMATE LENGTH: 1,200–1,800 words

MY NOTES:
[Paste: the original code or a description of it, what was wrong with it, why we decided to refactor now, the steps we took, the final code, the before/after metrics]

BEFORE CODE:
[Paste the actual before code — don't sanitise it]

AFTER CODE:
[Paste the actual after code]

STRUCTURE TO FOLLOW:
1. TL;DR (what was broken, what you did, what improved)
2. The "Before" State (code, honest description of the problems, metrics showing the issues)
3. Why We Refactored (triggering event, business/technical drivers, what we deliberately left alone)
4. The Refactoring Process (step-by-step: characterise → extract → improve, each with before/after code)
5. Results (code metrics table, operational metrics table, developer experience improvements)
6. Lessons Learned (what you'd do differently; patterns to watch for in future code reviews)

RULES:
- The "Before" code must be the real code, not a cleaned-up strawman. Its messiness is the point.
- Include the metrics table with real numbers — "it's faster" isn't useful.
- The lessons section must include at least one thing you'd do *differently* next time.
- Flag any section where you need more information with [NEEDS INPUT: what you need].
```

### Prompts for Weak Sections

**If the before code is too sanitised:**
```
The "Before" code example looks too clean — it reads like a strawman rather than real legacy code. The whole point of this section is to show authentic complexity.

Here is the actual code: [paste the real code]

Rewrite the "Before" section with this actual code. Keep the inline comments, the TODOs, the commented-out lines — all of it. Then describe specifically what makes each part problematic, using the actual issues from the code above.
```

**If the process section jumps straight to the solution:**
```
The refactoring process section jumps from "the problem" to "the solution" without showing the intermediate steps. Readers want to see how to navigate from bad code to good code.

Our actual steps were:
1. [First thing you did, e.g., wrote characterisation tests]
2. [Second step]
3. [Third step]

Rewrite the process section showing these intermediate steps. Each step should have: what we did → why we did it in this order → the code at this intermediate stage.
```

---

## 4. Technology Comparison / Evaluation

**Use when:** Your team evaluated multiple technologies and made a decision that other teams will face too.

### Initial Draft Prompt

```
You are helping me write a technical blog post for our engineering team.

BLOG TYPE: Technology Comparison / Evaluation
TARGET AUDIENCE: [Engineering leads / Other teams facing the same decision]
GOAL: Share our evaluation of [Tech A] vs [Tech B] for [use case] so other teams can make an informed decision without repeating our research.

OUR STACK: Python, FastAPI, PostgreSQL, AWS (ECS + RDS), Kubernetes
APPROXIMATE LENGTH: 1,200–2,000 words

THE DECISION:
- Use case: [What you needed the technology for]
- Scale/constraints: [Traffic, data volume, latency requirements, team size, timeline]
- Technologies evaluated: [Tech A vX], [Tech B vX]
- Decision: We chose [Tech A/B]
- Decision date: [Date — so readers know how current this is]

MY NOTES ON EACH TECHNOLOGY:
[Paste your notes, test results, benchmarks, team feedback]

EVALUATION CRITERIA:
[List the criteria you actually used to evaluate, with their relative importance]

STRUCTURE TO FOLLOW:
1. TL;DR (what you evaluated, what you chose, one-sentence reason)
2. Decision Context (specific use case, scale, constraints, success criteria table)
3. Technologies Evaluated (for each: what it is, core strengths/weaknesses in our context)
4. Hands-On Testing (test setup description, code samples, results table)
5. Evaluation Summary (weighted criteria table)
6. Our Decision (key deciding factors, trade-offs accepted, what would change our decision)
7. Implementation Notes (brief — link to ADR)
8. Recommendations for Other Teams (when to choose each option)

RULES:
- State the decision date prominently. Technology landscapes change.
- Benchmark results must include caveats about what they do/don't represent.
- The "what would change our decision" section is mandatory — when would Tech B have won?
- Be honest about the weaknesses of the option you chose.
- Flag any section where you need more information with [NEEDS INPUT: what you need].
```

### Prompts for Weak Sections

**If the criteria aren't weighted:**
```
The evaluation criteria in the summary table aren't weighted, which makes it look like a coin flip.

Our actual priorities were:
- [Criterion 1]: High priority because [reason]
- [Criterion 2]: Medium priority because [reason]
- [Criterion 3]: Low priority because [reason]

Rewrite the evaluation summary table with these weightings, and add a brief paragraph explaining why we weighted them this way. This is the most important thing for other teams to understand — our priorities may not be their priorities.
```

**If the benchmark section lacks caveats:**
```
The benchmark section needs stronger caveats so readers don't over-interpret the results.

Add a callout box after the results table that says:
- What hardware / instance type these tests ran on
- What traffic pattern the test data represents
- What the results would look like under [different condition]
- What we didn't test (and why)

Use this phrasing pattern: "These results reflect [our specific conditions]. Your results will differ if [condition that changes the outcome]."
```

---

## 5. Debugging / Troubleshooting Guide

**Use when:** You've just resolved a difficult or recurring bug and want to save the next engineer hours of investigation.

### Initial Draft Prompt

```
You are helping me write a technical blog post for our engineering team.

BLOG TYPE: Debugging / Troubleshooting Guide
TARGET AUDIENCE: On-call engineers and anyone debugging [system name]
GOAL: Create a practical runbook so the next person who hits this problem can resolve it in minutes, not hours.

OUR STACK: Python, FastAPI, PostgreSQL, AWS (ECS + RDS), Kubernetes
APPROXIMATE LENGTH: 800–1,500 words

THE PROBLEM:
- System: [Which service/system]
- Symptom: [What the engineer sees]
- Exact error message: [Copy-paste from logs — don't paraphrase]
- Root cause: [What was actually wrong]
- Fix: [What resolved it]
- How often this recurs: [One-off / occasional / frequent]

MY NOTES:
[Paste: the incident timeline, diagnostic steps you took, commands you ran, what ruled things out, what the fix was]

STRUCTURE TO FOLLOW:
1. TL;DR (symptom + root cause + one-line fix — for 2am reading)
2. Problem Description (exact error message, when it occurs, user impact, what it is NOT)
3. Diagnostic Checklist (ordered list of checks with exact commands)
4. Common Scenarios and Fixes (one section per root cause: signs → exact fix commands → time to resolve)
5. Prevention (alerts to add, code patterns that help, config best practices)
6. Escalation (who to contact when, what info to include)

RULES:
- The TL;DR must be useful to someone with no context at 2am. It's the most important section.
- All CLI commands must be exact and tested — no pseudocode.
- The "What it is NOT" section must cover the top 2–3 false leads.
- Each scenario's fix must include a way to verify the fix worked.
- Flag any section where you need more information with [NEEDS INPUT: what you need].
```

### Prompts for Weak Sections

**If the diagnostic checklist has vague steps:**
```
The diagnostic checklist steps are too vague — "check the logs" isn't actionable at 2am.

For each step, I need:
1. The exact command to run (with the real service name, namespace, etc.)
2. What "normal" output looks like
3. What "problem" output looks like (paste actual examples from the incident)

Here are the commands I actually ran during the incident:
[Paste your commands and their output]

Rewrite the checklist using these exact commands.
```

**To add a "not this" section:**
```
Add a "What This Is NOT" section after the problem description. This is one of the most time-saving parts of a debugging guide because it rules out the obvious guesses quickly.

During this incident, we wasted time investigating:
- [Red herring 1]: [Why it seemed relevant, why it wasn't]
- [Red herring 2]: [Why it seemed relevant, why it wasn't]

Write this section explaining how to rule each one out quickly, with a specific check for each.
```

---

## 6. Performance Optimization Story

**Use when:** You completed a performance improvement and want to share the methodology and results.

### Initial Draft Prompt

```
You are helping me write a technical blog post for our engineering team.

BLOG TYPE: Performance Optimization Story
TARGET AUDIENCE: [Our team / Other teams working on similar systems]
GOAL: Share how we diagnosed and fixed performance issues in [system/feature], documenting the profiling process and methodology so others can apply it.

OUR STACK: Python, FastAPI, PostgreSQL, AWS (ECS + RDS), Kubernetes
APPROXIMATE LENGTH: 1,200–2,000 words

THE OPTIMIZATION:
- System / feature: [What you optimised]
- Performance type: [Latency / throughput / memory / build time / bundle size]
- Baseline: [The exact numbers before you started]
- Final result: [The exact numbers after]
- Timeline: [How long this took]

BOTTLENECKS FOUND AND FIXED:
[For each bottleneck: what it was, how you found it, what you changed, what it improved by]

TOOLS USED:
[List the profiling and measurement tools]

MY NOTES:
[Paste your investigation notes, profiler output, before/after code, benchmark results]

STRUCTURE TO FOLLOW:
1. TL;DR (baseline, what you changed, end result)
2. The Performance Problem (baseline metrics table, business impact, how you discovered it)
3. Investigation Process (tools used, step-by-step investigation with actual profiler output)
4. Optimization Strategy (quick wins → architectural changes → code optimizations, each with effort/impact/code)
5. Final Results (metrics table, business metrics if applicable)
6. General Principles (what you learned about performance optimization from this project)

RULES:
- Baseline metrics must include the measurement method, not just the number.
- "Surprising vs. expected findings" must be honest — what did you get wrong in your initial hypothesis?
- Each optimization must state effort, impact, and how the impact was measured.
- The "always measure first" lesson must come through clearly.
- Flag any section where you need more information with [NEEDS INPUT: what you need].
```

### Prompts for Weak Sections

**If the investigation section jumps to the fix:**
```
The investigation section goes straight from "we had a performance problem" to "here's the fix". The most valuable part of this post is the investigation methodology — how you found the bottleneck.

Here's what I actually did to investigate:
1. [First tool you ran + what it showed]
2. [Second tool + what it showed]
3. [How you identified the actual bottleneck]

Rewrite the investigation section showing this process. Include the actual profiler output (I'll paste it below). The reader should be able to follow the same steps on their own system.

PROFILER OUTPUT:
[Paste your actual profiler output, flamegraph description, or EXPLAIN ANALYZE output]
```

**If the lessons section is too generic:**
```
The "General Principles" section sounds like advice from a textbook rather than something we learned from this specific project.

Here's what we actually learned — including where we were wrong initially:
- We assumed [X] was the bottleneck. We were wrong because [Y].
- The most impactful change was [Z], which surprised us because [reason].
- If we did this again, we would [specific change to the process].

Rewrite the General Principles section using these specific learnings. Each principle should be grounded in something concrete from this project.
```
