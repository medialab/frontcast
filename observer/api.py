#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, logging

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_HTTPERROR
from observer.forms import DeviceForm, FullDocumentForm, LoginForm
from observer.models import Device, Document, WorkingDocument, Tag


logger = logging.getLogger(__name__)

# 
# decorator staff_member_required_for_POST
# ===
# Decorator for views that checks that the user is logged in and is a staff  member
# only if is sending POST requests.
#
def staff_member_required_for_POST(view_func, redirect_field_name=REDIRECT_FIELD_NAME, login_url='observer_access_denied'):
    """
    
    member, displaying the login page if necessary.
    """
    def decorator(*args, **kwargs):
      if args[0].method == 'POST':
        return user_passes_test(
          lambda u: u.is_active and u.is_staff,
          login_url=login_url,
          redirect_field_name=redirect_field_name
        )(view_func)

      return view_func(*args, **kwargs)
    return decorator


# 
# helper is_number
# ===
# Determine if a string may be interpreted as a number (float value)
#
def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


# 
#  helper get_available_document
#  ===
#
#  @param request
#  @param django.db.models.Q instance
#  @return <observer.models.Dpcument> or raise exception
# 
def get_available_document(request, q):
  '''
  @param request
  @return <walt.models.Dpcument> or raise exception
  '''
  try:
    if request.user.is_staff:
      d = Document.objects.get(q)
    elif request.user.is_authenticated():
      d = Document.objects.get(q, Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user))
    else:
      d = Document.objects.get(q, status=Document.PUBLIC)
  except Document.DoesNotExist, e:
    raise
  return d


# 
#  helper get_available_documents
#  ===
#
#  Return a queryset according to user auth level and document status
#  
#  @param req HTTPRequest django
#  @return django.model.Queryset
# 
def get_available_documents(req, res):
  if req.user.is_staff:
    queryset = Document.objects.filter().distinct()
  elif req.user.is_authenticated():
    queryset = Document.objects.filter(Q(status=Document.PUBLIC) | Q(owner=req.user) | Q(authors=req.user)).distinct()
  else:
    queryset = Document.objects.filter(status=Document.PUBLIC).distinct()

  # deal with 'reduce' and various search field
  if res.reduce:
    for r in res.reduce:
      queryset = queryset.filter(r)

  if res.search:
    queryset = queryset.filter( Document.search(res.search))

  return queryset


# 
#  helper get_available_working_documents
#  ===
#
#  Return a queryset according to user auth level and document status
#  
#  @param request
#  @return django.model.Queryset
#
@staff_member_required_for_POST
def get_available_working_documents(req):
  
  if req.user.is_staff:
    queryset = WorkingDocument.objects.filter().distinct()
  elif req.user.is_authenticated():
    queryset = WorkingDocument.objects.filter(Q(status=WorkingDocument.PUBLIC) | Q(owner=req.user) | Q(authors=req.user)).distinct()
  else:
    queryset = WorkingDocument.objects.filter(status=WorkingDocument.PUBLIC).distinct()
  return queryset


# 
#  api:/
#  main entrance
#
def index(req):
  return Epoxy(req).json()


# 
#  api:/
#  main entrance
#
def access_denied(req):
  return Epoxy(req).throw_error(error='unauthorized', code=API_EXCEPTION_AUTH).json()


# 
#  api:/login
#  main entrance
#
def login_view(req):
  res = Epoxy(req)

  if req.user.is_authenticated():
    return res.json()

  form = LoginForm(req.POST)
  
  #if not req.POST.get('remember_me', None):
  #  req.session.set_expiry(0)

  if form.is_valid():
    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is not None:
      if user.is_active:
        login(req, user)
        # @todo: Redirect to next page
        res.item(user)
        return res.json()
      else:
        return res.throw_error(error='account disabled', code=API_EXCEPTION_AUTH).json()
    else:
      return res.throw_error(error='invalid credentials', code=API_EXCEPTION_AUTH).json()
      # Return a 'disabled account' error message
  else:
    return res.throw_error(error=form.errors, code=API_EXCEPTION_AUTH).json()


# 
#  api:/document
#  retrieve the requested documents and handle POST requests.
#  At present, only staff can add documents.
#
@staff_member_required_for_POST
def documents(req):
  res = Epoxy(req)
  if res.is_POST(): # staff only can add document via api
    if not req.user.is_staff:
      return res.throw_error(error='', code=API_EXCEPTION_AUTH).json()

    form = FullDocumentForm(res.data)
    if not form.is_valid():
      return res.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()

    doc = form.save(commit=False)
    doc.owner = req.user

    doc.save()
    return res.item(doc).json()

  queryset = get_available_documents(req=req, res=res)
  res.queryset(queryset)
  res.meta('query', '%s' % res._queryset.query)
  return res.json()


# 
#  api:/document/(?P<pk>[:a-zA-Z\.\-\d]+)
#  retrieve the requested document by numeric ID or by its SLUG field. and handle POST requests.
#  At present, only staff can add documents.
#
@staff_member_required_for_POST
def document(req, pk):
  res = Epoxy(req)

  try:
    doc = get_available_document(req, Q(pk=pk) if is_number(pk) else Q(slug=pk))
  except Document.DoesNotExist, e:
    return res.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()
  
  if epoxy.is_POST():
    is_valid, doc = edit_object(instance=doc, Form=FullDocumentForm, request=req, epoxy=res)
    if is_valid:
      doc.save()

  return res.item(doc, deep=True).json()


# 
#  api:/working-document
#  retrieve the requested documents and handle POST requests.
#  At present, only staff can add documents.
#
@staff_member_required_for_POST
def workingDocuments(req):
  res = Epoxy(req)
  if req.user.is_staff and res.is_POST(): # staff only can add document via api
    if not req.user.is_staff:
      return res.throw_error(error='', code=API_EXCEPTION_AUTH).json()

    form = FullDocumentForm(res.data)
    if not form.is_valid():
      return res.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()

    doc = form.save(commit=False)
    doc.owner = req.user

    doc.save()
    return res.item(doc).json()

  queryset = get_available_working_documents(req)
  res.queryset(queryset)
  res.meta('query', '%s' % res._queryset.query)
  return res.json()


# 
#  api:/working-document/(?P<pk>[:a-zA-Z\.\-\d]+)
#  retrieve the requested working-document by numeric ID or by its SLUG field.
#  At present, only staff can add new working-documents.
#
@staff_member_required_for_POST
def workingDocument(req, pk):
  res = Epoxy(request)

  try:
    doc = get_available_working_document(req, Q(pk=pk) if is_number(pk) else Q(slug=pk))
  except Document.DoesNotExist, e:
    return res.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()
  
  if epoxy.is_POST():
    is_valid, doc = edit_object(instance=doc, Form=FullDocumentForm, request=req, epoxy=res)
    if is_valid:
      doc.save()

  return res.item(doc, deep=True).json()


#
# api:/device
# Get or create new device by using forms.DeviceForm
# A device is a connection between a Document and a Working Document
# Post requests are accessible by staff only (create a new device)
@staff_member_required_for_POST
def devices(req):
  res = Epoxy(req)
  
  if res.is_POST():
    if not req.user.is_staff:
      return res.throw_error(error='', code=API_EXCEPTION_AUTH).json()

    form = DeviceForm(res.data)
    if is_valid:
      dev = form.save()
      res.item(dev)
    else:
      return res.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
  
  res.queryset(Device.objects.filter())
  return res.json()


#
# api:/device/(?P<pk>[:a-zA-Z\.\-\d]+)
# Get,modify or delete a single device connection by using forms.DeviceForm
# post requests are accessible by staff only
@staff_member_required_for_POST
def device(req, pk):
  res = Epoxy(req)
  
  try:
    dev = Device.objects.get(pk=pk)
  except Device.DoesNotExist, e:
    return res.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()

  if req.user.is_staff and res.is_DELETE():
    dev.delete()
  if epoxy.is_POST():
    is_valid, doc = edit_object(instance=doc, Form=FullDocumentForm, request=req, epoxy=res)
    if is_valid:
      doc.save()
  
  return res.item(doc, deep=True).json()



#
# api:/documents/facets
# Get available filters for the given view. To be reviewed.
def documents_facets(req):
  res = Epoxy(req)

  facets = {
    'type'  : [],
    'date'  : [],
    'tags'  : {},
    'tools' : [],
  }

  #load request filters and add them to the available queryset
  queryset = get_available_documents(req=req, res=res)
  
  c = queryset.count()
  res.meta('total_count', c)

  queryset = queryset.filter(**res.filters)

  for t in queryset.order_by().values('type').annotate(count=Count('id')):
    facets['type'].append({
      'name': '%s'%t['type'],
      'count': t['count']
    })

  for t in queryset.order_by().values('date').annotate(count=Count('id')):
    facets['date'].append({
      'name': '%s'%t['date'],
      'count': t['count']
    })

  ids = []
  for d in queryset:
    ids.append(d.id)
  
  # get keywords
  for facet in Tag.TYPE_IN_FACETS:
    facets['tags'][facet[0]] = [
      {
        'count': t.count,
        'slug': t.slug,
        'name': t.name,
        'type': t.type,
      } for t in Tag.objects.filter(document__id__in=ids, type=facet[0]).annotate(count=Count('document')).filter(count__gt=1)
    ]

  facets['tools'] = [
    { 
      'count': d.count,
      'title': d.title,
      'id': d.id,
      'slug': d.slug
    } for d in WorkingDocument.objects.filter(supports__document__id__in=ids).annotate(count=Count('supports__document')).filter(count__gt=1)
  ]

  res.add('facets', facets)

  return res.json()


@csrf_exempt
def proxy_reference(request):
  # it *should'nt* allow save/edit requests. User proxy_safe instead.
  import urllib2, json

  # filter uifiled, requests action according to role
  #result = Epoxy(request)
  logger.info('proxy biblib')
  # get request as an arbitrary object
  r = '%s'%request.read()
  
  data = json.loads(r)
  
  # inject role in request
  if data['method'] in ["save", "field", "fields", "set_metadata_property"]:
    if request.user.is_staff:
      data['params'].append('teacher')
    else:
      data['params'].append('student')

  if data['method'] == "save":
      # todo: check if user has access
      pass

  logger.info('... params to be sent %s' % data['params'])
  # return result.json()

  req = urllib2.Request(settings.BIBLIB_ENDPOINT, json.dumps(data))
  response = urllib2.urlopen(req)
  rs = '%s'%response.read()
  logger.info('... received %s' % rs[:64])
  # set the body
  return HttpResponse(rs)