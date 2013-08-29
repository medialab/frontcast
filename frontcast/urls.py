from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # home
    url(r'^$', 'walt.views.home', name='walt_home'),

    # login / logout
    url(r'^logout/$', 'walt.views.logout_view', name='walt_logout'),
    url(r'^login/$', 'walt.views.login_view', name='walt_login'),

    # url(r'^frontcast/', include('frontcast.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^u/(?P<username>[a-z\.]+)/$', 'walt.views.spiff', name='walt_spiff'), #i.e. user page
    #url(r'^robots\.txt$',  TemplateView.as_view(direct_to_template, {'template': 'frontcast/robots.txt', 'mimetype': 'text/plain'}),
    #//url(r'^humans\.txt$', direct_to_template, {'template': 'frontcast/humans.txt', 'mimetype': 'text/plain'}),
    # url(r'^crossdomain\.xml$', direct_to_template, {'template': 'frontcast/crossdomain.xml', 'mimetype': 'text/xml'}),


    url(r'^video/$', 'walt.views.spiff_video', name='walt_video'), # add video metadata ? provide upload features.

    # admin only pages
    url(r'^setup/$', 'walt.views.setup', name='walt_setup'), # add video metadata ? provide upload features.
)
