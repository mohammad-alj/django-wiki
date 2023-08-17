from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from markdown2 import markdown


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(req: HttpRequest, entry: str):
    content = util.get_entry(entry)
    if not content:
        return render(req, 'encyclopedia/error.html', {'error_message': '404 entry not found'})
    return render(req, 'encyclopedia/entry.html', {'entry_name': entry, 'entry_content': markdown(util.get_entry(entry))})


def search(req: HttpRequest):
    if req.method == 'GET':
        q = req.GET['q']
        if not q or len(q) > 75:
            return render(req, 'encyclopedia/error', {'error_message': 'Query must be atleast 75 characters long.'})
        
        entries = util.list_entries()
        for entry in entries:
            if q.lower() == entry.lower():
                return HttpResponseRedirect(f'/wiki/{entry}', {'entry_name': entry, 'entry_content': util.get_entry(entry)})

        return HttpResponse(req.GET['q'])
