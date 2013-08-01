from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login as login_user,
    logout as logout_user)
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
try:
    import simplejson as json
except ImportError:
    import json

DANGER = 40
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login_user(request, user)
                return redirect(reverse('index'))
            else:
                messages.add_message(request, DANGER, _('Your account is disabled.  Make sure you have activated your account.'))
        else:
            messages.add_message(request, DANGER, _('Invalid username/password'))
    return render_to_response('accounts/login.html',
        context_instance=RequestContext(request))

def logout(request):
    logout_user(request)
    return redirect(reverse('index'))

