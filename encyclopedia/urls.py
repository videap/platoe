from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show_entry, name="show_entry"),
    path("newpage", views.new_page, name="new_page"),
    path("editpage/<str:edit_entry>", views.edit_page, name="edit_page"),
    path("random", views.random, name="random")
]
