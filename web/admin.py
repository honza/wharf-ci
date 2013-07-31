from django.contrib import admin

from models import Project, Pusher, Build

admin.site.register(Project)
admin.site.register(Pusher)
admin.site.register(Build)
