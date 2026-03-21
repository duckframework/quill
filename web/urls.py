"""
URL patterns for Quill.
"""
from duck.urls import path

from web import views


urlpatterns = [
    path("/", views.home, name="home"),
]
