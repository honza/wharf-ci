from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    ctx = {}
    return render_to_response('index.html', ctx,
        context_instance=RequestContext(request))
