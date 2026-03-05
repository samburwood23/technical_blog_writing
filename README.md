---
title: Technical Blog Writing Assistant
emoji: ✍️
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# Technical Blog Writing Assistant

A RAG-powered chatbot that helps engineers write better technical blog posts.

Built on the blog templates, prompting guides, and common pitfalls in this repo. Ask it anything about structure, tone, openings, metrics, code examples, or which template to use.

## Setup (for local dev)

```bash
pip install -r requirements.txt
HF_TOKEN=your_token python app.py
```

## Deploying to HF Spaces

1. Create a new Space at huggingface.co/new-space (SDK: Gradio)
2. Push this repo to it: `git remote add space https://huggingface.co/spaces/<username>/<space-name>`
3. Add your `HF_TOKEN` as a Space secret (Settings → Variables and secrets)
4. Push: `git push space claude/expand-prompting-examples-75CAs:main`
