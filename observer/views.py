from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext



@staff_member_required
def index(request):
  data = _shared_data(request, tags=['scenario'])
  return render_to_response("observer/index.html", RequestContext(request, data))



def _shared_data( request, tags=[], d={} ):
  d['tags'] = tags
  d['debug'] = settings.DEBUG
  return d
