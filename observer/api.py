#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, logging

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.db.models import Count, Q
from django.db.models.loading import get_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_HTTPERROR
from glue.api import edit_object
from observer.forms import DeviceForm, FullDocumentForm, LoginForm, TagForm
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
#  return the requested documents and handle POST requests.
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
#  api:/document/(?P<ids>[\d,]+)
#  return the requested document by multiple ids.
#  At present, only GET requests are available.
#
@staff_member_required_for_POST
def documents_by_ids(req, ids):
  res = Epoxy(req)
  res.queryset(get_available_documents(req, res).filter(id__in=[x.strip() for x in ids.split(',')]))
  return res.json()



# 
#  api:/document/(?P<pk>[:a-zA-Z\.\-\d]+)
#  return the requested document by numeric ID or by its SLUG field. and handle POST requests.
#  At present, only staff can add documents.
#
@staff_member_required_for_POST
def document(req, pk):
  res = Epoxy(req)

  try:
    doc = get_available_document(req, Q(pk=pk) if is_number(pk) else Q(slug=pk))
  except Document.DoesNotExist, e:
    return res.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()
  
  if res.is_POST():
    form, doc = edit_object(instance=doc, Form=FullDocumentForm, epoxy=res)
    if form.is_valid():
      doc.save()
    else:
      return res.throw_error(error=form.errors, code=API_EXCEPTION_DOESNOTEXIST).json()

  if res.is_DELETE():
    pass
    
  return res.item(doc, deep=True).json()






# 
#  api:/working-document
#  return a collection of working-documents and handle POST requests as working-document creation.
#  At present, only staff can add working-document.
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
#  api:/working-document/(?P<ids>[\d]+,[\d]+)
#  return the requested tags by multiple ids (at least two ids).
#  At present, only GET requests are available.
#
@staff_member_required_for_POST
def workingDocuments_by_ids(req, ids):
  res = Epoxy(req)
  res.queryset(get_available_working_documents(req).filter(id__in=[x.strip() for x in ids.split(',')]))
  return res.json()


# 
#  api:/working-document/(?P<pk>[:a-zA-Z\.\-\d]+)
#  return the requested working-document by numeric ID or by its SLUG field.
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
    if form.is_valid():
      dev = form.save()
      return res.item(dev).json()
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

  if res.is_POST():
    form, dev = edit_object(instance=dev, Form=DeviceForm, epoxy=res)
    if form.is_valid():
      form.save()
    else:
      return res.throw_error(error=form.errors, code=API_EXCEPTION_DOESNOTEXIST).json()

  if res.is_DELETE():
    dev.delete()
    return res.json()

  return res.item(dev, deep=True).json()


# 
#  api:/tag
#  return a collection of tags and handle POST request for tag creation.
#  At present, only staff can add new tag.
#
@staff_member_required_for_POST
def tags(req):
  res = Epoxy(req)
  if res.is_POST(): # staff only can add document via api
    if not req.user.is_staff:
      return res.throw_error(error='', code=API_EXCEPTION_AUTH).json()

    form = TagForm(res.data)
    if not form.is_valid():
      return res.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()

    t = form.save()

    return res.item(t).json()

  res.queryset(Tag.objects.filter())
  return res.json()


# 
#  api:/tag/(?P<ids>[\d,]+)
#  return the requested tags by multiple ids.
#  At present, only GET requests are available.
#
@staff_member_required_for_POST
def tags_by_ids(req, ids):
  res = Epoxy(req)
  res.queryset(Tag.objects.filter(id__in=[x.strip() for x in ids.split(',')]))
  return res.json()


# 
#  api:/tag/(?P<pk>[:a-zA-Z\.\-\d]+)
#  return the requested tag by numeric ID or by its SLUG field. This method handles POST requests.
#  At present, only staff can add documents.
#
@staff_member_required_for_POST
def tag(req, pk):
  res = Epoxy(req)

  try:
    t = Tag.objects.get(Q(pk=pk) if is_number(pk) else Q(slug=pk))
  except Tag.DoesNotExist, e:
    return res.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()
  
  if res.is_POST():
    form, t = edit_object(instance=t, Form=TagForm, epoxy=res)
    if form.is_valid():
      t.save()
    else:
      return res.throw_error(error=form.errors, code=API_EXCEPTION_DOESNOTEXIST).json()

  if res.is_DELETE():
    pass
    
  return res.item(t, deep=True).json()



# GET or create m2m links
#
@staff_member_required_for_POST
def m2m_links(req, model_name, pk, m2m_name, ids):
  res = Epoxy(req)
  mod = get_model('observer', model_name)
  

  item = mod.objects.get(pk=pk)

  #m2mf = getattr(mod, m2m_name)
  m2m  = getattr(mod, m2m_name).field.rel.to

  getattr(item, m2m_name).add(*[x.id for x in m2m.objects.filter(id__in=[x.strip() for x in ids.split(',')])])
  
  res.item(item)
  #m2m = getattr(mod, m2m_name).field.rel.to
  #print m2m, [(f.name, f.related.parent_model) for f in mod._meta.many_to_many]
  #m2m = get_model('observer', m2m_name)
  #print [(f.name, f.related.parent_model) for f in mod._meta.many_to_many], m2m.__name__
  #print filter(lambda f: f == m2m, [f.related.parent_model for f in mod._meta.many_to_many])
  #if m2m.__name__ not in 
  #  return res.throw_error(error='%s is not related with %s' % (model_name, m2m_name), code=API_EXCEPTION_DOESNOTEXIST).json()
  #getattr(mod, m2m_name)
  # get related name
  #m2m.objects.filter(id__in=[x.strip() for x in ids.split(',')]))
  
  return res.json()


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




# 
# api:/graph-bipartite/observer/document/tags
@transaction.atomic
def graph_bipartite(req, app_name, model_name, m2m_name):
  res = Epoxy(req)
  mod = get_model(app_name, model_name)
  m2m = getattr(mod, m2m_name).field.rel.to

  B = {};

  res.queryset(m2m.objects.exclude(**{'%s__isnull' % model_name:True}).filter(**vfilters).annotate(w=Count(model_name)))

  return res.json()
  # # filter set a and set b....
  # for v in :
  #   node = {
  #     'label': v.name if hasattr(v,'name') else '%s' % v
  #     'weight': v.w,
  #     'pk': v.pk
  #   }
    
    
  #   B.add_node('v%s' % v.id, attr_dict={'pk':v.id, 'color': '#ccc', 'slug': v.slug}, label=v.name if hasattr(v,'name') else '%s' % v, weight=v.w)
  #   queryset = getattr(v, '%s_set' % model_name).filter(**result.filters)
  #   if result.reduce is not None:
  #     for r in result.reduce:
  #       queryset = queryset.filter(r)
  #       #queryset = queryset.filter(self.reduce)
  #   queryset = queryset.distinct()

  #   for u_in_v in queryset:
  #     B.add_node('u%s' % u_in_v.id, attr_dict={'pk': u_in_v.id, 'color': '#ba3c3c'}, label=u_in_v.title if hasattr(u_in_v,'title') else '%s'% u_in_v)
  #     B.add_edge('v%s' % v.id, 'u%s' % u_in_v.id)

  #   B.append(node)
     
  # # computate spring layout position on n=50 iterations to have a valid stasrting point.
  # data = json_graph.node_link_data(B)
  # data.update(result.response)

  # data['edges'] = []

  # for link in data['links']:
  #   data['edges'].append({
  #     'source': data['nodes'][link['source']]['id'],
  #     'target': data['nodes'][link['target']]['id']
  #   })

  # data.pop("links", None)

  # positions = nx.spring_layout(B).values()

  # for i, p in enumerate(positions):
  #   data['nodes'][i]['x'] = p[0]
  #   data['nodes'][i]['y'] = p[1]
  # #//  result.item(obj)
  # #  result.add('objects', [model_to_dict(i) for i in getattr(obj, m2m_name).all()])
  # return HttpResponse(json.dumps(data, default=Epoxy.encoder, indent=2), content_type='application/json')
