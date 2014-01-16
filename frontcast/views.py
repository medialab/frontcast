import logging, os, urllib
from mimetypes import guess_type

from django.conf import settings
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
    hidden_filepath = os.path.join('/videos/protected/', folder, "%s.%s"% (index,extension))
    response = HttpResponse()
    response['X-Accel-Redirect'] = hidden_filepath
    return response


  data['filepath'] = {
    'folder':folder,
    'index':index,
    'extension':extension,
    'total': filepath,
    'content-type':  guess_type( filepath )[0],
    'exists': os.path.exists( filepath )
  }

  #os.path.join(settings.STORAGE_ROOT, index)

  return render_to_response(  "dusk/404.html", RequestContext(request, data ) )


def document(request, slug):
  data = _shared_data(request, tags=['home'] )
  try:
    data['document'] = Document.objects.get( slug=slug)
  except Document.DoesNotExist, e:
    return notfound(request)
  data['total_count'] = 1
  data['filters'] = None

  return render_to_response(  "dusk/document.html", RequestContext(request, data ) )

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