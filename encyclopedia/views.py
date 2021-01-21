from django.http import Http404
from django.shortcuts import redirect, render

from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    entry =  util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry,
        })
    
    raise Http404("Page not found")

def random(request):
    page = choice(util.list_entries())
    return redirect("entry", title=page)

def search(request):
    if request.method == "GET":
        query = request.GET.get("q")
        if query:
            query_lower = query.lower()
            entries = util.list_entries()
            results = []

            for entry in entries:
                entry_lower = entry.lower()
                if query_lower == entry_lower:
                    return redirect("entry", title=entry)
                elif query_lower in entry_lower:
                    results.append(entry)
            
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "results": results,
                "total": len(results)
            })
    
        else:
            return render(request, "encyclopedia/search.html")
    