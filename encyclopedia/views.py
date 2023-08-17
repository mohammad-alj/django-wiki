from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from markdown2 import markdown
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(req: HttpRequest, entry: str):
    content = util.get_entry(entry)
    if not content:
        return render(req, 'encyclopedia/error.html', {'code': 404, 'message': 'entry not found.'})
    return render(req, 'encyclopedia/entry.html', {'entry_name': entry, 'entry_content': markdown(util.get_entry(entry))})


def search(req: HttpRequest):
    if req.method == 'GET':
        q = req.GET['q']
        if not q or len(q) > 75:
            return render(req, 'encyclopedia/error.html', {'code': 403, 'message': 'Query must be atleast 75 characters long.'})
        
        entries = util.list_entries()
        simular_entries = []
        for entry in entries:
            if q.lower() == entry.lower():
                return HttpResponseRedirect(f'/wiki/{entry}', {'entry_name': entry, 'entry_content': util.get_entry(entry)})
            if q.lower() in entry.lower():
                simular_entries.append(entry)
                

        # no entries match strictly...

        # check if any entries are simular to query
        print(simular_entries)
        if len(simular_entries) > 0:
            return render(req, 'encyclopedia/search_results.html', {'entries': simular_entries})
        else:
            # nothing found...
            return render(req, 'encyclopedia/error.html', {'code': 404, 'message': 'entry not found.'})

def new_page(req: HttpRequest):
    if req.method == 'POST':
        name = req.POST['name']
        content = req.POST['content']
        
        # check name
        if not name or len(name) > 75:
            return render(req, 'encyclopedia/error.html', {'code': 403, 'message': 'Name is required and should be less than 75 or greater.'})

        # check content
        if not content or len(content) < 30:
            return render(req, 'encyclopedia/error.html', {'code': 403, 'message': 'Content must be at least 30 characters.'})
        
        # all good
        util.save_entry(name, content)
        return HttpResponseRedirect('/')
    return render(req, 'encyclopedia/new_page.html', {'name': '', 'content': ''})


def edit_page(req: HttpRequest, entry):
    entries = util.list_entries()
    if entry not in entries:
        return render(req, 'encyclopedia/error.html', {'code': 404, 'message': 'Entry does\'t exit.'})
    
    if req.method == 'POST':
        content = req.POST['content']

        # check content
        if not content or len(content) < 30:
            return render(req, 'encyclopedia/error.html', {'code': 403, 'message': 'Content must be at least 30 characters.'})
        
        # all good
        util.save_entry(entry, content)
        return HttpResponseRedirect('/')
    
    return render(req, 'encyclopedia/edit_page.html', {'name': entry, 'content': util.get_entry(entry)})


def random(req: HttpRequest):
    return HttpResponseRedirect(f'/wiki/{choice(util.list_entries())}')