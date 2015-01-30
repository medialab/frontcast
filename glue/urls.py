from django.conf.urls import patterns, url

urlpatterns = patterns('glue.api',
  url(r'access-denied/$', 'access_denied'),
  url(r'^$', 'index'),
  url(r'(?P<app_name>[:a-zA-Z_]+)/(?P<model_name>[:a-zA-Z_]+)$', 'get_objects'),
  url(r'(?P<app_name>[:a-zA-Z_]+)/(?P<model_name>[:a-zA-Z_]+)/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'get_object'),
  url(r'(?P<app_name>[:a-zA-Z_]+)/(?P<model_name>[:a-zA-Z_]+)/(?P<pk>[:a-zA-Z\.\-\d]+)/(?P<m2m_name>[:a-zA-Z_]+)$', 'get_object_m2m'),
)