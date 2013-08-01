from django.conf.urls import patterns, url

urlpatterns = patterns('web.views',
    url(r'^createproject/$', 'create_project', name='create_project'),
    url(r'^project/(?P<project_id>\d+)$', 'project_details',
        name='project_details'),
)
