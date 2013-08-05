import json
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _

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
    pusher = Pusher.objects.get_or_create(
        email=pusher_json.get('email'),
        name=pusher_json.get('name'))[0]

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
    ctx = {
        'projects': Project.objects.filter(
            created_by=request.user).order_by('name'),
    }
    return render_to_response('dashboard.html', ctx,
                              context_instance=RequestContext(request))


@login_required
@require_http_methods(['POST'])
def create_project(request):
    name = request.POST.get('name')
    repository = request.POST.get('repository')
    build_command = request.POST.get('build_command')
    # validate
    if not name or not repository or not build_command:
        messages.error(request, _('You must specify a name, repository,'
                                  ' and build command.'))
    else:
        # create project
        project = Project(name=name, repository=repository,
                          build_command=build_command, created_by=request.user)
        project.save()
        messages.success(request,
                         '{} {}'.format(name, _('project created...')))
    return redirect(reverse('dashboard'))


@login_required
def project_details(request, project_id=None):
    project = Project.objects.get(pk=project_id)
    ctx = {
        'project': project,
        'builds': project.build_set.all().order_by('-created')
    }
    return render_to_response('projects/_project.html', ctx,
                              context_instance=RequestContext(request))
