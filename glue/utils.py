import json, os, inspect, re

from django.db.models.query import QuerySet, RawQuerySet
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.forms import Form, IntegerField
from django.core import serializers

#
#    CONSTS
#    ======
#
API_DEFAULT_OFFSET = 0
API_DEFAULT_LIMIT = 50
API_AVAILABLE_METHODS = [ 'DELETE', 'POST', 'GET' ]
API_EXCEPTION        =  'GenericException'
API_EXCEPTION_AUTH    =  'Unauthorized'
API_EXCEPTION_INTEGRITY    =  'IntegrityError'
API_EXCEPTION_VALUE      =  'ValueError'
API_EXCEPTION_DOESNOTEXIST  =  'DoesNotExist'
API_EXCEPTION_DUPLICATED  =  'Duplicated'
API_EXCEPTION_FORMERRORS  =  'FormErrors'
API_EXCEPTION_INCOMPLETE  =  'Incomplete'
API_EXCEPTION_EMPTY      =  'Empty'
API_EXCEPTION_INVALID    =  'Invalid'
API_EXCEPTION_OSERROR    =  'OsError'

#
#    MISC FUNCTIONS
#    ==============
#
def whosdaddy( level=2 ):
  return inspect.stack()[level][3]


#
#    BIBTEX JSON PARSER
#    ==================
#
def bibtex( reference ):
  reference = re.sub('(\w+)\s*=\s*\{+',r'"\1":"', reference )
  reference = re.sub('\}+(?=\s*[,\}+])','"', reference )
  reference = re.sub('@(\w+)\s*\{([^,]*)',r'{"bibtext_key":"\2","\1": "\2"', reference )
  return json.loads( reference )

#
#    REQUEST VALIDATION
#    ==================
#
class OffsetLimitForm( Form ):
  offset  = IntegerField( min_value=0, required=False, initial=0 )
  limit  = IntegerField( min_value=1, max_value=100, required=False, initial=25 )



#
#    EPOXY
#    =====
#
#    Helper to handle json response.
#
#    Basic usage
#    -----------
#    In a django view:
#    <code>
#    def view_with_json_output( request ):
#      response = Epoxy( request ).json()
#      return response.json()
#    </code>
#
#    Advanced usage
#    --------------
#    queryset =
#
class Epoxy:
  """
  Understand requet.REQUEST meta params like django filters, limit/offset

  Usage:

  queryset = <Model>.objects.filter( **kwargs )
  return Epoxy( request ).get_response( queryset=queryset )

  """
  def __init__(self, request, method='GUESS' ):
    self.request = request
    self.response = { 'status':'ok' } # a ditionary of things
    self.filters = {}
    self.search = None
    self.method = method
    self.limit = API_DEFAULT_LIMIT
    self.offset = API_DEFAULT_OFFSET
    self.order_by = []
    self.process()

  def warning( self, key, message ):
    if 'warnings' not in self.response['meta']:
      self.response['meta']['warnings'] = {}
    self.response['meta']['warnings'][ key ] = message


  def is_GET(self):
    return self.method == 'GET'


  def is_POST(self):
    return self.method == 'POST'


  def is_DELETE(self):
    return self.method == 'DELETE'


  def process( self ):
    self.response['meta'] = {}
    self.response['meta']['action'] = whosdaddy(3)
    self.response['meta']['user'] = self.request.user.username
    # understand method via REQUEST params only if desired.
    if self.method == 'GUESS':

      if 'method' in self.request.REQUEST: # simulation
        method = self.request.REQUEST.get('method')
        if method not in API_AVAILABLE_METHODS:
          self.warning( 'order_by', "Method: %s is not available " % self.request.REQUEST.get('method') )
        else:
          self.response['meta']['method'] = method
          self.method = method
      else:
        self.method = self.response['meta']['method'] = self.request.method

    if self.method == 'GET' and 'search' in self.request.REQUEST:
      self.search = self.meta('search', self.request.REQUEST.get('search'))
      
    if self.method == 'GET' and 'filters' in self.request.REQUEST:
      try:
        self.filters = self.meta('filters', json.loads( self.request.REQUEST.get('filters')))
      except Exception, e:
        self.warning( 'filters', "Exception: %s" % e )

    # order by
    if self.method == 'GET' and 'order_by' in self.request.REQUEST:
      try:
        self.order_by = self.response['meta']['order_by'] = json.loads( self.request.REQUEST.get('order_by') ) # json array
      except Exception, e:
        self.warning( 'order_by', "Exception: %s" % e )

    # limit / offset
    if self.method=='GET' and ( 'offset' in self.request.REQUEST or 'limit' in self.request.REQUEST ) :
      
      if '%s' % self.request.REQUEST.get('limit', 0) == '-1':
        self.offset = 0
        self.limit = -1
        self.response['meta']['offset'] = self.offset
        self.response['meta']['limit'] = self.limit
      else:
        form = OffsetLimitForm( self.request.REQUEST )
        if form.is_valid():
          self.offset = form.cleaned_data['offset'] if form.cleaned_data['offset'] else self.offset
          self.limit  = form.cleaned_data['limit'] if form.cleaned_data['limit'] else self.limit
        else:
          self.warning( 'offsets', form.errors )
          self.response['meta']['offset'] = self.offset
          self.response['meta']['limit'] = self.limit
          # next / previous
          if self.offset > 0:
            self.response['meta']['previous'] = {
              'offset': max( self.offset - self.limit, 0 ),
              'limit': self.limit
            }
        # set limit of offset
        self.response['meta']['next'] = {
          'offset': self.offset + self.limit,
          'limit': self.limit
        }

    return self


  def single( self, model, kwargs ):
    self.response['meta']['model'] = model.__name__
    try:
      self.response['object'] = model.objects.get( **kwargs ).json( deep=True )
    except model.DoesNotExist, e:
      return self.throw_error( error="%s" % e, code=API_EXCEPTION_EMPTY )
    return self


  def item( self, item, deep=False):
    self.response['meta']['model'] = '%s' % item.__class__.__name__
    self.response['object'] = item.json( deep=deep )
    return self


  def queryset( self, queryset, model=None ):
    if self.search:
      if not hasattr(queryset.model, "search"):
        self.warning( 'search', "Model %s has no method to perform your search" % queryset.model.__name__ )
      else:
        queryset = queryset.filter( queryset.model.search(self.search) ).distinct()

    if type( queryset ) == QuerySet:

      self.response['meta']['total_count'] = queryset.filter( **self.filters ).count()
      qs = queryset.filter( **self.filters ).order_by( *self.order_by )

    elif type( queryset ) == RawQuerySet:
      # Special exceptions for RawQuerySets (cannot filter, does not have count() method)
      self.response['meta']['total_count'] = sum( 1 for r in queryset )
      qs = queryset
    else:
      qs = queryset.filter()

    # apply limits
    if self.limit > -1:
      qs = qs[ self.offset : self.offset + self.limit ]

    self.response['meta']['model'] = queryset.model.__name__
    
    # "easier to ask for forgiveness than permission" (EAFP) rather than "look before you leap" (LBYL)
    try:
      self.response['objects'] = [ o.json() for o in qs ]

    except AttributeError, e:
      self.warning( 'objects', "Exception: %s" % e )
      self.response['objects'] = []#serializers.serialize(**kwargs)

    #except Exception, e:
    #  return self.throw_error( error="Exception: %s" % e, code=API_EXCEPTION_INVALID )

    return self


  def json( self, mimetype="application/json" ):
    if self.request is not None and self.request.REQUEST.has_key('indent'):
      return HttpResponse( json.dumps( self.response, indent=4),  mimetype=mimetype)
    return HttpResponse( json.dumps( self.response ), mimetype=mimetype)


  def add( self, key, value, jsonify=False):
    self.response[ key ] = value.json() if jsonify else value
    return value


  def meta( self, key, value ):
    self.response['meta'][ key ] = value
    return value


  def throw_error( self, error="", code=API_EXCEPTION ):
    self.response[ 'status' ] = 'error'
    self.response[ 'error' ] = error
    self.response[ 'code' ] = code

    return self


  @staticmethod
  def error( request, message="", code=API_EXCEPTION, mimetype="application/json" ):
    e = {
      'status': 'error',
      'error' : message,
      'code'  : code
    }
    return HttpResponse(json.dumps(e), mimetype=mimetype)
