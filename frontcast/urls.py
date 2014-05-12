from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin



admin.autodiscover()




api_urlpatterns = patterns('walt.api',
    url(r'^$', 'index'),
    url(r'access-denied/$', 'access_denied'),


    url(r'u/assignment/$', 'user_assignments', name='walt_api_user_assignments'),
    url(r'u/assignment/(?P<pk>\d+)/$', 'user_assignment', name='walt_api_user_assignment'),
    url(r'u/assignment/(?P<pk>\d+)/deliver/$', 'user_assignment_deliver', name='walt_api_user_assignment_deliver'),
    url(r'u/assignment/(?P<pk>\d+)/documents/$', 'user_assignment_documents', name='walt_api_user_assignment_documents'),

    url(r'u/(?P<username>[:a-zA-Z\.\-\d]+)/document/$', 'user_documents', name='walt_api_user_documents'),
    url(r'u/(?P<username>[:a-zA-Z\.\-\d]+)/document/filters/$', 'user_documents_filters', name='walt_api_user_documents_filters'),
    url(r'u/(?P<username>[:a-zA-Z\.\-\d]+)/document/(?P<slug>[:a-zA-Z_\-\d]+)$', 'user_document', name='walt_api_user_document'),

    url(r'r/document/$', 'reference_documents', name='walt_api_reference_documents'),
    url(r'r/document/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'reference_document', name='walt_api_reference_document'),

    # staff only: view all possible documents
    url(r'w/document/$', 'world_documents', name='walt_api_world_documents'),

    #staff only: graphs
    url(r'graph/bipartite/(?P<model_name>[:a-zA-Z_\-]+)/(?P<m2m_name>[:a-zA-Z_]+)/$', 'graph_bipartite', name='walt_api_graph_bipartite'),

     # staff only: working documents
    url(r'working-document$', 'working_documents', name='walt_api_working_documents'),
    url(r'working-document/filters$', 'working_documents_filters', name='walt_api_working_documents_filters'),
    url(r'working-document/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'working_document', name='walt_api_working_document'),
    url(r'working-document/(?P<pk>[:a-zA-Z\.\-\d]+)/attach-tags$', 'working_document_attach_tags', name='walt_api_working_document_attach_tags'),
    url(r'working-document/(?P<pk>[:a-zA-Z\.\-\d]+)/detach-tag/(?P<tag_pk>[:a-zA-Z\.\-\d]+)$', 'working_document_detach_tags', name='walt_api_working_document_attach_tags'),
    
    url(r'url/title$', 'url_title', name='walt_api_url_title'),

    url(r'document/$', 'documents', name='walt_api_documents'),
    url(r'document/filters$', 'documents_filters', name='walt_api_documents_filters'),
    url(r'document/(?P<pk>[:a-zA-Z\.\-\d]+)/$', 'document', name='walt_api_document'),
    url(r'document/(?P<pk>[:a-zA-Z\.\-\d]+)/attach-tags/$', 'document_attach_tags', name='walt_api_document_attach_tags'),
    url(r'document/(?P<pk>[:a-zA-Z\.\-\d]+)$', 'document', name='walt_api_update_document'),
    

    url(r'tag/$', 'tags', name='walt_api_tags'),
    

    url(r'biblib/$', 'biblib_proxy', name='walt_api_biblib_proxy'),
    url(r'biblib-safe/$', 'biblib_proxy_safe', name='walt_api_biblib_proxy_safe'), # user is not logged in! but requests are safe enough

    url(r'oembed/(?P<provider>[a-z]+)/$', 'oembed_proxy', name='walt_api_oembed_proxy'),
)





walt_urlpatterns = patterns('walt.views',
  #patterns('walt.views',
    # home
    url(r'^$', 'home', name='walt_home'),
    

    

    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    

    url(r'^d/$', 'document', name='walt_empty_document'), #i.e. user page
    url(r'^d/(?P<slug>[a-z\.-]+)/$', 'document', name='walt_document'), #i.e. user page
    url(r'^d/(?P<slug>[a-z\.\-\d]+)/edit/$', 'document_edit', name='walt_document_edit'), #i.e. user page


    url(r'^u/$', 'spiff', name='walt_empty_spiff'), #i.e. user page
    url(r'^u/(?P<username>[a-z\.]+)/$', 'spiff', name='walt_spiff'), #i.e. user page

    url(r'^t/(?P<pk>\d+)/$', 'task', name='walt_task'), #i.e. specific task assigned to a pedagogical unit via assignment
    #url(r'^robots\.txt$',  TemplateView.as_view(direct_to_template, {'template': 'frontcast/robots.txt', 'mimetype': 'text/plain'}),
    #//url(r'^humans\.txt$', direct_to_template, {'template': 'frontcast/humans.txt', 'mimetype': 'text/plain'}),
    # url(r'^crossdomain\.xml$', direct_to_template, {'template': 'frontcast/crossdomain.xml', 'mimetype': 'text/xml'}),

    
    url(r'^video/$', 'spiff_video', name='walt_video'), # add video metadata ? provide upload features.

    # admin only pages
    url(r'^setup/$', 'setup', name='walt_setup'), # add video metadata ? provide upload features.


    
    # url(r'^frontcast/', include(frontcast_urlpatterns))
)

urlpatterns = patterns('frontcast.views',
  url(r'^$', 'home', name='frontcast_home'),
  url(r'^scenario/$', 'scenario', name='frontcast_scenario'),

  url(r'^d/(?P<slug>[:a-zA-Z\.\-\d]+)/edit/$', 'document_edit', name='frontcast_document_edit'),
  url(r'^w/', include(walt_urlpatterns)),
  # restful api
  url(r'^api/', include(api_urlpatterns)),
  # test purpose glue
  url(r'^glue/', include('glue.urls')),

  url(r'^s/(?P<folder>[a-zA-Z\d\-]+)/(?P<index>[A-Za-z\-_\d]+)\.(?P<extension>[\.a-z\d]+)/$', 'storage', name='frontcast_storage'), #i.e. proxy to storage space

  # login / logout
  url(r'^logout/$', 'logout_view', name='frontcast_logout'),
  url(r'^login/$', 'login_view', name='frontcast_login'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^observer/', include('observer.urls')),
 # url(r'^ouch/$', 'not_found', name='not_found'),
)
