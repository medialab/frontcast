import logging
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

logger = logging.getLogger('glue')


def login_view( request ):
	
	form = LoginForm( request.POST )
	next = request.REQUEST.get('next', 'walt_home')

	login_message = { 'next': next if len( next ) else 'walt_home'}

	if request.method != 'POST':
		data = _shared_data( request, tags=[ "index" ], d=login_message )
		return render_to_response('walt/login.html', RequestContext(request, data ) )
	
	if form.is_valid():
		user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				# @todo: Redirect to next page

				return redirect( login_message['next'] )
			else:
				login_message['error'] = _("user has been disabled")
		else:
			login_message['error'] = _("invalid credentials")
			# Return a 'disabled account' error message
	else:
		login_message['error'] = _("invalid credentials")
		login_message['invalid_fields'] = form.errors


	data = _shared_data( request, tags=[ "index" ], d=login_message )


	return render_to_response('walt/login.html', RequestContext(request, data ) )

def logout_view( request ):
	logout( request )
	return redirect( 'walt_home' )



def home( request ):
	data = {}
	return render_to_response(  "walt/index.html", RequestContext(request, data ) )


@login_required
def spiff( request, username ):
	data = {}
	data['username'] = username

	return render_to_response(  "walt/spiff.html", RequestContext(request, data ) )

def _shared_data( request, tags=[], d={} ):
	d['tags'] = tags
	return d
