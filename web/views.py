"""
Views for Quill.
"""
from duck.settings import SETTINGS
from duck.utils.path import joinpaths
from duck.shortcuts import to_response, not_found404
from duck.http.response import FileResponse

from web.ui.pages.home import HomePage


async def robots(request):
    """
    View for serving a robots.txt file.
    """
    robots_txt = joinpaths(SETTINGS['BASE_DIR'], "etc/robots.txt")
    return FileResponse(robots_txt)
    
    
async def favicon(request):
    """
    View for serving a favicon.
    """
    if SETTINGS['DEBUG']:
        favicon = joinpaths(SETTINGS['BASE_DIR'], "web/ui/static/images/favicon.ico")
    else:
        favicon = joinpaths(SETTINGS['STATIC_ROOT'], "images/favicon.ico")
    return FileResponse(favicon)


async def home(request):
    """
    Renders the Quill home page.
    """
    page = HomePage(request=request)
    return to_response(page)
