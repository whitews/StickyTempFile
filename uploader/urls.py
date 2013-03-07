from django.conf.urls import patterns, url

from uploader.api_views import *

# API routes
urlpatterns = patterns(
    'uploader.api_views',
    url(r'^api/$', 'api_root'),
    url(r'^api/files/$', UploadedFileList.as_view(), name='uploadedfile-list'),
    url(r'^api/files/(?P<pk>\d+)/$', UploadedFileDetail.as_view(), name='uploadedfile-detail'),
)

# Regular web routes
urlpatterns += patterns(
    'uploader.views',
    url(r'^$', 'view_files', name='view_files'),
    url(r'^files/add/$', 'add_file', name='add_file'),
)
