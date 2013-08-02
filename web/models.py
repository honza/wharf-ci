from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


BUILD_STATUS_CHOICES = (
    ('f', 'Fail',),
    ('s', 'Success',),
    ('q', 'Queued',),
    ('a', 'Aborted',),
    ('b', 'Building',),
)


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(default=datetime.utcnow)
    created_by = models.ForeignKey(User)
    repository = models.CharField(max_length=255)
    build_command = models.TextField()
    dockerfile = models.TextField(default='Dockerfile')
    private = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)


class Pusher(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Build(models.Model):
    project = models.ForeignKey(Project)
    pusher = models.ForeignKey(Pusher)
    created = models.DateTimeField(default=datetime.utcnow)
    commit_sha = models.CharField(max_length=40)
    commit_timestamp = models.DateTimeField()
    host = models.CharField(max_length=255, default='localhost')
    status = models.CharField(max_length=1, choices=BUILD_STATUS_CHOICES,
                              default='q')
    result = models.TextField(default='')
    return_code = models.IntegerField(default=-1, null=True)

    def __unicode__(self):
        return self.commit_sha

    @property
    def is_success(self):
        return self.status == 's'
