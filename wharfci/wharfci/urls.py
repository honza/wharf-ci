from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wharfci.views.home', name='home'),
    # url(r'^wharfci/', include('wharfci.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
