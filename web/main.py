#!/usr/bin/env python
"""
Entry point for the Quill application.
Run this file to start the server: python web/main.py
"""
import os

from duck.settings import SETTINGS


# Environment 
# Read configuration from environment variables so the same code works
# locally and on any deployment platform without changing this file.
#
#   DEBUG      — True locally. Set to False in production.
#   DOMAIN   — Your app's public domain. Defaults to localhost.
#   PORT         — The port the server listens on. Deployment platforms often
#                           assign this automatically via an environment variable.

DEBUG = bool(os.getenv("DEBUG", True))
PORT = int(os.getenv("PORT") or 8000)
DOMAIN = os.getenv("DOMAIN", "localhost")


# Duck settings override
# Override specific values from web/settings.py at runtime.
# Keeps deployment config here rather than scattered across settings files.

SETTINGS['ENABLE_HTTPS']  = 0  # Set to 1 if your server handles HTTPS directly
SETTINGS['DEBUG'] = DEBUG
SETTINGS['EXTRA_HEADERS'] = {"cache-control": "no-cache"} if DEBUG else {}
SETTINGS['ALLOWED_HOSTS'] = [DOMAIN, f"*.{DOMAIN}"] if not DEBUG else ["*"]
SETTINGS['ASYNC_HANDLING'] = True


from duck.app import App


app = App(
    port=PORT,                # Custom port to receive traffic from
    addr="0.0.0.0",          # Accept connections from any network interface
    domain=DOMAIN,    # Configure application domain
    workers=5,                # Number of worker threads — increase for higher traffic
)


if __name__ == "__main__":
    super_on_app_start = app.on_app_start

    def on_app_start():
        from duck.meta import Meta

        # Some deployment platforms run the app on an internal port (e.g. 5000)
        # but expose it publicly on a different domain and port (e.g. port 443 over HTTPS).
        # This tells Duck the correct public protocol and port so WebSocket URLs
        # and security headers point to the right place.
        Meta.update_meta({"DUCK_SERVER_PORT": 443, "DUCK_SERVER_PROTOCOL": "https"})
        super_on_app_start()

    # Only apply this fix in production — not needed for local development.
    if not DEBUG:
        app.on_app_start = on_app_start

    app.run()
