import os
import logging

from celery import task
from docker.client import Client
from git import Repo

from django.conf import settings


logger = logging.getLogger(__name__)
REPOSITORY_DIR = getattr(settings, 'REPOSITORY_DIR', None)


@task
def run_build(build):
    project = build.project

    # docker client
    c = Client(build.host)

    project_dir = os.path.join(REPOSITORY_DIR, project.slug)
    main_repo_path = os.path.join(project_dir, 'clone')

    if not os.path.exists(main_repo_path):

        # assert project repo present
        os.path.makedirs(project_dir)

        # clone repo
        repo = Repo.clone_from(project.repository, main_repo_path)

    else:
        repo = Repo(main_repo_path)
        remote = repo.remote()
        remote.pull()

    # build_path is a local clone of the project and it's named after the
    # current build's commit sha
    build_path = os.path.join(project_dir, build.commit_sha)
    repo = Repo.clone_from(main_repo_path, build_path)
    g = repo.git

    g.checkout(build.commit_sha)

    image_name = ':'.join([project.slug, build.commit_sha])

    img_id, res = c.build(build_path)

    # create image
    c.tag(img_id, repository=project.slug, tag=build.commit_sha)

    # run build command from new image and report output
    container = c.create_container(image_name, project.build_command,
                                   stdin_open=True, tty=True)

    container_id = container.get('Id')

    c.start(container_id)
    c.wait(container_id)

    out = c.logs(container_id)
    build.result = out
    build.save()

    # TODO: Update build status based on exit code
