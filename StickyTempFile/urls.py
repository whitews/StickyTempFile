from django.conf.urls import patterns, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('uploader.urls')),
    (r'^admin/', include(admin.site.urls)),
)
