import logging, os, urllib
from mimetypes import guess_type

from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from glue.utils import Epoxy

from walt.forms import LoginForm
from walt.models import Assignment, Document, Task
from walt.utils import get_document_filters

from frontcast import local_settings



def home( request ):
  data = _shared_data(request, tags=['home'] )
  
  if request.user.is_authenticated():
    queryset = Document.objects.filter(Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user)).distinct()
  else:
    queryset = Document.objects.filter(status=Document.PUBLIC).distinct()
  
  data, q = _queryset(request, qs=queryset, d=data) 
  data['facets'] = get_document_filters(q)
  return render_to_response(  "dusk/index.html", RequestContext(request, data ) )


def notfound(request):
  raise
  return render_to_response("dusk/index.html", RequestContext(request, {}))


#
#
#   Storage
#   =======
#
#   Direct storage solution. You only have to login. extension are given as first arg
#
def storage( request, folder=None, index=None, extension=None ):
  data = _shared_data(request, tags=['me'])

  storage_path = settings.STORAGE_ROOT_PROTECTED if request.user.is_authenticated() else settings.STORAGE_ROOT_PUBLIC 


  filepath = os.path.join( storage_path, folder,"%s.%s" % (index,extension) );

  if os.path.exists(filepath):
    if settings.ENABLE_XACCEL and extension in ['mp4', 'ogg']:
      hidden_filepath = os.path.join('/videos/protected/', folder, "%s.%s"% (index,extension))
      response = HttpResponse()
      response['X-Accel-Redirect'] = hidden_filepath
      return response
    else:
      content_type = guess_type(filepath)
      wrapper = FileWrapper(file(filepath))
      response = HttpResponse(wrapper, content_type=content_type[0])
      response['Content-Length'] = os.path.getsize(filepath)
      return response
    # serve the file via django
  elif extension == "png":
    filepath = os.path.join( settings.STORAGE_ROOT, "common/notfound.png");
    wrapper = FileWrapper(file(filepath))
    response = HttpResponse(wrapper, content_type='image/png')
    response['Content-Length'] = os.path.getsize(filepath)
    return response

  data['filepath'] = {
    'folder':folder,
    'index':index,
    'extension':extension,
    'total': filepath,
    'content-type':  guess_type( filepath )[0],
    'hidden_filepath': os.path.join('/videos/protected/', folder, "%s.%s"% (index,extension)),
    'exists': os.path.exists( filepath )
  }

  #os.path.join(settings.STORAGE_ROOT, index)

  return render_to_response(  "dusk/404.html", RequestContext(request, data ) )

@login_required
def document_edit(request, slug):
  data = _shared_data(request, tags=['home'] )
  try:
    data['document'] = Document.objects.get( slug=slug)
  except Document.DoesNotExist, e:
    return notfound(request)

  print data['document'].owner
  print data['document'].authors
  if request.user.is_staff or data['document'].owner == request.user: 
    return render_to_response(  "dusk/document_edit.html", RequestContext(request, data ) )
  else:
    return login_view(request, message=_("unauthorized request"))


def _queryset(request, qs, d={}):
  e = Epoxy(request)
  q = qs.filter(**e.filters)

  d['filters'] = e.filters
  d['order_by'] = e.order_by
  d['total_count'] = q.count()
  d['items'] = q.order_by(*e.order_by)[e.offset : e.offset + e.limit] if e.limit != -1 else q.order_by(*e.order_by)

  return d, q


def _shared_data( request, tags=[], d={} ):
  d['tags'] = tags
  d['debug'] = settings.DEBUG
  return d



logger = logging.getLogger('glue')


def login_view(request, message="", default_next=None):
  if request.user.is_authenticated():
    return home( request )

  form = LoginForm( request.POST )
  next = request.REQUEST.get('next', 'frontcast_home') if default_next is None else default_next

  login_message = { 'next': next if len( next ) else 'frontcast_home'}

  if message:
    login_message['error'] = message
    return render_to_response('dusk/login.html', RequestContext(request, data ) )

  if request.method != 'POST':
    data = _shared_data( request, tags=[ "login" ], d=login_message )
    return render_to_response('dusk/login.html', RequestContext(request, data ) )

  if form.is_valid():
    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is not None:
      if user.is_active:
        login(request, user)
        # @todo: Redirect to next page

        return redirect( login_message['next'] )
      else:
        login_message['error'] = _("user has been disabled")
    else:
      login_message['error'] = _("invalid credentials")
      # Return a 'disabled account' error message
  else:
    login_message['error'] = _("invalid credentials")
    login_message['invalid_fields'] = form.errors


  data = _shared_data( request, tags=[ "login" ], d=login_message )


  return render_to_response('dusk/login.html', RequestContext(request, data ) )

def logout_view( request ):
  logout( request )
  return redirect( 'frontcast_home' )