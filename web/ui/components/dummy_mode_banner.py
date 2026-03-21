"""
DummyModeBanner component — lets users try Quill in demo mode.

Demo mode streams pre-built designs instantly with no API key needed.
Only the design type selector is interactive — prompt is locked.
Toggle state is per-session (one per WebSocket connection).
"""
from duck.html.components.container import FlexContainer
from duck.html.components.paragraph import Paragraph
from duck.html.components.label import Label
from duck.html.components import to_component
from duck.html.components.script import Script

from duck.settings import SETTINGS


# JS — animates the toggle switch and locks/unlocks all form fields
TOGGLE_SCRIPT = """
function quillUpdateDummyToggle(enabled) {
    var knob  = document.getElementById('quill-dummy-knob');
    var track = document.getElementById('quill-dummy-track');
    var badge = document.getElementById('quill-dummy-badge');
    if (!knob || !track) return;

    if (enabled) {
        knob.style.transform   = 'translateX(18px)';
        track.style.background = '#6366f1';
        if (badge) badge.style.display = 'inline-block';
    } else {
        knob.style.transform   = 'translateX(0px)';
        track.style.background = 'rgba(255,255,255,0.12)';
        if (badge) badge.style.display = 'none';
    }
}

function quillApplyDummyState(enabled) {
    var prompt     = document.getElementById('quill-prompt');
    var modelGroup = document.getElementById('quill-model-group');
    var submitBtn  = document.getElementById('quill-submit-btn');
    var chips      = document.querySelectorAll('.quill-example-chip');
    var note       = document.getElementById('quill-dummy-note');

    if (enabled) {
        // Lock prompt textarea
        if (prompt) {
            prompt.disabled = true;
            prompt.style.opacity = '0.35';
            prompt.style.cursor  = 'not-allowed';
            prompt.style.resize  = 'none';
        }
        // Hide model selector
        if (modelGroup) modelGroup.style.display = 'none';
        // Disable example chips (keep visible)
        chips.forEach(function(c) {
            c.disabled             = true;
            c.style.opacity        = '0.35';
            c.style.cursor         = 'not-allowed';
            c.style.pointerEvents  = 'none';
        });
        // Update button label
        if (submitBtn) submitBtn.innerText = '⚡  Run Demo';
        // Show locked note
        if (note) note.style.display = 'block';
    } else {
        // Unlock prompt textarea
        if (prompt) {
            prompt.disabled      = false;
            prompt.style.opacity = '1';
            prompt.style.cursor  = 'text';
            prompt.style.resize  = 'vertical';
        }
        // Show model selector
        if (modelGroup) modelGroup.style.display = 'flex';
        // Re-enable example chips
        chips.forEach(function(c) {
            c.disabled            = false;
            c.style.opacity       = '1';
            c.style.cursor        = 'pointer';
            c.style.pointerEvents = 'auto';
        });
        // Restore button label
        if (submitBtn) submitBtn.innerText = '✦  Generate Design';
        // Hide locked note
        if (note) note.style.display = 'none';
    }
}
"""


class DummyModeBanner(FlexContainer):
    """
    Info banner with a toggle switch to enable or disable demo mode.

    Demo ON:  pre-built designs stream instantly, prompt is locked.
    Demo OFF: all fields active, real AI generation.

    Exposes is_dummy_enabled() for the form handler to read before each
    generation. Toggle state persists on this instance for the session.
    """
    def on_create(self):
        super().on_create()
        self.style.update({
            "flex-direction": "column",
            "gap": "0",
            "border-radius": "12px",
            "overflow": "hidden",
            "border": "1px solid rgba(99,102,241,0.2)",
            "background": "rgba(99,102,241,0.06)",
        })

        # Read initial state from settings
        self.dummy_enabled = SETTINGS.get("QUILL_DUMMY_MODE", False)

        self.build_header()
        self.build_body()
        self.add_child(Script(inner_html=TOGGLE_SCRIPT))

    # Header row
    def build_header(self):
        """
        Builds the always-visible header: icon, title, ON badge, and toggle switch.
        """
        header = FlexContainer(
            style={
                "flex-direction": "row",
                "align-items": "center",
                "justify-content": "space-between",
                "padding": "11px 14px",
                "gap": "10px",
            },
        )

        # Left side — icon, label, ON badge
        left = FlexContainer(
            style={
                "flex-direction": "row",
                "align-items": "center",
                "gap": "8px",
            },
        )

        icon = to_component("⚡", "span")
        icon.style["font-size"] = "0.9rem"

        title = Label(
            text="Demo Mode",
            style={
                "font-size": "0.82rem",
                "font-weight": "700",
                "color": "#a5b4fc",
            },
        )

        # ON badge — visible only when demo mode is active
        badge = to_component("ON", "span")
        badge.id = "quill-dummy-badge"
        badge.style.update({
            "font-size": "0.6rem",
            "font-weight": "800",
            "color": "#6366f1",
            "background": "rgba(99,102,241,0.2)",
            "border": "1px solid rgba(99,102,241,0.4)",
            "padding": "1px 6px",
            "border-radius": "99px",
            "letter-spacing": "0.08em",
            "display": "inline-block" if self.dummy_enabled else "none",
        })

        left.add_children([icon, title, badge])

        # Toggle switch button
        self.toggle_btn = to_component("", "button")
        self.toggle_btn.id = "quill-dummy-toggle"
        self.toggle_btn.props.update({
            "type": "button",
            "aria-label": "Toggle demo mode",
        })
        self.toggle_btn.style.update({
            "background": "none",
            "border": "none",
            "padding": "0",
            "cursor": "pointer",
            "display": "flex",
            "align-items": "center",
        })

        # Track
        track = to_component("", "div")
        track.id = "quill-dummy-track"
        track.style.update({
            "width": "38px",
            "height": "20px",
            "border-radius": "99px",
            "background": "#6366f1" if self.dummy_enabled else "rgba(255,255,255,0.12)",
            "position": "relative",
            "transition": "background 0.2s",
            "flex-shrink": "0",
        })

        # Knob
        knob = to_component("", "div")
        knob.id = "quill-dummy-knob"
        knob.style.update({
            "position": "absolute",
            "top": "3px",
            "left": "3px",
            "width": "14px",
            "height": "14px",
            "border-radius": "50%",
            "background": "#fff",
            "transition": "transform 0.2s",
            "transform": "translateX(18px)" if self.dummy_enabled else "translateX(0px)",
        })

        # Assemble toggle
        track.add_child(knob)
        self.toggle_btn.add_child(track)

        # Bind toggle click
        self.toggle_btn.bind(
            "click",
            self.handle_toggle,
            update_targets=[],
            update_self=False,
        )

        header.add_children([left, self.toggle_btn])
        self.add_child(header)

    # Body / description
    def build_body(self):
        """
        Builds the description text and the locked-prompt note.
        """
        body = FlexContainer(
            style={
                "flex-direction": "column",
                "gap": "8px",
                "padding": "0 14px 12px 14px",
            },
        )

        # Description paragraph
        desc = Paragraph(
            inner_html=(
                "Try Quill instantly — no sign-up or waiting. "
                "Demo mode shows you a pre-built design for each type "
                "so you can experience live streaming, the code editor, "
                "resize, and download right now."
            ),
            style={
                "font-size": "0.75rem",
                "color": "rgba(255,255,255,0.45)",
                "margin": "0",
                "line-height": "1.55",
            },
        )

        # Note shown only when demo mode is ON
        self.demo_active_note = Paragraph(
            inner_html=(
                "🔒 In demo mode only the design type can be changed. "
                "Turn demo mode off to write your own prompt."
            ),
            style={
                "font-size": "0.72rem",
                "color": "rgba(255,255,255,0.35)",
                "margin": "0",
                "line-height": "1.5",
                "display": "block" if self.dummy_enabled else "none",
            },
        )
        self.demo_active_note.id = "quill-dummy-note"

        body.add_children([desc, self.demo_active_note])
        self.add_child(body)

    # Toggle handler
    async def handle_toggle(self, source, event, value, ws):
        """
        Flips demo mode and updates the toggle and all form fields via JS.
        No Lively re-render needed — JS handles all visual changes.
        """
        # Flip the state
        self.dummy_enabled = not self.dummy_enabled
        enabled_js = "true" if self.dummy_enabled else "false"

        # Animate toggle and update form fields in one call
        await ws.execute_js(
            f"quillUpdateDummyToggle({enabled_js}); quillApplyDummyState({enabled_js});",
            wait_for_result=False,
        )

    def is_dummy_enabled(self) -> bool:
        """
        Returns whether demo mode is currently active for this session.
        """
        return self.dummy_enabled
