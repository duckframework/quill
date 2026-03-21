"""
claude_client.py — Anthropic API wrapper for Quill.

Handles streaming HTML generation from Claude.
Each design type gets its own tailored system prompt.
"""
import anthropic

from duck.settings import SETTINGS


# ── Design type system prompts ───────────────────────────────────────────────

_BASE_RULES = """
CRITICAL RULES — follow every one without exception:
- Return ONLY a single complete HTML document. Nothing else. No explanation, no markdown, no code fences.
- The HTML must be fully self-contained — all CSS inside <style>, all JS inside <script>.
- Do NOT use external CDN links, image URLs, or any resource that requires a network request.
- Use only web-safe fonts OR embed a Google Fonts @import inside the <style> tag.
- The design must look stunning. Treat this as professional creative work.
- Every element must be visible and readable against its background.
- The root element should fill 100% of the viewport with no scrollbars.
""".strip()

SYSTEM_PROMPTS = {
    "poster": f"""
You are an expert graphic designer who creates stunning posters and flyers as HTML.
Your designs use bold typography, rich gradients, dramatic layouts, and strong visual hierarchy.
Think concert posters, event flyers, promotional material — vivid, eye-catching, professional.
{_BASE_RULES}
""".strip(),

    "code": f"""
You are a developer advocate who creates beautiful code snippet showcase cards as HTML.
Your designs use dark themes, accurate syntax highlighting with span-based coloring,
clean monospace fonts, subtle glow effects, and a polished "screenshot-worthy" aesthetic.
Include a filename tab, line numbers, and a language badge.
{_BASE_RULES}
""".strip(),

    "social": f"""
You are a social media designer who creates scroll-stopping cards as HTML.
Your designs are bold, modern, and optimised for sharing — think Twitter/LinkedIn cards,
quote graphics, announcement posts. Strong contrast, punchy copy layout, and clear branding.
{_BASE_RULES}
""".strip(),

    "certificate": f"""
You are a formal document designer who creates elegant certificates as HTML.
Your designs use classic serif typography, decorative borders, gold/cream/navy palettes,
official seals, and a sense of prestige and ceremony.
{_BASE_RULES}
""".strip(),

    "custom": f"""
You are a world-class creative designer who creates any visual design as HTML.
Interpret the user's prompt freely and produce the most visually impressive result possible.
Match the aesthetic to the content — minimal for tech, ornate for formal, vibrant for events.
{_BASE_RULES}
""".strip(),
}


def stream_design(prompt: str, design_type: str):
    """
    Calls Claude API with streaming enabled.
    Yields HTML chunks as they arrive.

    Args:
        prompt:      The user's design prompt.
        design_type: One of: poster, code, social, certificate, custom.

    Yields:
        str — partial HTML text chunks from the stream.
    """
    system = SYSTEM_PROMPTS.get(design_type, SYSTEM_PROMPTS["custom"])

    client = anthropic.Anthropic(api_key=SETTINGS["ANTHROPIC_API_KEY"])

    with client.messages.stream(
        model=SETTINGS["CLAUDE_MODEL"],
        max_tokens=SETTINGS["CLAUDE_MAX_TOKENS"],
        system=system,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text
