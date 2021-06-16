from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

class NewArticleForm(forms.Form):
    title = forms.CharField(label="Title: ")
    article = forms.CharField(label="Article", widget=forms.Textarea)

def index(request):
    """
    Displays the main page with all the wiki entries.
    """
    # it renders the index page with a dictionary including all the entries
    # from the entries folder.
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    """
    Displays the article by the title if it exists.
    Otherwise, it shows an error page.
    """
    # attempts to grab the entry by title
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "error": f"{title} entry does not exist."
        })
    
    # this renders the entry.html template by including the title and the entry text.
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })

def search(request):
    """
    It searches the page for an article by title.  It it matches an entry, it 
    displays it directly.  If the title matches more than one title, it shows
    all the entries by links.  Otherwise, if no matches are found, an error page
    is displayed.
    """
    # gets the q value from field
    title = request.GET['q']
    # tries to get entry for q.  if so, it loads that page.
    entry = util.get_entry(title)
    # if the entry is found, it redirects to the /wiki/title page.
    # it uses the HttpResponseRedirect object which uses the reverse function to
    # search for the wiki page by name, with arguments as the title.
    if entry:
        return HttpResponseRedirect(reverse('title', args=(title,)))
    # it tries in the rest of the entries for partial matches.
    entries = util.list_entries()
    matches = []
    for entry in entries:
        if entry.lower().find(title.lower()) >= 0:
            matches.append(entry)
    # if there are matches, we show the search page with a list of matches.
    if matches:
        return render(request, "encyclopedia/search.html", {
            "title": title,
            "matches": matches
        })
    # otherwise, we display an error page indicating there are no entries for the title.
    else:
        return render(request, "encyclopedia/error.html", {
            "error": f"There are no entries for '{title}'"
        })

def newpage(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            article = form.cleaned_data['article']
            if util.article_exists(title):
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "error": f"There is already an article for '{title}'"
                })                  
            util.save_entry(title, article)
            # after it saves the entry, it redirects to the index page
            # it doesn't use args because the 'index' route does not use one.
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form,
                "error": "Please review field content validity."
            })  
    return render(request, "encyclopedia/newpage.html", {
        "form": NewArticleForm()
    })

def edit(request, title):
    print(f"TITLE is {title}")
    if request.method == 'POST':
        form = NewArticleForm(request.POST)
        if form.is_valid():
            title_form = form.cleaned_data['title']
            article_form = form.cleaned_data['article']
            if title_form == title:
                util.save_entry(title, article_form)
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
                })
            else:
                return render(request, "encyclopedia/edit.html", {
                    "form": form,
                    "error": f"You can't change the article name."
                })
    if util.article_exists(title):
        form = NewArticleForm(initial = {
            "title": title,
            "article": util.get_entry(title)
        })
        # print(form)
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title #f"There is no article for '{title}'"
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "error": f"There is no article for '{title}'"
        })

def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('title', args=(title,)))
