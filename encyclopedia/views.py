from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render

from random import choice

from . import util


class CreateEntryForm(forms.Form):
    entry_title = forms.CharField(label="Entry title", max_length=255)
    entry_content = forms.CharField(label="Content", widget=forms.Textarea)

    def clean_entry_title(self):
        data = self.cleaned_data["entry_title"]
        if util.get_entry(data):
            raise ValidationError(f"Error: '{data}' already exists")

        return data

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


def new(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entry_title"]
            if not util.get_entry(title):
                content = f"# {title}\n\n{form.cleaned_data['entry_content']}"
                util.save_entry(title, content)
                return redirect("entry", title=title)
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            }) 

    return render(request, "encyclopedia/new.html", {
        "form": CreateEntryForm()
    }) 


def random(request):
    page = choice(util.list_entries())
    return redirect("entry", title=page)
   