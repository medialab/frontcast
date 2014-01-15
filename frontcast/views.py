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