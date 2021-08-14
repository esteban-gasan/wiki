from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render

import markdown2
import random
import re

from . import util


class CreateEntryForm(forms.Form):
    entry_title = forms.CharField(label="Title", max_length=255, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    entry_content = forms.CharField(label="Content", widget=forms.Textarea(
        attrs={"class": "form-control", "rows": "15"}))

    def clean_entry_title(self):
        data = self.cleaned_data["entry_title"]
        if util.get_entry(data):
            raise ValidationError(f"Error: '{data}' already exists")

        return data


class EditEntryForm(forms.Form):
    content = forms.CharField(label=False, widget=forms.Textarea(
        attrs={"class": "form-control", "rows": "15"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    entry = util.get_entry(title)
    if not entry:
        raise Http404("Page not found")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry)
    })


def edit_entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        raise Http404(f"'{title}' does not exist")

    pattern = re.compile(r"^# .+")
    title_part = re.findall(pattern, entry)[0]

    if request.method == "GET":
        # Accessing the edit page
        content_part = re.sub(pattern, "", entry).strip()
        data = {"content": content_part}
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": EditEntryForm(initial=data)
        })

    elif request.method == "POST":
        # Submitting the form
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = f"{title_part}\n\n{form.cleaned_data['content']}\n"
            util.save_entry(title, content.encode())
            return redirect("encyclopedia:entry", title=title)
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })


def search(request):
    if request.method != "GET":
        return

    query = request.GET.get("q")
    if not query:
        return render(request, "encyclopedia/search.html")

    query_lower = query.lower()
    entries = util.list_entries()
    results = []

    for entry in entries:
        entry_lower = entry.lower()
        if query_lower == entry_lower:
            return redirect("encyclopedia:entry", title=entry)
        elif query_lower in entry_lower:
            results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results,
        "total": len(results)
    })


def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "form": CreateEntryForm()
        })

    elif request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entry_title"]
            content = f"# {title}\n\n{form.cleaned_data['entry_content']}\n"
            util.save_entry(title, content)
            return redirect("encyclopedia:entry", title=title)
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })


def random(request):
    page = random.choice(util.list_entries())
    return redirect("encyclopedia:entry", title=page)
