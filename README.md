# ✦ Quill — AI Design Generator

> Describe any design in plain English. Quill uses Claude AI to generate
> a pixel-perfect HTML design you can download as a PNG instantly.
> Built with Duck Framework — pure Python, no JavaScript frameworks.

---

## What is this?

Quill is an AI-powered design tool. You type a prompt like:

> *"A neon cyberpunk music festival poster for Lagos, Nigeria"*

Quill sends that prompt to Claude, which generates a complete HTML design.
You watch the design build itself live in the preview panel as Claude streams
the response token by token. Then you resize it and download it as a PNG.

---

## Installation

### Step 1 — Install dependencies
```bash
pip install duckframework anthropic
```

### Step 2 — Add your API key
Open `web/settings.py` and replace `"your-api-key-here"` with your key.
Or use an environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Step 3 — Run
```bash
cd quill
duck runserver
```
Open `http://localhost:8000`

---

## Key files

| File | What it does |
|---|---|
| `web/claude_client.py` | Anthropic streaming API wrapper |
| `web/ui/components/prompt_form.py` | Prompt input + generate button |
| `web/ui/components/preview_panel.py` | iframe preview + resize + download |
| `web/ui/pages/home.py` | Full page layout |
| `web/settings.py` | API key, model, Duck config |

---

*Part of the Duck Framework showcase — [duckframework.xyz](https://duckframework.xyz)*
