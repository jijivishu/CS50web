from auctions import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from datetime import datetime
from decimal import Decimal
from django.forms import ModelForm, Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Form for accepting comments
class CommentForm(ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 3, 'rows': 2, 'placeholder': 'Type your comment here'}),
        }


# List Item
def item(request, id):

    # User either commented or placed a bid
    if request.method == "POST":

        # Validate received comment and update appropriate models
        form = CommentForm(request.POST)
        if form.is_valid:
            object = form.save(commit=False)
            object.commentator = request.user
            object.title = models.List.objects.get(pk=id)
            object.comment_time = datetime.now()
            object.save()
        else:
            print(form.errors)

        return HttpResponseRedirect(reverse("item", args=(id,)))
        

    # User reached via redirection or by clicking a url
    else:

        # Update template with item details
        mod = models.List.objects.prefetch_related('cat_post', 'bid_post', 'com_title').get(pk=id)
        message = ''
        match = False

        # Special variable to keep check of new bids by the user
        max = mod.bid_post.values('bid')[0]['bid'] + Decimal(0.01)

        # Show commentting and bidding facility only when logged in
        if request.user.is_authenticated:
            comment = CommentForm()

            if models.Watchlist.objects.filter(holder=request.user, holding=id).exists():
                message = "Remove from"
            else:
                message = "Add to"

            if models.List.objects.filter(pk=id, owner = request.user).exists():
                match = True
            else:
                match = False
        else:
            comment=""

        return render(request, "auctions/item.html", {
                "list": mod,
                "comment": comment,
                "message": message,
                "match": match,
                "max": max
            })
        

#Adding to watchlist
def watch(request, id):
    post_id = id
    user_id = request.user

    # Remove if already present in Watchlist, otherwise Add
    if models.Watchlist.objects.filter(holder=user_id, holding=post_id).exists():
        models.Watchlist.objects.filter(holder=user_id, holding=post_id).delete()
    else:
        models.Watchlist.objects.create(holder=user_id, holding=models.List.objects.get(pk=id))

    return HttpResponseRedirect(reverse("item", args=(post_id,)))


#Closing the current listing
def close(request, id):
    obj = models.List.objects.get(pk=id)
    obj.status = False
    obj.save()
    return HttpResponseRedirect(reverse("item", args=(id,)))


#Save a bidding
def bidding(request, id):

    new_bid = request.POST['new_bid']

    # Replace old bid with new one
    if models.Bid.objects.filter(post=id).exists():
        models.Bid.objects.filter(post=id).delete()
    something = models.Bid.objects.create(post = models.List.objects.get(pk=id), bid = new_bid, bidder = request.user)
    
    return HttpResponseRedirect(reverse("item", args=(id,)))
