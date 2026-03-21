"""
HomePage — Quill's single-page layout.

Desktop: sidebar (PromptForm) on the left, PreviewPanel on the right.
Mobile:  sidebar flows inline above the preview panel (column direction).
"""
from duck.html.components.page import Page
from duck.html.components.container import FlexContainer
from duck.html.components.style import Style
from duck.html.components import to_component

from web.ui.components.prompt_form import PromptForm
from web.ui.components.preview_panel import PreviewPanel


# Global CSS — layout, typography, scrollbars, animations, mobile breakpoint
GLOBAL_STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background: #08080f;
    color: #fff;
    font-family: 'Syne', -apple-system, BlinkMacSystemFont, sans-serif;
    min-height: 100vh;
    overflow: hidden;
}

/* Scrollbars */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 3px; }

/* Range input */
input[type=range] { height: 4px; }
input[type=range]::-webkit-slider-thumb {
    width: 14px; height: 14px; border-radius: 50%;
    background: #6366f1; cursor: pointer;
}

/* Textarea + select focus */
textarea:focus, select:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12);
}
textarea::placeholder { color: rgba(255,255,255,0.2); }

/* Shared pulse animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.5; }
}

/* Button states */
button:not(:disabled):hover { filter: brightness(1.1); }
button:disabled { opacity: 0.5; cursor: not-allowed !important; }

/* Mobile — sidebar flows inline, no drawer */
@media (max-width: 768px) {
    body { overflow: auto; }

    #quill-layout {
        flex-direction: column !important;
        height: auto !important;
        overflow: visible !important;
    }

    #quill-sidebar {
        width: 100% !important;
        border-right: none !important;
        border-bottom: 1px solid rgba(255,255,255,0.06) !important;
        padding: 24px 20px !important;
        overflow-y: visible !important;
        flex-shrink: 0 !important;
    }

    #quill-right {
        padding: 16px 20px !important;
        gap: 14px !important;
        overflow: visible !important;
        min-height: 60vh;
    }

    /* Resize sliders stack vertically */
    .quill-resize-row {
        flex-direction: column !important;
        gap: 10px !important;
    }

    /* Download button full width */
    #quill-download-btn {
        width: 100% !important;
        text-align: center !important;
    }
}
"""


class HomePage(Page):
    """
    Quill's main page. Builds the two-panel layout and injects global styles.
    """
    def on_create(self):
        super().on_create()
        self.set_title("Quill — AI Design Generator")
        self.set_description(
            "Describe any design in plain English. Quill uses AI to generate "
            "a pixel-perfect HTML design you can download as a PNG instantly."
        )
        self.build_page()

    def build_page(self):
        """
        Assembles the full page: styles, Prism.js, layout, sidebar, and right panel.
        """
        # Inject global styles
        self.add_to_head(Style(inner_html=GLOBAL_STYLES))

        # Prism.js syntax highlighting for the HTML code editor
        prism_css = to_component("", "link", no_closing_tag=True)
        prism_css.props.update({
            "rel": "stylesheet",
            "href": "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css",
        })
        self.add_to_head(prism_css)

        prism_core = to_component("", "script", no_closing_tag=False)
        prism_core.props["src"] = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"
        self.add_to_head(prism_core)

        # Load all grammars needed for full HTML + embedded CSS + embedded JS
        for src in [
            "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-markup.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-css.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/markup-templating/prism-markup-templating.min.js",
        ]:
            s = to_component("", "script", no_closing_tag=False)
            s.props["src"] = src
            self.add_to_head(s)

        prism_autoload = to_component("", "script", no_closing_tag=False)
        prism_autoload.props.update({
            "src": "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js",
            "data-manual": "true",
        })
        self.add_to_head(prism_autoload)

        # Build layout and panels
        layout = self.build_layout()
        self.build_sidebar(layout)
        self.build_right(layout)
        self.add_to_body(layout)

        # Status strip helpers — show generating/error state above the button
        from duck.html.components.script import Script
        self.add_to_body(Script(inner_html="""
function quillSetGenerating() {
    var strip = document.getElementById('quill-status-strip');
    var icon  = document.getElementById('quill-status-icon');
    var text  = document.getElementById('quill-status-text');
    if (!strip) return;
    strip.style.display    = 'flex';
    strip.style.background = 'rgba(99,102,241,0.1)';
    strip.style.border     = '1px solid rgba(99,102,241,0.25)';
    strip.style.color      = '#a5b4fc';
    icon.innerHTML  = '&#9711;';
    icon.style.animation = 'pulse 1s ease-in-out infinite';
    text.innerText  = 'Generating your design...';
}

function quillSetStatusError(message) {
    var strip = document.getElementById('quill-status-strip');
    var icon  = document.getElementById('quill-status-icon');
    var text  = document.getElementById('quill-status-text');
    if (!strip) return;
    strip.style.display    = 'flex';
    strip.style.background = 'rgba(248,113,113,0.08)';
    strip.style.border     = '1px solid rgba(248,113,113,0.25)';
    strip.style.color      = '#fca5a5';
    icon.innerHTML  = '&#9888;';
    icon.style.animation = '';
    text.innerText  = message;
}

function quillClearStatus() {
    var strip = document.getElementById('quill-status-strip');
    if (strip) strip.style.display = 'none';
}
"""))

    def build_layout(self) -> FlexContainer:
        """
        Creates the root flex row that holds the sidebar and right panel.
        """
        layout = FlexContainer(
            id="quill-layout",
            style={
                "flex-direction": "row",
                "height": "100vh",
                "gap": "0",
                "overflow": "hidden",
            },
        )
        return layout

    def build_sidebar(self, parent: FlexContainer):
        """
        Builds the left sidebar containing the PromptForm.
        On mobile this flows inline above the preview panel.
        """
        sidebar = FlexContainer(
            id="quill-sidebar",
            style={
                "flex-direction": "column",
                "width": "360px",
                "flex-shrink": "0",
                "background": "rgba(255,255,255,0.02)",
                "border-right": "1px solid rgba(255,255,255,0.06)",
                "padding": "32px 28px",
                "overflow-y": "auto",
                "gap": "0",
            },
        )

        # Add the prompt form
        self.form = PromptForm()
        sidebar.add_child(self.form)
        parent.add_child(sidebar)

    def build_right(self, parent: FlexContainer):
        """
        Builds the right panel containing the PreviewPanel.
        """
        right = FlexContainer(
            id="quill-right",
            style={
                "flex-direction": "column",
                "flex": "1",
                "padding": "32px 28px",
                "overflow": "auto",
                "gap": "20px",
                "min-width": "0",
            },
        )

        # Add the preview panel
        self.preview = PreviewPanel()
        right.add_child(self.preview)
        parent.add_child(right)
