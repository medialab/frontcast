import logging, json

from datetime import datetime

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models.loading import get_model
from django.db.models import Q,Count
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST

from walt.models import Assignment, Profile, Document, Tag, Task, WorkingDocument
from walt.forms import DocumentForm, FullDocumentForm, DocumentTagsForm, TagsForm
from walt.utils import get_document_filters, get_available_documents, get_available_document, is_number



logger = logging.getLogger('glue')



def index(request):
  return Epoxy(request).json()



def access_denied(request):
  return Epoxy.error(request, message='access denied');



def documents(request):
  '''
  Public domain Document objects getter
  '''
  if request.user.is_staff:
    queryset =   Document.objects.filter().distinct()
  elif request.user.is_authenticated():
    queryset =   Document.objects.filter(Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user)).distinct()
  else:
    queryset = Document.objects.filter(status=Document.PUBLIC).distinct()
    
  result = Epoxy(request).queryset(queryset)
  result.meta('query', '%s' % result._queryset.query)
  return result.json()



def documents_filters(request):
  '''
  Get every tag associated with global collection in order to provide filtering features.
  '''
  epoxy = Epoxy(request)
 
  queryset = get_available_documents(request).filter(**epoxy.filters)
  # deal with reduce and search field
  if epoxy.reduce:
    for r in epoxy.reduce:
      queryset = queryset.filter(r)

  if epoxy.search:
    queryset = queryset.filter( Document.search(epoxy.search)).distinct()

  c = queryset.count()
  epoxy.meta('total_count', c)

  filters = get_document_filters(queryset=queryset)
  filters['total_count'] =c # I know, I know... copy for god's sake
  epoxy.add('objects', filters);
  return epoxy.json()



def document(request, pk):
  result = Epoxy(request)

  try:
    if request.user.is_staff:
      d = Document.objects.get(
        Q(slug=pk)
      )
    elif request.user.is_authenticated():
      d = Document.objects.get(
        Q(slug=pk),
        Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user)
      )
    else:
      if is_number(pk):
        d = Document.objects.get(pk=pk, status=Document.PUBLIC)
      else:
        d = Document.objects.get(slug=pk, status=Document.PUBLIC)
  except Document.DoesNotExist,e:
    return result.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()

  if result.is_GET():
    return result.item(d, deep=True).json()

  if not request.user.is_authenticated():
    # check ownerships or is_staffitude or is_author to enable it @todo
    return result.throw_error(code=API_EXCEPTION_AUTH).json()
    
  if result.is_POST():
    is_valid, d = edit_object(instance=d, Form=FullDocumentForm, request=request)
    if is_valid:
      d.save()
      
    else:
      return result.throw_error(error=d, code=API_EXCEPTION_FORMERRORS).json()

  return result.item(d, deep=True).json()



@staff_member_required
def working_documents(request):
  result = Epoxy(request).queryset(WorkingDocument.objects.filter())
  return result.json()



@staff_member_required
def working_document(request, pk):
  if is_number(pk):
    d = WorkingDocument.objects.get(pk=pk)
  else: 
    d = WorkingDocument.objects.get(slug=pk)

  result = Epoxy(request)
  result.item(d)

  return result.json()



@staff_member_required
def working_document_attach_tags(request, pk):
  if is_number(pk):
    d = WorkingDocument.objects.get(pk=pk)
  else: 
    d = WorkingDocument.objects.get(slug=pk)

  result = Epoxy(request)
  result.item(d)
 
  if result.is_POST():
    is_valid, d = helper_free_tag(instance=d, request=request, append=False)
    if not is_valid:
      return result.throw_error(error=d, code=API_EXCEPTION_FORMERRORS).json()

  result.item(d, deep=True)
  return result.json()


import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
from django.db.models import Count
@transaction.atomic
def graph_bipartite(request, model_name, m2m_name):
  mod = get_model('walt', model_name)
  
  #result = Epoxy(request).queryset()
  B = nx.Graph()

  #print getattr(mod, m2m_name)
  m2m = getattr(mod, m2m_name).field.rel.to

  # filter set a and set b....
  for v in m2m.objects.exclude(**{'%s__isnull' % model_name:True}).annotate(w=Count(model_name)):
    B.add_node('v%s' % v.id, attr_dict={'pk':v.id}, label=v.slug, weight=v.w)

    for u_in_v in getattr(v, '%s_set' % model_name).all():
      B.add_node('u%s' % u_in_v.id, attr_dict={'pk': u_in_v.id}, label=u_in_v.slug)
      B.add_edge('v%s' % v.id, 'u%s' % u_in_v.id)

  #add_edge
    
  '''{
  "nodes": [
    {
      "id": "n0",
      "label": "A node",
      "x": 0,
      "y": 0,
      "size": 3
    },'''
  data = json_graph.node_link_data(B)
  #//  result.item(obj)
  #  result.add('objects', [model_to_dict(i) for i in getattr(obj, m2m_name).all()])
  return HttpResponse(json.dumps(data, default=Epoxy.encoder, indent=2), content_type='application/json')



@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def document_attach_tags(request, pk):
  result = Epoxy(request)

  # check validity first of all
  form = DocumentTagsForm(request.REQUEST)
  if form.is_valid():
    try:
      d = get_available_document(request, pk)
    except Document.DoesNotExist,e:
      return result.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()

    # list of unique comma separated cleaned tags.
    tags = list(set([t.strip() for t in form.cleaned_data['tags'].split(',')]))

    for tag in tags:
      t, created = Tag.objects.get_or_create(name=tag, type=Tag.KEYWORD)
      t.save()
      d.tags.add(t)

    result.meta('tags', tags)
    return result.item(d, deep=True).json()

  else:
    return result.throw_error(error='%s' % form.errors, code=API_EXCEPTION_FORMERRORS).json()



def reference_documents(request):
  '''
  Document as Reference list. If request.user is_staff, even not public reference are shown
  '''
  quesryset = Document.objects.filter(reference__isnull=false) if request.user.is_staff else Document.objects.filter(reference__isnull=false, status=Document.PUBLIC)
  result = Epoxy(request).queryset(queryset)
  return result.json()


def reference_document(request, pk):
  '''
  Single document Reference list. If request.user is_staff, 
  ---

  '''
  result = Epoxy(request)

  try:
    d = Document.objects.get(pk=pk) if request.user.is_staff else Document.objects.get(pk=pk, status=Document.PUBLIC)
  except Document.DoesNotExist,e:
    return result.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()

  return result.item(d).json()


@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def user_drafts(request):
  result = Epoxy(request).queryset(
    Document.objects.filter(owner=request.user, status=Document.DRAFT)
  )
  return result.json()


#
#
#  Get all draft published recently
# ---
#
@staff_member_required
def world_documents(request):
  result = Epoxy(request)

  result.queryset(
    Document.objects.filter()
  )

  return result.json()



#
#
#  Document objects getter
# ---
#
@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def user_documents(request, username):
  result = Epoxy(request)

  if result.is_POST():
    form = DocumentForm(request.REQUEST)

    if form.is_valid():
      d = form.save(commit=False)
      d.owner = request.user
      d.slug = slugify(d.title)
      d.save()
      result.item(d)
    elif "__all__" in form.errors:
      try:
        d = Document.objects.get(slug=form.cleaned_data['slug'],title=form.cleaned_data['title'])
        result.warning(key='duplicate',message="item exists indeed")
        result.item(d)
      except Document.DoesNotExist, e:
        result.throw_error(error=form.errors, code=API_EXCEPTION_DOESNOTEXIST)
    else:
      result.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS)

  else:
    result.meta('o','e')
    if request.user.username == username:
      queryset =  Document.objects.filter(Q(owner=request.user) | Q(authors=request.user))
    else:
      queryset =  Document.objects.filter(status=Document.PUBLIC).filter(Q(owner__username=username) | Q(authors__username=username))
    result.queryset(queryset)

  return result.json()


def user_documents_filters(request, username):
  '''
  Get every tag associated with user collection in order to provide filtering features.
  
  '''
  epoxy = Epoxy(request)
 
  queryset= Document.objects.filter(Q(owner__username=username) | Q(authors__username=username), **epoxy.filters)
  epoxy.meta('total_count', queryset.count())

  filters = get_document_filters(queryset=queryset)
  epoxy.add('objects', filters);
  return epoxy.json()
  

@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def user_document(request, username, slug):
  result = Epoxy(request)

  try:
    if request.user.is_staff:
      d = Document.objects.get(
        Q(slug=slug)
      )
    elif request.user.username == username:
      d = Document.objects.get(
        Q(slug=slug),
        Q(owner=request.user) | Q(authors=request.user)
      )
    else:
      d = Document.objects.get(
        Q(slug=slug),
        Q(owner__username=username) | Q(authors__username=username)
      )
  except Document.DoesNotExist,e:
    return result.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()

  if result.is_DELETE():
    if d.owner == request.user:
      d.delete()
      return result.json()

    return result.throw_error(error='%s' % 'not authorized', code=API_EXCEPTION_AUTH).json()


  if result.is_POST():
    #if d.owner == request.user OR user in d.authors:
      form = DocumentForm(request.REQUEST, instance=d)
      if form.is_valid():
        form.save(commit=False)
        d.save()
      else:
        result.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS)
    #else:
    #  return result.throw_error(error='%s' % 'not authorized', code=API_EXCEPTION_AUTH).json()

  result.item(d)

  return result.json()


@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def user_assignment_documents(request, pk):
  result = Epoxy(request)

  try:
    a = Assignment.objects.get(
      pk = pk,
      unit__profile__user = request.user
    )
  except Assignment.DoesNotExist,e:
    return result.throw_error(error='%s'%e, code=API_EXCEPTION_DOESNOTEXIST)

  if result.is_POST():
    form = DocumentForm(request.REQUEST)

    if form.is_valid():
      d = form.save(commit=False)
      d.owner = request.user
      d.save()
      a.documents.add(d)
      a.save()
    elif "__all__" in form.errors:
      result.throw_error(error=form.errors, code=API_EXCEPTION_DOESNOTEXIST)
    else:
      result.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS)

  # todo
  result.queryset(
    Document.objects.filter(assignment=a).filter(Q(owner=request.user) | Q(authors=request.user))
  )

  result.item(a)

  return result.json()


@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def user_assignment_deliver(request, pk):
  result = Epoxy(request)

  try:
    a = Assignment.objects.get(
      pk = pk,
      unit__profile__user = request.user
    )
  except Assignment.DoesNotExist,e:
    return result.throw_error(error='%s'%e, code=API_EXCEPTION_DOESNOTEXIST)

  if a.date_completed is not None:
    return result.item(a).json()

  a.date_completed = datetime.now()
  a.save()
  result.item(a)

  return result.json()


#
#
#  Assignment objects getter
# ---
#
@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def user_assignments(request):
  result = Epoxy(request).queryset(
    Assignment.objects.filter(unit__profile__user=request.user, date_completed__isnull=True)
  )
  return result.json()


@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def user_assignment(request, pk):
  result = Epoxy(request).queryset(
    Assignment.objects.filter(unit__profile__user=request.user, date_completed__isnull=True)
  )
  return result.json()



#
#
#  BIBLIB
# ------
#
#  For POST data.
#
@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def biblib_proxy(request):
  # it *should'nt* allow save/edit requests. is admin only omni hyper power. User proxy_safe instead
  import urllib2, json

  req = urllib2.Request(settings.BIBLIB_ENDPOINT, '%s'%request.read())
  response = urllib2.urlopen(req)

  # set the body
  return HttpResponse(response.read())


@csrf_exempt
def biblib_proxy_safe(request):
  # it *should'nt* allow save/edit requests. User proxy_safe instead
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


@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def oembed_proxy(request, provider):
  # handle oembed requests not supporting remote domains (isntead of using jsonp)
  import urllib2, json
  import urllib

  providers = {
    'flickr': 'http://www.flickr.com/services/oembed',
    'youtube': 'http://www.youtube.com/oembed'
  }

  if provider not in providers:
    result = Epoxy(request)
    result.meta('known_providers',providers)
    result.throw_error(error="not a known embed provider")
    return result.json()
  
  req = urllib2.Request("%s?%s" % (providers[provider], urllib.urlencode({
    'url': request.REQUEST.get('url',''),
    'format': 'json'
  })))
  response = urllib2.urlopen(req)

  # set the body
  return HttpResponse(response.read())


def edit_object(instance, Form, request):
  data = model_to_dict(instance)
  data.update(request.REQUEST)

  form = Form(instance=instance, data=data)
  if form.is_valid():
    instance = form.save(commit=False)
    return True, instance
  return False, form.errors





@transaction.atomic
def helper_free_tag(instance, request, append=True):
  '''
  instance's model should have tags m2m property...
  '''
  form = TagsForm(request.REQUEST)

  if form.is_valid():
    tags = list(set([t.strip() for t in form.cleaned_data['tags'].split(',')]))# list of unique comma separated cleaned tags.
    candidates = []
    for tag in tags:
      t, created = Tag.objects.get_or_create(name=tag, type=form.cleaned_data['type'])
      if append:
        instance.tags.add(t)
      else:
        candidates.append(t)

    if not append:
      instance.tags = candidates
    
    instance.save()

    return True, instance
  return False, form.errors

