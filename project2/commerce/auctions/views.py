from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from datetime import datetime
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, List, Comment, Watchlist, Category, Bid

# Form for creating a new list
class create_list_form(forms.Form):
    title = forms.CharField(label='Title', max_length=64, widget=forms.TextInput(attrs={"placeholder":"Heading of your listing"}))
    description = forms.CharField(label='Description', max_length=200, widget=forms.Textarea(attrs={"placeholder":"We recommend describing your item in detail for higher chances of bids"}))
    min_bid = forms.DecimalField(label='Starting Bid', max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={"placeholder":"(in USD)"}))
    image_link = forms.URLField(label='Image url', required=False, widget=forms.TextInput(attrs={"placeholder": "Please check your url is working before uploading as it may alter probability of higher bids"}))
    category = forms.CharField(label='Category', max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': "(enter only one category)"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('min_bid', css_class='form-group col-md-2 mb-0'),
                Column('category', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'description',
            'image_link',
            Submit('submit', 'Submit', css_class="btn btn-light btn-outline-dark")
        )


# Active listings
def index(request):

    # Join multiple models to send appropriate table to the template
    lists = Bid.objects.all().select_related('post').select_related('bidder').order_by('-id')  
    return render(request, "auctions/index.html", {
        "lists": lists
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

# Create a new listing
def create(request):
    # User reached by submitting form
    if request.method == "POST":
        form = create_list_form(request.POST)

        print("Entered Create(via post)")
        # Form input validity
        if form.is_valid():
            owner = request.user
            
            # Update the appropriate models. Assign hero image if none exists
            if form.cleaned_data['image_link']:
                something = List.objects.create(title = form.cleaned_data['title'], description = form.cleaned_data['description'], min_bid = form.cleaned_data['min_bid'], image_link = form.cleaned_data['image_link'], listed_on = datetime.now(), owner = owner)
            else:
                something = List.objects.create(title = form.cleaned_data['title'], description = form.cleaned_data['description'], min_bid = form.cleaned_data['min_bid'], image_link = 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637', listed_on = datetime.now(), owner = owner)
                
            Bid.objects.create(post = something, bidder = request.user, bid = form.cleaned_data['min_bid'])
            if form.cleaned_data['category']:    
                Category.objects.create(post = something, category = form.cleaned_data['category'])

            return HttpResponseRedirect(reverse('index'))
        
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
        
    else:
        # Entered Create via GET
        return render(request, "auctions/create.html", {
                "form": create_list_form()
            })
    

# Watchlist
@login_required
def watchlist(request):

    # Join multiple models to send appropriate table to the template
    lists = Watchlist.objects.filter(holder = request.user).select_related('holding')    
    return render(request, "auctions/watchlist.html", {
        "lists": lists
    })
