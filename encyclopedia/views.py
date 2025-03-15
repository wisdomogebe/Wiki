from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
import random

from . import util
from .util import get_entry, list_entries

# The index view which renders the hompage. It displays the list of all entries in the encyclopedia.
def index(request):
    # This block created to handle the search form action with GET request method. 
    if request.GET:
        entries = list_entries()
        entry_title = request.GET["q"].strip()

        if entry_title:

            # If the entry exists, the user is redirected to the entry's page.
            if entry_title in entries:
                return HttpResponseRedirect(reverse(entry, args=[entry_title]))
            
            #
            elif entry_title == "#random#":
                entry_title = random.choice(list_entries())
                return HttpResponseRedirect(reverse(entry, args=[entry_title]))
        
            # If the entry does not exist, the user is directed to a page that lists out all the entries that has the entry as a substring.
            else:
                return render(request, "encyclopedia/search.html", {
                    "title": entry_title,
                    "entries": list_entries(),
                })
    # Render the Hompage of the encyclopedia.
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# The entry view that diplays the encyclopedia entry to the user if it exists else it displays an error page
def entry(request, entry_title):
    contents = get_entry(entry_title)
    if contents:
        # We need to do the conversion from MARKDOWN to HTML here.
        contents = markdown2.markdown(contents)
        return render(request, "encyclopedia/entry.html", {
            "title": entry_title,
            "body" : contents
        })
    

    else:
        # Display the page that tells the user that the requested entry does not exist
       return render(request, "encyclopedia/no_entry.html", {
           "title": entry_title.capitalize()
       })

# The create view that renders the page where the user can create a new entry.
def create(request):
    if request.POST:
        title = request.POST["title"]
        content = request.POST["content"]
        if title in list_entries():
            return render(request, "encyclopedia/create_error.html", {
                "title": title,
            }) 
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse(entry, args=[title]))
    return render(request, "encyclopedia/create.html")

# The edit view handles editing of an entry page
def edit(request):
    # Saves the new edited page to disk
    if request.POST:
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse(entry, args=[title]))
    
    # Renders the edit page with the initial contents of the entry page
    title = request.GET["title"]
    content = request.GET["content"]
    return render(request, "encyclopedia/create.html", {
        "initial_title": title,
        "initial_content": content,
    })
