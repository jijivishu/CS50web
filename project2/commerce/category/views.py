from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions import models

# Category List
def categories(request):
    
    # Display distinct categories
    return render(request, "auctions/category.html", {
        "lists": models.Category.objects.values('category').distinct().order_by('category')
    })


# Specific listings as per the chosen category
def cat(request, cat):

    # Join multiple models to send appropriate table to the template
    lists = models.Category.objects.filter(category=cat).select_related('post').order_by('-id')  
    return render(request, "auctions/cat.html", {
        "lists": lists,
        "cat": cat
    })