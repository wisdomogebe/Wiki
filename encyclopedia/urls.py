from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry_title>", views.entry, name="entry"),
    path("Special:createpage/", views.create, name="create"),
    path("Special:editpage/", views.edit, name="edit"),
]
