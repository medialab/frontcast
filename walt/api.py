from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.loading import get_model
from django.db.models import Q

from glue.utils import Epoxy

from walt.models import Assignment, Profile, Document, Tag, Task


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
def documents( request ):
	result = Epoxy( request ).queryset(
		Document.objects.filter(Q(published=True) | Q(owner=request.user))
	)
	return result.json()


#
#
#	Assignment objects getter
# ---
#
@login_required( login_url=settings.GLUE_ACCESS_DENIED_URL )
def assignments( request ):
	result = Epoxy( request ).queryset(
		Assignment.objects.filter( profile__user=request.user, date_completed__isnull=True )
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
