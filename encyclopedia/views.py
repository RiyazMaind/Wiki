from django.shortcuts import redirect, render
from django import forms

import random

from . import util

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {"message": "The requested page was not found."})
    html_content = markdown2.markdown(entry_content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get('q', '').strip()
    if query:
        entries = util.list_entries()
        if query.lower() in [entry.lower() for entry in entries]:
            return redirect('entry', title=query)
        else:
            results = [entry for entry in entries if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "results": results
            })
    else:
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": []
        })

    
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="content")

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": "An entry with this title already exists."
                })
            util.save_entry(title, content)
            return redirect("entry", title=title)
    else:
        form = NewEntryForm()
    return render(request, "encyclopedia/create.html", {
        "form": form
    })

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('entry', title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })
        form = EditPageForm(initial={'content': content})
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    })
        
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", title = random_entry)


