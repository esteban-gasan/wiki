from django.http import Http404
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    entry =  util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
        })
    
    raise Http404("Entry not found")
