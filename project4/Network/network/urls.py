
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("your", views.your, name="your"),
    path("user/<int:id>", views.user, name="user"),
    path("follow", views.follow, name="follow"),
    path("followdata/<int:id>", views.followdata, name="followdata"),
    path("like", views.like, name="like"),
    path("feed", views.feed, name="feed"),
    path("post", views.postdata, name="post"),
    path("edit", views.edit, name="edit")
]


''' 
index: Acts as landing page url
login: To log a user in
logout: To log user out
register: To register the new user
create: To create new posts
your: To show user, posts created by him
user/id: To load profile of a user
follow: To update (un)follow data
followdata: To fetch follower and following data
like: To update (dis)like data
feed: To show user posts by people (s)he follows
post: To fetch data associated with any particular post
edit: To edit any particular post
'''