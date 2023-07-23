from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

import json
import operator

from .models import User, Post, Follow, Like


# Landing View
def index(request):

    # Get posts by the order they were last uploaded to show on the landing page
    posts = Post.objects.all().order_by('-info')

    # Get all posts the user has liked to assign like icon as per the status
    liked = Like.objects.filter(liker=request.user.id).values_list('liked', flat=True)

    # Update number of likes on every post and whether the current user hasliked it, into the already fetched Post object
    for post in posts:
        count = Like.objects.filter(liked=post).count()
        post.likes = count
        post.like_status = 0
        if post.id in liked:
            post.like_status = 1
    
    # Restrict number of posts to 10 through Django Paginator class 
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    post = paginator.get_page(page)

    # Send a clone of user data which will be replaced by another user's data whenever user visit's another user's profile 
    who = request.user
    who.info = datetime.now().strftime('%B %d, %Y, %I:%M %p')
    
    return render(request, "network/layout.html", {
        "posts": post,
        "who": who
    })


# Log the user in unless an error shows up, in that case get back to landing page anonymously, with error message
def login_view(request):
    if request.method == "POST":

        # Get the info that was being displayed on page initially
        posts = Post.objects.all().order_by('-info')
        liked = Like.objects.filter(liker=request.user.id).values_list('liked', flat=True)
        for post in posts:
            count = Like.objects.filter(liked=post).count()
            post.likes = count
            post.like_status = 0
            if post.id in liked:
                post.like_status = 1
        
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        post = paginator.get_page(page)

        who = request.user
        who.info = datetime.now().strftime('%B %d, %Y, %I:%M %p')

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/layout.html", {
                "message": "Invalid username and/or password.",
                "posts": post,
                "who": who
            })
    else:
        return render(request, "network/login.html")


# Log user Out
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register a new user unless he uses pre-used username or fails password confirmation
def register(request):
    if request.method == "POST":

        # Get the info that was being displayed on page initially
        posts = Post.objects.all().order_by('-info')
        liked = Like.objects.filter(liker=request.user.id).values_list('liked', flat=True)
        for post in posts:
            count = Like.objects.filter(liked=post).count()
            post.likes = count
            post.like_status = 0
            if post.id in liked:
                post.like_status = 1
        
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        post = paginator.get_page(page)

        who = request.user
        who.info = datetime.now().strftime('%B %d, %Y, %I:%M %p')

        # Get user's entered parameter
        username = request.POST["username"]
        email = request.POST["email"]
        pfp = 0

        # Check if user sent a pfp
        if request.FILES:
            pfp = request.FILES["pfp"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/layout.html", {
                "message": "Passwords must match.",
                "posts": post,
                "who": who
            })

        # Attempt to create new user
        try:
            if pfp:
                user = User.objects.create_user(username, email, password, pfp=pfp)
            else:
                user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/layout.html", {
                "message": "Username already taken.",
                "posts": post,
                "who": who
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# Create a post
@login_required
def create(request):
    if request.method == "POST":

        # Get the info that was being displayed on page initially
        posts = Post.objects.all().order_by('-info')
        liked = Like.objects.filter(liker=request.user.id).values_list('liked', flat=True)
        for post in posts:
            count = Like.objects.filter(liked=post).count()
            post.likes = count
            post.like_status = 0
            if post.id in liked:
                post.like_status = 1
        
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        post = paginator.get_page(page)

        who = request.user
        who.info = datetime.now().strftime('%B %d, %Y, %I:%M %p')

        # User's entered parameter for post
        content = request.POST["content"]       
        image = 0
    
        if request.FILES:
            image = request.FILES["image"]

        # Throw an error if user tries to create an empty post
        if not content and not image:
            return render(request, "network/layout.html", {
                "message": "Cannot create empty posts.",
                "posts": post,
                "who": who
            })

        # Save created post into database
        if image:
            post = Post.objects.create(owner=request.user, content=content, image=image, info=datetime.now())
        else:
            post = Post.objects.create(owner=request.user, content=content, info=datetime.now())
        post.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))


# View to show user the posts created by himself only
@login_required
def your(request):

    # Get the posts created by the user and the like data per posts
    posts = Post.objects.all().filter(owner=request.user).order_by('-info')
    liked = Like.objects.filter(liker=request.user).values_list('liked', flat=True)
    for post in posts:
        count = Like.objects.filter(liked=post).count()
        post.likes = count
        post.like_status = 0
        if post.id in liked:
            post.like_status = 1

    # Use Django's Paginator class to restrict number of posts shown to 10 per page
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    post = paginator.get_page(page)

    # Send a clone of user data which will be replaced by another user's data whenever user visit's another user's profile 
    who = request.user
    who.info = datetime.now().strftime('%B %d, %Y, %I:%M %p')
    
    return render(request, "network/layout.html", {
        "posts": post,
        "who": who
    })


# View to send information about another user
@login_required
def user(request, id):

    # Obtain posts by the user who is visited and like information per post
    posts = Post.objects.all().filter(owner=id).order_by('-info')
    liked = Like.objects.filter(liker=request.user).values_list('liked', flat=True)
    for post in posts:
        count = Like.objects.filter(liked=post).count()
        post.likes = count
        post.like_status = 0
        if post.id in liked:
            post.like_status = 1
    
    # Use Django's Paginator class to restrict number of posts shown to 10 per page
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    
    # Send data about who's profile has been visited and current datetime data send via this dict to transfer it to javascript 
    who = User.objects.get(pk=id)
    who.info = datetime.now().strftime('%B %d, %Y, %I:%M %p')

    return render(request, "network/layout.html", {
        "posts": post,
        "who": who
    })


# View to process follow requests
@login_required
def follow(request):
    if request.method == "POST":
        # Extract users through json request
        follower = User.objects.get(pk=json.loads(request.body)['follower'])
        following = User.objects.get(pk=json.loads(request.body)['following'])

        # Remove if follower already follows following, else follow
        if Follow.objects.filter(follower=follower, follows=following).exists():
            Follow.objects.filter(follower=follower, follows=following).delete()
        else:
            Follow.objects.create(follower=follower, follows=following)
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


# View to send followers and following data for the requested user to the javascript file
@login_required
def followdata(request, id):
    # Extract user informations and get respective datas
    logger = request.user
    visited = User.objects.get(pk=id)
    followers = Follow.objects.filter(follows=visited).all()
    following = Follow.objects.filter(follower=visited).all()

    # Create a list to send the follow data to javascript file as Json file
    follower_list = []
    following_list = []
    status = False

    # Update every follower's follow status with respect to our logged in user
    for follower in followers:
        a = follower.follower

        # Check if our user follows that user's followers
        if Follow.objects.filter(follower=logger, follows=a).exists():
            a.status = True
        else:
            a.status = False

        pfp = str(a.pfp)
        if not a.pfp:
            pfp = "None"

        if a.id == logger.id:
            status = True

        # Update the json array
        something = {"id": a.id, "pfp": pfp, "username": a.username, "status": a.status}
        follower_list.append(something)
    
    # Update every following's follow status with respect to our logged in user
    for follower in following:
        a = follower.follows

        # Check if our user follows users which that user follows
        if Follow.objects.filter(follower=logger, follows=a).exists():
            a.status = True
        else:
            a.status = False

        pfp = str(a.pfp)
        if not a.pfp:
            pfp = "None"

        # Update the json array
        something = {"id": a.id, "pfp": pfp, "username": a.username, "status": a.status}
        following_list.append(something)

    # Sort follower and following list alphabetically
    follower_list.sort(key=operator.itemgetter('username'))
    following_list.sort(key=operator.itemgetter('username'))

    # Zip all the obtained data into dictionary for ease of transfer through JsonResponse
    dictionary = {"followers": follower_list, "following": following_list, "status": status, "follower_count": len(follower_list), "following_count": len(following_list)}
    return JsonResponse(dictionary, safe=False)


# View to update likes
@login_required
def like(request):
    if request.method == "POST":
        # Get user datas
        liker = request.user
        liked = Post.objects.get(pk=json.loads(request.body)['liked'])

        # Remove like if user unliked the post, else like
        if Like.objects.filter(liker=liker, liked=liked).exists():
            Like.objects.filter(liker=liker, liked=liked).delete()
        else:
            Like.objects.create(liker=liker, liked=liked)

        # Fetch how many likes are remaining on the post and send it to the javascript file
        count = Like.objects.filter(liked=liked).values_list('liker', flat=True)
        count = len(count)

        return JsonResponse({"likes": count})
    else:
        return HttpResponseRedirect(reverse("index"))
        

# View to show user the posts of people (s)he follows
@login_required
def feed(request):
    # Get followers of the user and all the posts they liked
    following = Follow.objects.filter(follower=request.user).values_list('follows', flat=True)
    posts = Post.objects.all().order_by('-info')
    liked = Like.objects.filter(liker=request.user).values_list('liked', flat=True)

    # Create an empty post object to append posts by followers later
    post_list = Post.objects.none()

    # Append posts by every follower into the post object
    for someone in following:
        post = Post.objects.filter(owner=someone)
        post_list = post_list | post

    # Order in reverse chronological order and update like data
    post_list = post_list.order_by('-info')
    for post in post_list:
        count = Like.objects.filter(liked=post).count()
        post.likes = count
        post.like_status = 0
        if post.id in liked:
            post.like_status = 1

    # Send a clone of user data which will be replaced by another user's data whenever user visit's another user's profile 
    who = request.user
    who.info = datetime.now().strftime('%B %d, %Y, %I:%M %p')
    
    return render(request, "network/layout.html", {
        "posts": post_list,
        "who": who,
        "liked": liked
    })


# View to fetch data of a post to javascript file in order to display the post completely, when clicked
def postdata(request):
    if request.method == "POST":
        # Get details of the post user wants to see
        post = Post.objects.get(pk=json.loads(request.body)['id'])
        liked = Like.objects.filter(liker=request.user.id).values_list('liked', flat=True)
        count = Like.objects.filter(liked=post).count()
        post.likes = count
        post.like_status = 0
        if post.id in liked:
            post.like_status = 1

        # Zip the post data into a dictionary in order to send as a JsonResponse Object
        req_post = {}
        req_post["id"] = post.id
        req_post["content"] = post.content
        req_post["info"] = post.info.strftime('%B %d, %Y, %I:%M %p')
        req_post["owner_id"] = post.owner.id
        req_post["owner_name"] = post.owner.username
        req_post["pfp"] = str(post.owner.pfp)
        req_post["image"] = str(post.image)
        req_post["likes"] = post.likes
        req_post["like_status"] = post.like_status
        
        return JsonResponse(req_post)
    else:
        return HttpResponseRedirect(reverse("index"))


# View accepting the edited that and replacing the pre-existing one
@login_required
def edit(request):
    if request.method == "POST":
        # Get the info that was being displayed on page initially, before user visited the page in order to get back there with an error
        posts = Post.objects.all().order_by('-info')
        liked = Like.objects.filter(liker=request.user.id).values_list('liked', flat=True)
        for post in posts:
            count = Like.objects.filter(liked=post).count()
            post.likes = count
            post.like_status = 0
            if post.id in liked:
                post.like_status = 1
        
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        post = paginator.get_page(page)

        who = request.user
        who.info = datetime.now().strftime('%B %d, %Y, %I:%M %p')
        
        # Get the submitted data
        content = request.POST["content"]       
        image = 0
        if request.FILES:
            image = request.FILES["image"]
        post_id = request.POST["post_id"]

        # Throw an error if user tries to create an empty post
        if not content and not image:
            return render(request, "network/layout.html", {
                "message": "Cannot create empty posts.",
                "posts": post,
                "who": who
            })

        # Get the object of the post which is to be edited and update it accordingly, deleting previous data. Then save the object
        foo = Post.objects.get(pk=post_id)
        if content:
            foo.content = content
        if image:
            foo.image.delete(False)
            foo.image = image
        foo.save()
    return HttpResponseRedirect(reverse("index"))

