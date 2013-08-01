from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

def index(request):
    ctx = {}
    # show dashboard if logged in
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))
    return render_to_response('index.html', ctx,
        context_instance=RequestContext(request))
