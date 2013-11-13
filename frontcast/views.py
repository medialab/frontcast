import logging, os, urllib
from mimetypes import guess_type

from django.conf import settings
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

from glue.utils import Epoxy

from walt.forms import LoginForm
from walt.models import Assignment, Document, Task
from walt.utils import get_pending_assignments

from frontcast import local_settings



def home( request ):
  data = _shared_data( request, tags=['home'] )
  #a = Assignment.objects.filter(unit__profile__user=request.user, date_completed__isnull=True)
  #if a.count() > 0:
  # t = a[0].task
  # return task( request, t.id)

  return render_to_response(  "frontcast/index.html", RequestContext(request, data ) )


def _shared_data( request, tags=[], d={} ):
  d['tags'] = tags
  return d