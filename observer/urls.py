from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin


# 
# api REST endpoints (cfr glue app)
#
apipatterns = patterns('observer.api',
    url(r'^$', 'index'),
    url(r'^login/$', 'login_view', name='observer_login'),
    url(r'^access-denied/$', 'access_denied', name='observer_access_denied'),

    # REST for working-documents
    url(r'^working-document/$', 'workingDocuments', name='observer_working_documents'),
    url(r'^working-document/(?P<ids>[\d]+,[\d,]+)$', 'workingDocuments_by_ids', name='observer_workingDocuments_by_ids'),
    url(r'^working-document/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'workingDocument', name='observer_working_document'),
    
    # REST for document facets
    url(r'^document/facets$', 'documents_facets', name='observer_documents_facets'),
    
    # REST for document
    url(r'^document/$', 'documents', name='observer_documents'),
    url(r'^document/(?P<ids>[\d]+,[\d,]+)$', 'documents_by_ids', name='observer_documents_by_ids'),
    url(r'^document/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'document', name='observer_document'),
    
    # REST for devices (connector of document and working document)
    url(r'^device/$', 'devices', name='observer_devices'),
    url(r'^device/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'device', name='observer_device'),

    # REST for tags
    url(r'^tag/$', 'tags', name='observer_tags'),
    url(r'^tag/(?P<ids>[\d]+,[\d,]+)$', 'tags_by_ids', name='observer_tags_by_ids'),
    url(r'^tag/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'tag', name='observer_tag'),
    
    ##
    # SPECIAL FUNCTIONS BELOW
    # REST for biblib references
    url(r'^proxy/reference/$', 'proxy_reference', name='observer_proxy_reference'),

    # REST linking for m2m models
    url(r'^(?P<model_name>[:a-zA-Z_\-]+)/(?P<pk>[\d]+)/links/(?P<m2m_name>[:a-zA-Z_]+)/(?P<ids>[\d,]+)$', 'm2m_links', name='observer_m2m_links'),

    # graph bipartite for m2m relations
    url(r'^graph-bipartite/(?P<app_name>[:a-zA-Z_\-]+)/(?P<model_name>[:a-zA-Z_\-]+)/(?P<m2m_name>[:a-zA-Z_]+)/$', 'graph_bipartite', name='observer_graph_bipartite'),
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


handler403 = 'observer.api.access_denied'