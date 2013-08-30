from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.loading import get_model
from glue.utils import Epoxy


def index(request):
	return Epoxy( request ).json()


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


@login_required( login_url=settings.GLUE_ACCESS_DENIED_URL )
def get_object( request, model_name, pk ):
	m = get_model( "walt", model_name )
	result = Epoxy( request ).single( m, {'pk':pk})
	return result.json()
