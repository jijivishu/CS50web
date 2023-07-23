from django.urls import include, path

from . import views

urlpatterns = [
    path("/<int:id>", views.item, name="item"),
    path("/<int:id>/bid", views.bidding, name="bidding"),
    path("/<int:id>/close", views.close, name="close"),
    path("/<int:id>/watch", views.watch, name="watch"),
]
