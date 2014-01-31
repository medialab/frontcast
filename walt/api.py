import logging

from datetime import datetime

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models.loading import get_model
from django.db.models import Q,Count
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

from glue.utils import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST

from walt.models import Assignment, Profile, Document, Tag, Task
from walt.forms import DocumentForm, FullDocumentForm
from walt.utils import get_document_filters, get_available_documents, is_number

logger = logging.getLogger('glue')

def index(request):
  return Epoxy(request).json()


def access_denied(request):
  return Epoxy.error(request, message='access denied');

#
#
#  Public domain Document objects getter
# ---
#
def documents(request):
  if request.user.is_staff:
    queryset =   Document.objects.filter()
  elif request.user.is_authenticated():
    queryset =   Document.objects.filter(Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user)).distinct()
  else:
    queryset = Document.objects.filter(status=Document.PUBLIC).distinct()
    
  result = Epoxy(request).queryset(queryset)
  return result.json()


def documents_filters(request):
  '''
  Get every tag associated with global collection in order to provide filtering features.
  '''
  epoxy = Epoxy(request)
 
  queryset = get_available_documents(request).filter(**epoxy.filters)
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
#  Generic objects getter
# ---
#
@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def get_objects(request, model_name):
  try:
    m = get_model("walt", model_name)
    queryset = m.objects.filter()
  except AttributeError, e:
    return Epoxy.error(request, message='model "%s" not found' % model_name, code='AttributeError')
  
  result = Epoxy(request).queryset(
    queryset,
    model=m
  )
  return result.json()


#
#
#  Generic single object getter
# ---
#
@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def get_object(request, model_name, pk):
  m = get_model("walt", model_name)
  result = Epoxy(request).single(m, {'pk':pk})
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
