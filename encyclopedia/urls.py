from django.urls import path

from . import views


app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki"),
    path("wiki/<str:title>/", views.entry_page, name="entry"),
    path("wiki/<str:title>/edit/", views.edit_entry, name="edit"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("random/", views.random_entry, name="random")
]
