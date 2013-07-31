from django.shortcuts import get_object_or_404
from django.http import HttpReponse

from models import Project, Build, Pusher
from tasks import run_build


def webhook_handler(request, project_pk):
    """
    * Verify that the project exists
    * Create a new Build
    """
    project = get_object_or_404(Project, pk=project_pk)

    payload = request.POST.get('payload')

    pusher_json = payload.get('pusher')
    pusher, _ = Pusher.objects.get_or_create(
        email=pusher_json.get('email'),
        name=pusher_json.get('name'))

    build = Build.objects.create(
        project=project,
        pusher=pusher,
        git_sha=payload.get('after'))

    run_build.delay(build)

    return HttpReponse()
