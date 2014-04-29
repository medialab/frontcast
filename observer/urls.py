from django.conf.urls import patterns, include, url



apipatterns = patterns('observer.api',
  url(r'^$', 'index'),
  url(r'document-profile$', 'document_profiles'),
  url(r'document-profile/(?P<document_pk>[:a-zA-Z\.\-\d]+)$', 'document_profile'),
  url(r'device$', 'devices'),
  url(r'device/(?P<pk>\d+)$', 'device'), 
)

urlpatterns = patterns('observer.views',
  url(r'^$', 'index'),
  url(r'^api/', include(apipatterns)),
)