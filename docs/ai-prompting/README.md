# AI-Assisted Technical Writing Guide

This folder contains prompts and guidance for using AI tools (Claude, ChatGPT, Gemini, etc.) to accelerate your technical blog writing. The goal is not to replace your expertise — it's to handle the blank-page problem and the first-draft grind so you can focus on accuracy, tone, and the knowledge only you have.

## What's in This Folder

| File | What It's For |
|------|--------------|
| [template-prompts.md](./template-prompts.md) | Ready-to-use prompts for generating first drafts of each blog template type |
| [refinement-and-editing.md](./refinement-and-editing.md) | Prompts for improving, expanding, and polishing drafts |

## How AI Fits Into the Writing Process

```
Your knowledge + notes
        ↓
  AI generates draft      ← template-prompts.md
        ↓
  You review + fill gaps
        ↓
  AI refines sections     ← refinement-and-editing.md
        ↓
  Technical peer review
        ↓
  Published
```

AI is fast at structure, transitions, and common explanations. You are irreplaceable for:
- The actual technical details and code
- Whether the explanation is accurate
- Knowing which edge cases matter to your team
- The "war stories" — the failed attempts, the surprising findings

---

## General Principles for Good AI Prompts

### 1. Give Context, Not Just Instructions

The more context you provide, the less generic the output.

| Less useful | More useful |
|-------------|-------------|
| "Write a blog about fixing a bug" | "Write a blog about the connection pool exhaustion bug we fixed in checkout-api. Background: [paste your notes]" |
| "Explain how we use Docker" | "Explain our Docker setup for a new hire who knows Python but has never used containers" |

### 2. Specify Your Audience Precisely

- "Our team" → assumes familiarity with our stack (Python, FastAPI, Postgres, AWS, Kubernetes)
- "Other internal teams" → needs our stack explained; knows general software concepts
- "New hires (6 months experience)" → needs foundational concepts linked
- "External / public" → no internal jargon; everything must be self-contained

### 3. Paste Your Raw Notes

AI is much better at turning bullet points into prose than it is at inventing accurate technical details. Before prompting:

- Dump your notes, Slack messages, PR descriptions, incident retrospective
- Paste the actual error messages and stack traces
- Include the "before" and "after" code snippets

### 4. Iterate, Don't Regenerate

A bad first draft isn't a prompt failure — it's the start of a conversation. Use [refinement-and-editing.md](./refinement-and-editing.md) to steer the AI toward what you need, section by section.

### 5. Always Verify Technical Content

AI can confidently produce plausible-sounding but subtly wrong technical explanations. Treat the output as a first draft, not a source of truth. Your technical review step is non-negotiable.

---

## Quick-Start Prompt

If you want a quick first draft without reading the full prompting guide, use this:

```
You are helping me write a technical blog post for our engineering team.

CONTEXT:
- Topic: [what you solved or built]
- Template type: [Problem-Solution / Tool Deep Dive / Refactoring / Comparison / Debugging / Performance]
- Target audience: [our team / other teams / new hires]
- Our stack: Python, FastAPI, PostgreSQL, AWS (ECS + RDS), Kubernetes
- Approximate length: 1,200 words

MY NOTES:
[Paste everything you know: bullet points, error messages, code snippets, what you tried, what worked]

Please write a first draft following the structure of the [template type] template. Use the notes above for all technical details — do not invent facts. Flag any section where you need more information from me with [NEEDS INPUT].
```

---

## Model-Specific Tips

### Claude

- Works well with long context — paste your full notes, PR description, and retrospective all at once
- Responds well to "think step by step before writing" for complex technical explanations
- Ask it to "identify any technical claims you're uncertain about" at the end of a draft

### ChatGPT (GPT-4)

- Good at restructuring and shortening verbose drafts
- Use the "custom instructions" feature to set your team's stack as persistent context
- Works well for generating multiple alternative introductions to choose from

### Gemini

- Strong at summarising long documents (useful for turning incident retrospectives into blog posts)
- Ask it to "cite specific sections of my notes" to reduce hallucination risk

---

## When NOT to Use AI

- **For the metrics and measurements** — always use real numbers from your monitoring tools
- **For security-sensitive content** — don't paste internal credentials, hostnames, or customer data into AI tools
- **For the final code examples** — AI-generated code can have subtle bugs; always test it yourself
- **As a substitute for peer review** — AI doesn't know whether your approach was actually the right one for your system
