from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


BUILD_STATUS_CHOICES = (
    ('f', 'Fail',),
    ('s', 'Success',),
    ('q', 'Queued',),
    ('a', 'Aborted',),
    ('b', 'Building',),
)


class Project(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.utcnow)
    created_by = models.ForeignKey(User)
    repository = models.CharField(max_length=255)
    build_command = models.TextField()
    dockerfile = models.TextField()
    private = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Pusher(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Build(models.Model):
    project = models.ForeignKey(Project)
    pusher = models.ForeignKey(Pusher)
    created = models.DateTimeField(default=datetime.utcnow)
    git_sha = models.CharField(max_length=40)
    git_timestamp = models.DateTimeField()
    status = models.CharField(max_length=1, choices=BUILD_STATUS_CHOICES,
                              default='q')

    def __unicode__(self):
        return self.git_sha

    @property
    def is_success(self):
        return self.status == 's'
