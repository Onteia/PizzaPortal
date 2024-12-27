from django.urls import path
from . import views

urlpatterns = [
    path("", views.portal_view, name="portal"),
    path("<int:item_id>/edit/", views.edit_view, name="edit"),
    path("add/", views.add_view, name="add"),
    path("<int:item_id>/delete/", views.delete_view, name="delete"),
]
