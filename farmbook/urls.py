from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bookkeeper.views.show', name='home'),
    url(r'^bookkeeper/', include('bookkeeper.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^process/', 'bookkeeper.views.process'),
    )
