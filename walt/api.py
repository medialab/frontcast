from datetime import datetime

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models.loading import get_model
from django.db.models import Q
from django.http import HttpResponse
from django.utils.text import slugify

from glue.utils import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST

from walt.models import Assignment, Profile, Document, Tag, Task
from walt.forms import DocumentForm


def index(request):
	return Epoxy(request).json()


def access_denied(request):
	return Epoxy.error(request, message='access denied');

#
#
#	Public domain Document objects getter
# ---
#
def documents(request):
	result = Epoxy(request).queryset(
		Document.objects.filter(status=Document.PUBLIC)
	)
	return result.json()


def document(request, pk):
	result = Epoxy(request)

	try:
		d = Document.objects.get(pk=pk, status=Document.PUBLIC)
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
#	Document objects getter
# ---
#
@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def user_documents(request):
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
		result.queryset(
			Document.objects.filter(Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user))
		)

	return result.json()


@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def user_document(request, pk):
	result = Epoxy(request)

	try:
		d = Document.objects.get(
			Q(pk=pk),
			Q(owner=request.user) | Q(authors=request.user)
		)
	except Document.DoesNotExist,e:
		return result.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()

	if result.is_DELETE():
		if d.owner == request.user:
			d.delete()
			return result.json()

		return result.throw_error(error='%s' % 'not authorized', code=API_EXCEPTION_AUTH).json()


	if result.is_POST():

		form = DocumentForm(request.REQUEST, instance=d)
		if form.is_valid():
			form.save(commit=False)
			d.save()
		else:
			result.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS)

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
#	Assignment objects getter
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
#	Generic objects getter
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
#	Generic single object getter
# ---
#
@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def get_object(request, model_name, pk):
	m = get_model("walt", model_name)
	result = Epoxy(request).single(m, {'pk':pk})
	return result.json()


#
#
#	BIBLIB
# ------
#
#	For POST data.
#
@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def biblib_proxy(request):
	# it *should'nt* allow save/edit requests. User proxy_safe instead
	import urllib2, json

	req = urllib2.Request(settings.BIBLIB_ENDPOINT, '%s'%request.read())
	response = urllib2.urlopen(req)

	# set the body
	return HttpResponse(response.read())


@login_required(login_url=settings.GLUE_ACCESS_DENIED_URL)
def biblib_proxy_safe(request):
	result = Epoxy(request)
	return result.json()


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

