from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "error": f"{title} entry does not exist."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })

