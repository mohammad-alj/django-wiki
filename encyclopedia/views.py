from django.shortcuts import render
from django.http import HttpRequest
from .util import get_entry


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(req: HttpRequest, entry: str):
    return render(req, 'encyclopedia/entry.html', {'entry_name': entry, 'entry_content': get_entry(entry)})

