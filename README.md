# ✦ Quill — AI Design Generator

> Describe any design in plain English. Quill uses different AI models to generate
> a pixel-perfect HTML design you can download as a PNG instantly.
> Built with Duck Framework — pure Python, no JavaScript frameworks.


**[▶ Try the Live Demo](https://quill.duckframework.com/)**

---

## What is this?

Quill is an AI-powered design tool. You type a prompt like:

> *"A neon cyberpunk music festival poster for Lagos, Nigeria"*

Quill sends that prompt to Claude or the chose model, which generates a complete HTML design.
You watch the design build itself live in the preview panel as Claude/Groq/Gemini streams
the response token by token. Then you resize it and download it as a PNG.

---

## Installation

### Step 1 — Install dependencies

Clone the repo and navigate inside the project, then run the following command:

```bash
pip install -r requirements.txt
```

### Step 2 — Add your API keys

Open `web/settings.py` and replace `"your-api-key-here"` with your key.
Or use an environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."
export GROK_API_KEY="..."
```

### Step 3 — Run

```bash
python web/main.py
```

Open `http://localhost:8000`

---

## Key files

| File | What it does |
|---|---|
| `web/ai_client.py` | AI client streaming API wrapper |
| `web/ui/components/prompt_form.py` | Prompt input + generate button |
| `web/ui/components/preview_panel.py` | iframe preview + resize + download |
| `web/ui/pages/home.py` | Full page layout |
| `web/settings.py` | API keys, model, Duck config |

---

*Part of the Duck Framework showcase — [duckframework.com](https://duckframework.com)*
