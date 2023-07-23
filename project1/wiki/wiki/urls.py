"""
path_name: use
title: facilitates showcase of entry content           
search: facilitates searching through entry title
add: facilitates adding new entry
edit: facilitates editing of existing entries
random: shows a random entry content
"""
from django.contrib import admin
from django.urls import include, path

from encyclopedia import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("encyclopedia.urls")),
    path('wiki/' + '<str:name>', views.title, name="title"),
    path('search/', views.search, name="search"),
    path('add/', views.add, name="add"),
    path('edit/', views.edit, name="edit"),
    path('random/', views.rand, name="random")
]
