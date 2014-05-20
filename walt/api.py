import logging, json
import networkx as nx

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

from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_HTTPERROR

from networkx.algorithms import bipartite
from networkx.readwrite import json_graph

from walt.models import Assignment, Profile, Document, Tag, Task, WorkingDocument
from walt.forms import DocumentForm, FullDocumentForm, DocumentTagsForm, TagsForm, WorkingDocumentForm, URLForm
from walt.utils import get_document_filters, get_available_documents, get_available_document, get_working_document_filters, get_available_working_documents, is_number



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

  querymanager = [
    {
      'field':'title',
      'options': [
        {
          'label' : 'contains',
          'value' : 'title__icontains',
          'expect': 'text'
        },
        {
          'label' : 'AND contains',
          'value' : 'title__icontains__REDUCE',
          'expect': 'text'
        },
        {
          'label': 'equals',
          'value' : 'title__iexact',
          'expect': 'text'
        }
      ],
    },
    {
      'field':'type',
      'options': [
        {
          'label' : 'contains',
          'value' : 'type__icontains__REDUCE',
          'expect': 'text'
        },
        {
          'label': 'IS',
          'value' : 'type',
          'expect': 'type'
        }
      ],
    },
    {
      'field': 'institution',
      'options': [
        {
          'label' : 'name contains',
          'value' : 'tags__slug__icontains',
          'expect': 'text'
        },
        {
          'label' : 'IS',
          'value' : 'tags__slug',
          'expect': 'tags.In'
        },
      ],
    },
    {
      'field': 'tool',
      'options': [
        {
          'label' : 'name contains',
          'value' : 'tags__slug__icontains',
          'expect': 'text'
        },
        {
          'label' : 'is',
          'value' : 'devices__working_document__slug',
          'expect': 'tools'
        },
        {
          'label' : 'AND is',
          'value' : 'devices__working_document__slug__REDUCE',
          'expect': 'tools'
        }
      ],
    },
    {
      'field': 'tags',
      'options': [
        {
          'label' : 'contains',
          'value' : 'tags__slug__icontains',
          'expect': 'text'
        },
        {
          'label' : 'AND contains',
          'value' : 'tags__slug__icontains__REDUCE',
          'expect': 'text'
        },
        {
          'name': 'equals',
          'value' : 'tags__slug__iexact',
          'expect': 'text'
        }
      ],
    }
  ]
  epoxy.meta('manager',querymanager)
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
  epoxy = Epoxy(request)

  q = Q(pk=pk) if is_number(pk) else Q(slug=pk) 

  try:
    if request.user.is_staff:
      d = Document.objects.get(q)
    elif request.user.is_authenticated():
      d = Document.objects.get(
        q,
        Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user)
      )
    else:
      if is_number(pk):
        d = Document.objects.get(q, status=Document.PUBLIC)
      else:
        d = Document.objects.get(slug=pk, status=Document.PUBLIC)
  except Document.DoesNotExist,e:
    return epoxy.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()

  if epoxy.is_GET():
    return epoxy.item(d, deep=True).json()

  if not request.user.is_authenticated():
    # check ownerships or is_staffitude or is_author to enable it @todo
    return epoxy.throw_error(code=API_EXCEPTION_AUTH).json()
    
  if epoxy.is_POST():
    is_valid, d = edit_object(instance=d, Form=FullDocumentForm, request=request, epoxy=epoxy)
    if is_valid:
      d.save()
      
    else:
      return epoxy.throw_error(error=d, code=API_EXCEPTION_FORMERRORS).json()

  return epoxy.item(d, deep=True).json()



def tags(request):
  epoxy = Epoxy(request)
  epoxy.queryset(Tag.objects.filter())
  return epoxy.json()



@staff_member_required
def working_documents(request):
  epoxy = Epoxy(request)
  if epoxy.is_POST():
    form = WorkingDocumentForm(epoxy.data)
    if form.is_valid():
      w = form.save(commit=False)
      w.owner = request.user
      w.save()
      epoxy.item(w, deep=True)
    else:
      return epoxy.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
  else:
    epoxy.queryset(WorkingDocument.objects.filter())
  return epoxy.json()


@staff_member_required
def working_documents_filters(request):
  '''
  Get every tag associated with global collection in order to provide filtering features.
  '''
  epoxy = Epoxy(request)

  querymanager = [
    {
      'field':'title',
      'options': [
        {
          'label' : 'contains',
          'value' : 'title__icontains',
          'expect': 'text'
        },
        {
          'label' : 'AND contains',
          'value' : 'title__icontains__REDUCE',
          'expect': 'text'
        },
        {
          'label': 'equals',
          'value' : 'title__iexact',
          'expect': 'text'
        }
      ],
    },
    {
      'field': 'institution',
      'options': [
        {
          'label' : 'name contains',
          'value' : 'tags__slug__icontains',
          'expect': 'text'
        },
        {
          'label' : 'IS',
          'value' : 'tags__slug',
          'expect': 'tags.In'
        },
      ],
    },
    {
      'field': 'tool',
      'options': [
        {
          'label' : 'name contains',
          'value' : 'tags__slug__icontains',
          'expect': 'text'
        },
        {
          'label' : 'is',
          'value' : 'devices__working_document__slug',
          'expect': 'tools'
        },
        {
          'label' : 'AND is',
          'value' : 'devices__working_document__slug__REDUCE',
          'expect': 'tools'
        }
      ],
    },
    {
      'field': 'tags',
      'options': [
        {
          'label' : 'contains',
          'value' : 'tags__slug__icontains',
          'expect': 'text'
        },
        {
          'label' : 'AND contains',
          'value' : 'tags__slug__icontains__REDUCE',
          'expect': 'text'
        },
        {
          'name': 'equals',
          'value' : 'tags__slug__iexact',
          'expect': 'text'
        }
      ],
    }
  ]
  epoxy.meta('manager',querymanager)
  queryset = get_available_working_documents(request).filter(**epoxy.filters)
  # deal with reduce and search field
  if epoxy.reduce:
    for r in epoxy.reduce:
      queryset = queryset.filter(r)

  if epoxy.search:
    queryset = queryset.filter(WorkingDocument.search(epoxy.search)).distinct()

  c = queryset.count()
  epoxy.meta('total_count', c)

  filters = get_working_document_filters(queryset=queryset)
  filters['total_count'] =c # I know, I know... copy for god's sake
  epoxy.add('objects', filters); # docuemnt connected
  return epoxy.json()



@staff_member_required
def working_document(request, pk):
  epoxy = Epoxy(request)
  try:
    if is_number(pk):
      d = WorkingDocument.objects.get(pk=pk)
    else: 
      d = WorkingDocument.objects.get(slug=pk)
  except WorkingDocument.DoesNotExist, e:
    return epoxy.throw_error(error='%s'%e, code=API_EXCEPTION_DOESNOTEXIST).json()

  

  if epoxy.is_POST():
    is_valid, d = edit_object(instance=d, Form=WorkingDocumentForm, request=request, epoxy=epoxy)
    if is_valid:
      d.save()
    else:
      return epoxy.throw_error(error=d, code=API_EXCEPTION_FORMERRORS).json()

  epoxy.item(d, deep=True)

  return epoxy.json()



@staff_member_required
def working_document_attach_tags(request, pk):
  if is_number(pk):
    d = WorkingDocument.objects.get(pk=pk)
  else: 
    d = WorkingDocument.objects.get(slug=pk)

  epoxy = Epoxy(request)
  epoxy.item(d)
 
  if epoxy.is_POST():
    is_valid, d = helper_free_tag(instance=d, append=True, epoxy=epoxy)
    if not is_valid:
      return epoxy.throw_error(error=d, code=API_EXCEPTION_FORMERRORS).json()

  epoxy.item(d, deep=True)
  return epoxy.json()



@staff_member_required
def working_document_detach_tags(request, pk, tag_pk):
  if is_number(pk):
    d = WorkingDocument.objects.get(pk=pk)
  else: 
    d = WorkingDocument.objects.get(slug=pk)


  epoxy = Epoxy(request)
  epoxy.item(d)

  #get tag
  t = Tag.objects.get(pk=tag_pk)
  d.tags.remove(t)
  
  epoxy.item(d, deep=True)
  return epoxy.json()

  



@staff_member_required
def url_title(request):
  '''
  @phttpparam url=http://blogs.scientificamerican.com/sa-visual/2014/02/18/dont-just-visualize-datavisceralize-it/
  '''
  epoxy = Epoxy(request)
  form = URLForm(request.REQUEST)

  if form.is_valid():
    import urllib2
    from bs4 import BeautifulSoup
    #print form.cleaned_data['url']
    try:
      soup = BeautifulSoup(urllib2.urlopen(form.cleaned_data['url']).read())
    except urllib2.HTTPError, e:
      soup = BeautifulSoup(e.read())
      #return epoxy.throw_error(error='%s' % e, code=API_EXCEPTION_HTTPERROR).json()
    #print soup
    epoxy.add('object',{
      'title': soup.title.string
    })
    return epoxy.json()
  
  return epoxy.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()



@transaction.atomic
def graph_bipartite(request, model_name, m2m_name):
  mod = get_model('walt', model_name)
  m2m = getattr(mod, m2m_name).field.rel.to

  result = Epoxy(request)
  B = nx.Graph()

  vfilters = {}
  warnings = {}

  #print getattr(mod, m2m_name)
  if 'v-filters' in request.REQUEST:
    try:
      vfilters = json.loads(request.REQUEST.get('v-filters'))
    except Exception, e:
      result.warning('v-filters', "Exception: %s" % e)
    else:
      result.meta('v-filters', vfilters)

  # filter set a and set b....
  for v in m2m.objects.exclude(**{'%s__isnull' % model_name:True}).filter(**vfilters).annotate(w=Count(model_name)):
    B.add_node('v%s' % v.id, attr_dict={'pk':v.id, 'color': '#ccc', 'slug': v.slug}, label=v.name if hasattr(v,'name') else '%s' % v, weight=v.w)
    queryset = getattr(v, '%s_set' % model_name).filter(**result.filters)
    if result.reduce is not None:
      for r in result.reduce:
        queryset = queryset.filter(r)
        #queryset = queryset.filter(self.reduce)
    queryset = queryset.distinct()

    for u_in_v in queryset:
      B.add_node('u%s' % u_in_v.id, attr_dict={'pk': u_in_v.id, 'color': '#ba3c3c'}, label=u_in_v.title if hasattr(u_in_v,'title') else '%s'% u_in_v)
      B.add_edge('v%s' % v.id, 'u%s' % u_in_v.id)

  # computate spring layout position on n=50 iterations to have a valid stasrting point.
  data = json_graph.node_link_data(B)
  data.update(result.response)

  data['edges'] = []

  for link in data['links']:
    data['edges'].append({
      'source': data['nodes'][link['source']]['id'],
      'target': data['nodes'][link['target']]['id']
    })

  data.pop("links", None)

  positions = nx.spring_layout(B).values()

  for i, p in enumerate(positions):
    data['nodes'][i]['x'] = p[0]
    data['nodes'][i]['y'] = p[1]
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



def biblib_proxy_guess(request):
  '''
  usage sample:
  angularjs
  angular.element(document.body).injector().get('ReferenceFactory').citation_by_rec_ids(["forccast",["scpo-icom2040-2013-0002"]]]).success(function(data){console.log(data.meta)})
  or point your broswer urlat :
  http://localhost:8000/api/biblib-proxy?indent&action=citation_by_rec_ids&params=[%22forccast%22,[%22scpo-icom2040-2013-0002%22]]
  '''
  import urllib2, json

  epoxy = Epoxy(request)

  #todo: form check action and params
  data = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": epoxy.data['action'],
    "params": json.loads(epoxy.data['params']) if 'params' in epoxy.data else []
  }

  
  if data['method'] in ["save", "field", "fields", "set_metadata_property"]:
    if request.user.is_staff:
      data['params'].append('teacher')
    else:
      data['params'].append('student')

  req = urllib2.Request(settings.BIBLIB_ENDPOINT, json.dumps(data))
  response = urllib2.urlopen(req)
  rs = '%s'%response.read()
  print rs[:64]
  # set the body
  return HttpResponse(rs)

  epoxy.meta('verbose', data)
  epoxy.add('object', rs)
  return epoxy.json()


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


def edit_object(instance, Form, request, epoxy=None):
  data = model_to_dict(instance)
  if epoxy:
    data.update(epoxy.data)
  else:
    data.update(request.REQUEST)

  form = Form(instance=instance, data=data)
  if form.is_valid():
    instance = form.save(commit=False)
    return True, instance
  return False, form.errors





@transaction.atomic
def helper_free_tag(instance, epoxy, append=True):
  '''
  instance's model should have tags m2m property...
  '''
  form = TagsForm(epoxy.data)

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

