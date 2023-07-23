from django.urls import include, path

from . import views

urlpatterns = [
    path("/", views.categories, name="categories"),
    path("/<str:cat>", views.cat, name="cat"),
]
