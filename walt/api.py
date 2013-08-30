from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.loading import get_model
from glue.utils import Epoxy

def index(request):
	return Epoxy( request ).json()

@login_required( login_url=settings.GLUE_ACCESS_DENIED_URL )
def get_objects( request, model_name ):
	try:
		queryset = get_model( "walt", model_name ).objects.filter()
	except AttributeError, e:
		return Epoxy.error( request, message='model %s not found' % model_name, code='AttributeError')

	result = Epoxy( request ).queryset(
		queryset,
		model_name=model_name
	)
	return result.json()
