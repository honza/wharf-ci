import json
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from models import Project, Build, Pusher
from tasks import run_build


def parse_github_timestamp(s):
    """
    2013-07-31T12:15:57-07:00
    """
    delta = timedelta(hours=int(s[20:22]), minutes=int(s[23:25]))

    if s[19] == '-':
        tz = 1 * delta
    else:
        tz = -1 * delta

    return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S") + tz


@csrf_exempt
def webhook_handler(request, project_pk):
    """
    * Verify that the project exists
    * Create a new Build
    """
    project = get_object_or_404(Project, pk=project_pk)

    payload = json.loads(request.POST.get('payload'))

    pusher_json = payload.get('pusher')
    pusher, _ = Pusher.objects.get_or_create(
        email=pusher_json.get('email'),
        name=pusher_json.get('name'))

    after = payload.get('after')
    latest_commit = None

    for commit in payload.get('commits'):
        if commit['id'] == after:
            latest_commit = commit
            break

    if not commit:
        return HttpResponseBadRequest()

    timestamp = latest_commit.get('timestamp', None)
    timestamp = parse_github_timestamp(timestamp)

    build = Build.objects.create(
        project=project,
        pusher=pusher,
        commit_sha=after,
        commit_timestamp=timestamp)

    run_build.delay(build)

    return HttpResponse()

@login_required
def dashboard(request):
    ctx = {}
    return render_to_response('dashboard.html', ctx,
        context_instance=RequestContext(request))
