"""
HomePage — Quill's single-page layout.

Inherits global styles, Prism.js, status strip JS, and all SEO from
BasePage. Only defines what is unique to this page.

Desktop: sidebar (PromptForm) on the left, PreviewPanel on the right.
Mobile:  sidebar flows inline above the preview panel.
"""
from duck.html.components.container import FlexContainer

from web.ui.pages.base import BasePage, DUCK_HOMEPAGE, DONATE_URL
from web.ui.components.prompt_form import PromptForm
from web.ui.components.preview_panel import PreviewPanel


# Design-type specific OG image map.
# Each key matches a design_type value from the prompt form.
# Override by setting og_image in query params or via subclassing.
DESIGN_OG_IMAGES = {
    "poster":      "images/og-poster.png",
    "code":        "images/og-code.png",
    "social":      "images/og-social.png",
    "certificate": "images/og-certificate.png",
    "custom":      "images/og-image.png",
}


class HomePage(BasePage):
    """
    Quill's main page — two-panel layout with sidebar and preview.
    Inherits all SEO and shared assets from BasePage.
    """
    PAGE_TITLE       = "Quill — AI Design Generator | Powered by Duck Framework"
    PAGE_DESCRIPTION = (
        "Describe any design in plain English. Quill uses AI to instantly generate "
        "a pixel-perfect HTML poster, social card, code snippet, or certificate "
        "you can download as a PNG. Built with Duck Framework — pure Python."
    )
    PAGE_KEYWORDS    = [
        "AI design generator", "AI poster maker", "AI social card generator",
        "AI certificate generator", "AI code card", "HTML design generator",
        "generate design from text", "duck framework showcase",
        "python AI app", "no javascript design tool", "quill",
    ]

    def on_create(self):
        # BasePage.on_create injects styles, Prism, status strip, and all SEO
        super().on_create()
        self.build_page()

    def get_json_ld(self) -> dict:
        """
        Homepage JSON-LD — WebApplication with a CreateAction describing
        that the primary use is generating a design from a text prompt.
        """
        return {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Quill",
            "url": self._page_url,
            "description": self.PAGE_DESCRIPTION,
            "applicationCategory": "DesignApplication",
            "operatingSystem": "All",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD",
            },
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
        Assembles the two-panel layout: sidebar on the left, preview on the right.
        """
        layout = self.build_layout()
        self.build_sidebar(layout)
        self.build_right(layout)
        self.add_to_body(layout)

    def build_layout(self) -> FlexContainer:
        """
        Root flex row that holds the sidebar and right panel.
        """
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
        Left sidebar — PromptForm in a scrollable panel.
        Flows inline above the preview on mobile.
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

        self.form = PromptForm()
        sidebar.add_child(self.form)
        parent.add_child(sidebar)

    def build_right(self, parent: FlexContainer):
        """
        Right panel — PreviewPanel with tabs, iframe, sliders, and download.
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
