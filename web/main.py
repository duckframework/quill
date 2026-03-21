"""
Entry point — creates and runs the Quill application.
"""
from duck.app import App


app = App(port=8000, addr="0.0.0.0", domain="localhost")

if __name__ == "__main__":
    app.run()
