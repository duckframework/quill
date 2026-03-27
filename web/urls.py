"""
URL patterns for Quill.
"""
from duck.urls import path

from web import views


urlpatterns = [
    path("/", views.home, name="home"),
    path("/robots.txt", views.robots, name="robots-txt"),
    path("/favicon.ico", views.favicon, name="favicon"),
]
