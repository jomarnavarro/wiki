from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    print(title)
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "error": f"{title} entry does not exist."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })

def search(request):
    # gets the q value from field
    title = request.GET['q']
    # tries to get entry for q.  if so, it loads that page.
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })
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
