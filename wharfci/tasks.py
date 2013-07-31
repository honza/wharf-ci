from celery import task
from docker.client import Client
import tempfile
from git import Repo
import shutil


@task
def run_build(build):
    prj = build.project
    # docker client
    c = Client(build.host)
    tmp_dir = tempfile.mkdtemp()
    # clone repo
    repo = Repo.clone_from(prj.repository, tmp_dir)
    g = repo.git
    # checkout commit from push
    g.checkout(build.commit_sha)
    repo_name = '/'.join(['wharfci', prj.name])
    image_name = ':'.join([repo_name, build.commit_sha])
    img_id, res = c.build(tmp_dir)
    # create image
    c.tag(img_id, repository=repo_name, tag=build.commit_sha)
    # cleanup
    shutil.rmtree(tmp_dir)
    # run build command from new image and report output
    container = c.create_container(image_name, prj.build_command,
        stdin_open=True, tty=True)
    container_id = container.get('Id')
    c.start(container_id)
    c.wait(container_id)
    out = c.logs(container_id)
    build.result = out
    build.save()
