from django.conf.urls.defaults import *
from settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
print MEDIA_ROOT
urlpatterns = patterns('',
    (r'^$', include('likebanana.bananadeployer.urls')),
    (r'^show_log/?$', 'bananadeployer.views.show_log'),
    (r'^site_media/(?P<path>.*)$',      'django.views.static.serve', {'document_root': MEDIA_ROOT}),

)
