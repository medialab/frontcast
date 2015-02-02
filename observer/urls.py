from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin


# 
# api REST endpoints (cfr glue app)
#
apipatterns = patterns('observer.api',
    url(r'^$', 'index'),
    #url(r'access-denied/$', 'access_denied'),
    # REST for document side
    url(r'document/$', 'documents', name='observer_documents'),
    url(r'document/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'document', name='observer_document'),
    # REST for devices
    url(r'device/$', 'devices', name='observer_devices'),
    url(r'device/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'device', name='observer_device')
)


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    
    url(r'^glue/', include('glue.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # api patterns
    url(r'^api/', include(apipatterns)),

    # storage proxy
    url(r'^s/(?P<folder>[a-zA-Z\d\-]+)/(?P<index>[A-Za-z\-_\d]+)\.(?P<extension>[\.a-z\d]+)/$', 'storage', name='frontcast_storage'), #i.e. proxy to storage space
)
