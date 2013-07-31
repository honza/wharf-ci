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
    created_by = models.Foreign(User)
    repository = models.CharField(max_length=255)
    build_command = models.TexField()
    dockerfile = models.TexField()
    private = models.BooleanField(default=False)


class Pusher(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)


class Build(models.Model):
    project = models.ForeignKey(Project)
    pusher = models.ForeignKey(Pusher)
    created = models.DateTimeField(default=datetime.utcnow)
    git_sha = models.CharField(max_length=40)
    git_timestamp = models.DateTimeField()
    status = models.CharField(max_length=1, choices=BUILD_STATUS_CHOICES,
                              default='q')

    @property
    def is_success(self):
        return self.status == 's'
