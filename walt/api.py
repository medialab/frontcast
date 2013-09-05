from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.loading import get_model
from django.db.models import Q

from glue.utils import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST

from walt.models import Assignment, Profile, Document, Tag, Task
from walt.forms import DocumentForm

def index(request):
	return Epoxy( request ).json()


def access_denied(request):
	return Epoxy.error( request, message='access denied');


#
#
#	Document objects getter
# ---
#
@login_required( login_url=settings.GLUE_ACCESS_DENIED_URL )
def user_documents( request ):
	result = Epoxy( request )

	if result.is_POST():
		form = DocumentForm(request.REQUEST)

		if form.is_valid():
			d = form.save(commit=False)
			d.owner = request.user
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
		result.queryset(
			Document.objects.filter(Q(status=Document.PUBLIC) | Q(owner=request.user))
		)

	return result.json()


@login_required( login_url=settings.GLUE_ACCESS_DENIED_URL )
def user_document( request, pk ):
	result = Epoxy( request )

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
		form.save()

	result.item(d)

	return result.json()

#
#
#	Assignment objects getter
# ---
#
@login_required( login_url=settings.GLUE_ACCESS_DENIED_URL )
def user_assignments( request ):
	result = Epoxy( request ).queryset(
		Assignment.objects.filter( unit__profile__user=request.user, date_completed__isnull=True )
	)
	return result.json()


#
#
#	Generic objects getter
# ---
#
@login_required( login_url=settings.GLUE_ACCESS_DENIED_URL )
def get_objects( request, model_name ):
	try:
		m = get_model( "walt", model_name )

	except AttributeError, e:
		return Epoxy.error( request, message='model %s not found' % model_name, code='AttributeError')

	# to be filtered according to user
	queryset = m.objects.filter()

	result = Epoxy( request ).queryset(
		queryset,
		model=m
	)
	return result.json()

#
#
#	Generic single object getter
# ---
#
@login_required( login_url=settings.GLUE_ACCESS_DENIED_URL )
def get_object( request, model_name, pk ):
	m = get_model( "walt", model_name )
	result = Epoxy( request ).single( m, {'pk':pk})
	return result.json()
