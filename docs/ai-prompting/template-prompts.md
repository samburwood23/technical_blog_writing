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

**If the business impact section is vague:**
```
The business/engineering impact in "The Challenge" section is too vague — "it caused problems"
isn't enough to help a reader decide whether this post is relevant to them.

Here are the actual consequences we experienced:
[paste: SLA breaches, customer complaints, engineering hours lost, revenue impact, error rates, etc.]

Rewrite the impact section using these specific details. If we have numbers, use them. If we
only have qualitative data, describe the concrete events: the page at 2am, the support escalation,
the sprint disruption — not just "it was bad".
```

**If the lessons learned section feels generic:**
```
The "Lessons Learned" section reads like general engineering advice rather than something
specific to what we went through.

Here's what we actually learned — including where our assumptions were wrong:
- We initially thought [X] was the cause. We were wrong because [Y].
- The fix that seemed obvious ([Z]) didn't work because [reason].
- If we faced this again, we'd [specific change to our approach].
- We'd add [specific alert / test / code pattern] to catch this earlier.

Rewrite the lessons section using these specific details. Each lesson should be traceable
back to something that actually happened in this incident.
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

**If the "why we adopted this tool" section is missing or thin:**
```
The post jumps straight into how to use [tool] without explaining why we chose it over what we
were doing before. Readers need this context to judge whether they should adopt it too.

Here's our actual adoption story:
- What we were doing before [tool]: [describe the previous solution or absence of one]
- The specific pain point that triggered evaluation: [the incident, the scaling wall, the dev complaint]
- Other tools we briefly considered and why we didn't choose them: [list + reason]
- The moment we decided to proceed: [the POC result, the benchmark, the recommendation]

Write a "Why We Adopted [Tool]" section (200–300 words) using these details. It should read
like a decision record, not a product testimonial.
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

**If the lessons learned section is too brief or obvious:**
```
The lessons learned section is either too short or lists things any engineer would already know.
The most useful lessons from a refactoring are the ones specific to what we found in *this* codebase.

Here are the specific things we'd do differently or watch for in future code reviews:
- [Specific pattern in the original code that we now know to catch early]
- [Something we assumed would be easy that turned out to be hard, and why]
- [A decision we made during the refactor that we're still uncertain about]
- [A thing we wanted to refactor but deliberately left alone, and when we'd revisit it]

Rewrite the lessons section with these specific points. Each lesson should finish with a
practical implication: "so now we [specific practice / review habit / code pattern]".
```

**If the metrics table is missing or uses vague improvements:**
```
The results section claims the refactor was successful but the evidence is thin.

Here are the actual measurements we took before and after:
BEFORE:
- [Metric: e.g., test run time, cyclomatic complexity, lines of code, error rate]
- [Value + how measured]

AFTER:
- [Same metric]
- [Value + how measured]

Build a results table using these numbers. For any metric where we don't have exact numbers,
flag it with [ESTIMATED] and note how we arrived at the estimate. Don't invent numbers.
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

**If the decision context doesn't give enough constraints:**
```
The "Decision Context" section describes what we needed but not the constraints that shaped
our evaluation. Without these, readers from different teams may over-apply our findings.

Our actual constraints were:
- Scale: [e.g., requests per second, data volume, number of services]
- Team: [e.g., team size, existing expertise, ramp-up time available]
- Timeline: [e.g., had to ship in X weeks]
- Budget/cost: [e.g., licence cost, operational cost considerations]
- Existing dependencies: [e.g., already using X, so Y integrates better]

Add a "Constraints That Shaped Our Evaluation" subsection listing these. Then add a "What
Would Change Our Recommendation" paragraph: if [constraint] were different, we'd have chosen
[the other option] instead. This is the part that makes the post useful to teams with different contexts.
```

**If the "what would change our decision" section is missing:**
```
This post documents what we chose but doesn't say when a different team should make a different choice.

Our actual position is:
- We'd choose [Tech B] instead if: [condition — e.g., team is smaller, data volume is lower,
  latency requirements are looser, cost is the primary constraint]
- We'd revisit our decision if: [future change — e.g., Tech B releases feature X, our scale
  changes by Y, we hire someone with expertise in Z]
- We explicitly didn't consider [factor] because [reason] — a team where that matters should weight it differently

Write a "When You Should Choose Differently" section (150–200 words) making our position honest
and useful to teams with different constraints. This is not a disclaimer — it's the most
team-independent value in the whole post.
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

**If the prevention section is too generic:**
```
The "Prevention" section says things like "add monitoring" and "improve your config management"
without any specifics. An engineer reading this section after an incident wants to know exactly
what to add, not that they should add something.

Here's what we actually added or changed after this incident:
- [Specific alert: name, threshold, what it catches]
- [Specific code pattern or guard that prevents recurrence]
- [Specific config change or validation we added]
- [Runbook or playbook link we created]

Rewrite the Prevention section with these specific additions. For each item include:
1. What to add (the exact alert query, code snippet, or config setting)
2. Where it goes (which service, which config file, which monitoring dashboard)
3. What it catches (the specific failure mode it would have detected earlier)
```

**If the escalation section is incomplete:**
```
The escalation section is missing the information an on-call engineer needs to decide
*when* to escalate vs. keep investigating independently.

Add:
1. The specific signals that mean "stop investigating and escalate now":
   [e.g., issue has persisted > 30 minutes, affecting > X% of traffic, data loss risk]
2. The exact team or rotation to contact: [e.g., @team-sre via PagerDuty P1, not Slack]
3. What information to have ready before escalating:
   [e.g., error rate graph URL, pod logs from the last 30 minutes, last deployment time]
4. What NOT to do while waiting: [e.g., don't restart pods without SRE sign-off if data is at risk]
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

**If the profiling and investigation tools section is thin:**
```
The investigation section mentions that we "used a profiler" but doesn't explain the process
well enough for another engineer to replicate it. The methodology is often more reusable than
the specific fix.

Here's what we actually did to investigate:
1. [First tool and command: e.g., "ran py-spy top --pid $(pgrep -n gunicorn)"]
2. [What it showed: paste actual output or describe key finding]
3. [Second tool and command]
4. [What it showed: and what made us look at the real bottleneck]
5. [The moment we identified the actual bottleneck: what the data showed]

ACTUAL PROFILER OUTPUT:
[Paste your profiler output, flamegraph description, EXPLAIN ANALYZE result, or metrics screenshot description]

Rewrite the investigation section using these exact steps and outputs. A reader should be able
to follow this process on their own system. Include the actual commands, not pseudocode.
```

**If the effort vs. impact framing is missing:**
```
The optimisation strategy lists what we changed but not how we prioritised. Readers doing their
own performance work need to know the effort/impact tradeoffs, not just the final list.

For each optimisation we made:
[Fill in this table from your notes]

| Change | Engineering effort | Performance impact | How we knew it worked |
|--------|-------------------|-------------------|----------------------|
| [Change 1] | [hours / days] | [% improvement in which metric] | [measurement method] |
| [Change 2] | ... | ... | ... |

Rewrite the "Optimisation Strategy" section organising changes by this effort/impact framing.
Group into: Quick Wins (< 1 day, measurable impact), Structural Changes (> 1 week, high impact),
and Fine-Tuning (low effort, small gains). For each group, explain why we did them in this order.
```
