from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from markdown2 import markdown
from .util import get_entry



from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(req: HttpRequest, entry: str):
    content = get_entry(entry)
    if not content:
        return render(req, 'encyclopedia/error.html', {'error_message': '404 entry not found'})
    return render(req, 'encyclopedia/entry.html', {'entry_name': entry, 'entry_content': markdown(get_entry(entry))})


def search(req: HttpRequest):
    if req.method == 'GET':
        q = req.GET['q']
        if not q:
            return HttpResponseRedirect('/')
        return HttpResponse(req.GET['q'])
