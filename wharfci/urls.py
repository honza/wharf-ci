from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'wharfci.views.index', name='index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^webhook/(?P<project_pk>[0-9])$', 'web.views.webhook_handler',),
    url(r'^admin/', include(admin.site.urls)),
)
