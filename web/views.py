"""
Views for Quill.
"""
from duck.shortcuts import to_response

from web.ui.pages.home import HomePage


def home(request):
    """
    Renders the Quill home page.
    """
    page = HomePage(request=request)
    return to_response(page)
