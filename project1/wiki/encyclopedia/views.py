from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from random import choice

from . import util

# preloaded function
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# function to facilitate content showcasing of any requested entry.
def title(request, name):

    # dictionary created for easily sending entry data to HTML when rendering.
    send = {}
    send["show"] = util.get_entry(name)
    send["title"] = name

    # checking if any entry with requested title is available. if no, error page is rendered.
    if send["show"] == None:
        error = {}
        error["code"] = 404
        error["message"] = "Not Found"
        return render(request, "encyclopedia/error.html", {
            "error": error
        })
    
    # converting received markdown content into html
    markdowner = Markdown()
    send["show"] = markdowner.convert(send["show"])

    # rendering template to showcase contents of requested file
    return render(request, "encyclopedia/show.html", {
        "received": send
    })
    

# function to facilitate addition of new pages/entries
def add(request):

    # if the user reaches vaya POST i.e. through filling up the add form
    if request.method == "POST":

        # accepting new title and content data entered by the user
        title = request.POST["title"]
        content = request.POST["content"]

        # checking if an entry with the same name already exists. If yes, renders error page
        if title in util.list_entries():
            error = {"code": "403", "message": "Another page with this title already exists."}
            return render(request, "encyclopedia/error.html", {
                "error": error
            })
        
        # if no such entry with the same name exists, new entry is created and user is redirected home.
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))

    # user reached vaya GET i.e. by redirection or clicking links
    else:
        return render(request, "encyclopedia/add.html")
    

# function to edit the contents of a pre-existing entry
def edit(request):

    # if the user reaches vaya POST i.e. through filling up the edit form
    if request.method == "POST":

        # accepting edited content data entered by the user and saving it 
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)

        # converting markdown file to html for rendering the updated contents of the same page 
        markdowner = Markdown()
        content = markdowner.convert(content)
        received = {"title": title, "show": content}
        return render(request, "encyclopedia/show.html", {
                "received": received
            })
    
    # if the user reaches vaya GET that is through redirection or by clicking on the links
    else:

        # accepting which entry is going to be edited and taking user to the editable page
        title = request.GET["title"]
        content = util.get_entry(title)
        page = {"title": title, "content": content}
        return render(request, "encyclopedia/edit.html", {
            "page": page
        })
    

# function to select a random entry and showcase it by calling wiki/<title>    
def rand(request):
    name = choice(util.list_entries())
    return title(request, name)


# function to search entries with the help of the searchbox
def search(request):

    # accepting the keyword that is to be searched, if no keyword is entred, user is redirected home
    q = request.POST["q"]
    if not q:
        return HttpResponseRedirect(reverse("index"))

    # getting entries in a list to compare with the received keyword
    list = util.list_entries()
    slist = {"title": q}
    found = []
    error = {"code": "404", "message": "Please try with a different search input."}
    mkd = util.get_entry(q)
    
    # checking if keyword matches exactly, partially or not at all with any entry title
    q = q.lower()
    for entry in list:

        # if keyword matches exactly, user is directed to that entry
        if q == entry.lower():
            markdowner = Markdown()
            mkd = markdowner.convert(mkd)
            received = {"title": q, 'show': mkd}
            return render(request, "encyclopedia/show.html", {
                "received": received
            })
        if q in entry.lower():
            found.append(entry)

    # if keyword matches partially, list of matching entriess is displayed
    slist["entries"] = found
    if found:
        return render(request, "encyclopedia/search.html", {
            "list": slist
        })
    
    # if keyword does not match at all, error page is displayed
    else:
        return render(request, "encyclopedia/error.html", {
            "error": error
        })