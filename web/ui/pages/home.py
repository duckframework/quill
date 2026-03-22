"""
HomePage — Quill's single-page layout.

Desktop: sidebar (mode tabs + PromptForm / ImportForm) on the left,
         PreviewPanel on the right.
Mobile:  sidebar flows inline above the preview panel.
"""
from duck.html.components.container import FlexContainer
from duck.html.components.script import Script
from duck.html.components import to_component

from web.ui.pages.base import BasePage, DUCK_HOMEPAGE, DONATE_URL
from web.ui.components.prompt_form import PromptForm, ImportForm
from web.ui.components.preview_panel import PreviewPanel


# Mode-switching JS — swaps between Generate and Import panels
MODE_SCRIPT = """
function quillSwitchMode(mode) {
    var modes = ['generate', 'import'];
    modes.forEach(function(m) {
        var panel = document.getElementById('quill-mode-' + m);
        var tab   = document.getElementById('quill-mode-tab-' + m);
        if (!panel || !tab) return;
        var active = (m === mode);
        panel.style.display    = active ? 'flex' : 'none';
        tab.style.color        = active ? '#fff' : 'rgba(255,255,255,0.35)';
        tab.style.borderBottom = active ? '2px solid #6366f1' : '2px solid transparent';
    });
}

// Show import status strip
function quillShowImportStatus(type, message) {
    var strip = document.getElementById('quill-import-status-strip');
    var icon  = document.getElementById('quill-import-status-icon');
    var text  = document.getElementById('quill-import-status-text');
    if (!strip) return;
    var styles = {
        loading: { bg: 'rgba(99,102,241,0.1)',   border: 'rgba(99,102,241,0.25)',  color: '#a5b4fc' },
        success: { bg: 'rgba(74,222,128,0.08)',   border: 'rgba(74,222,128,0.25)',  color: '#4ade80' },
        error:   { bg: 'rgba(248,113,113,0.08)',  border: 'rgba(248,113,113,0.25)', color: '#fca5a5' },
    };
    var s = styles[type] || styles.loading;
    strip.style.display    = 'flex';
    strip.style.background = s.bg;
    strip.style.border     = '1px solid ' + s.border;
    strip.style.color      = s.color;
    icon.style.animation   = type === 'loading' ? 'pulse 1s ease-in-out infinite' : '';
    text.innerHTML = message;
}
"""


class HomePage(BasePage):
    """
    Quill's main page — two-panel layout with sidebar and preview.
    Sidebar has two mode tabs: Generate (AI prompt) and Import (URL fetch).
    """
    PAGE_TITLE       = "Quill — AI Design Generator | Powered by Duck Framework"
    PAGE_DESCRIPTION = (
        "Describe any design in plain English. Quill uses AI to instantly generate "
        "a pixel-perfect HTML poster, social card, code snippet, certificate, or "
        "Open Graph image you can download as a PNG. Built with Duck Framework."
    )
    PAGE_KEYWORDS    = [
        "AI design generator", "AI poster maker", "AI social card generator",
        "AI certificate generator", "AI open graph image generator",
        "HTML design generator", "generate design from text",
        "import website screenshot", "duck framework", "quill",
    ]

    # Design-type specific OG images — served at ?dt=<type>
    DESIGN_OG_IMAGES = {
        "poster":      "images/og-poster.png",
        "code":        "images/og-code.png",
        "social":      "images/og-social.png",
        "certificate": "images/og-certificate.png",
        "opengraph":   "images/og-opengraph.png",
        "custom":      "images/og-image.png",
    }

    def on_create(self):
        super().on_create()
        self.build_page()

    def get_json_ld(self) -> dict:
        return {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Quill",
            "url": self._page_url,
            "description": self.PAGE_DESCRIPTION,
            "applicationCategory": "DesignApplication",
            "operatingSystem": "All",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "author": {
                "@type": "Organization",
                "name": "Duck Framework",
                "url": DUCK_HOMEPAGE,
            },
            "potentialAction": {
                "@type": "CreateAction",
                "target": self._page_url,
                "name": "Generate an AI Design",
            },
        }

    def build_page(self):
        """
        Assembles the two-panel layout.
        """
        layout = self.build_layout()
        self.build_sidebar(layout)
        self.build_right(layout)
        self.add_to_body(layout)
        self.add_to_body(Script(inner_html=MODE_SCRIPT))

    def build_layout(self) -> FlexContainer:
        return FlexContainer(
            id="quill-layout",
            style={
                "flex-direction": "row",
                "height": "100vh",
                "gap": "0",
                "overflow": "hidden",
            },
        )

    def build_sidebar(self, parent: FlexContainer):
        """
        Left sidebar with Generate / Import mode tabs at the top.
        Each tab reveals its own panel below.
        """
        sidebar = FlexContainer(
            id="quill-sidebar",
            style={
                "flex-direction": "column",
                "width": "360px",
                "flex-shrink": "0",
                "background": "rgba(255,255,255,0.02)",
                "border-right": "1px solid rgba(255,255,255,0.06)",
                "padding": "0",
                "overflow-y": "auto",
                "gap": "0",
            },
        )

        # Mode tab bar
        tab_bar = to_component("", "div", no_closing_tag=False)
        tab_bar.style.update({
            "display": "flex",
            "flex-direction": "row",
            "border-bottom": "1px solid rgba(255,255,255,0.07)",
            "flex-shrink": "0",
        })

        for mode_id, label, active in [
            ("generate", "✦  Generate", True),
            ("import",   "⤓  Import",   False),
        ]:
            btn = to_component(label, "button", no_closing_tag=False)
            btn.id = f"quill-mode-tab-{mode_id}"
            btn.props.update({
                "type": "button",
                "onclick": f"quillSwitchMode('{mode_id}')",
                "aria-label": f"Switch to {mode_id} mode",
            })
            btn.style.update({
                "flex": "1",
                "padding": "13px 0",
                "background": "none",
                "border": "none",
                "border-bottom": "2px solid #6366f1" if active else "2px solid transparent",
                "color": "#fff" if active else "rgba(255,255,255,0.35)",
                "font-family": "inherit",
                "font-size": "0.82rem",
                "font-weight": "600",
                "cursor": "pointer",
                "letter-spacing": "0.04em",
                "transition": "color 0.15s, border-color 0.15s",
            })
            tab_bar.add_child(btn)

        sidebar.add_child(tab_bar)

        # Generate panel — visible by default
        generate_panel = to_component("", "div", no_closing_tag=False)
        generate_panel.id = "quill-mode-generate"
        generate_panel.style.update({
            "display": "flex",
            "flex-direction": "column",
            "padding": "28px 28px 32px",
        })
        self.form = PromptForm()
        generate_panel.add_child(self.form)
        sidebar.add_child(generate_panel)

        # Import panel — hidden by default
        import_panel = to_component("", "div", no_closing_tag=False)
        import_panel.id = "quill-mode-import"
        import_panel.style.update({
            "display": "none",
            "flex-direction": "column",
            "padding": "28px 28px 32px",
        })
        self.import_form = ImportForm()
        import_panel.add_child(self.import_form)
        sidebar.add_child(import_panel)

        parent.add_child(sidebar)

    def build_right(self, parent: FlexContainer):
        """
        Right panel — PreviewPanel shared by both modes.
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
        self.preview = PreviewPanel()
        right.add_child(self.preview)
        parent.add_child(right)
