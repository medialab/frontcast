import json, os, inspect, re
from operator import and_

from django.db.models.query import QuerySet, RawQuerySet
from django.conf import settings
from django.core import serializers
from django.db.models import Q
from django.forms import IntegerField
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpRequest

from glue.forms import OffsetLimitForm

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
API_EXCEPTION_HTTPERROR    = 'HTTPError'
API_EXCEPTION_ATTRIBUTEERROR = 'AttributeError'

#
#    MISC FUNCTIONS
#    ==============
#
def whosdaddy( level=2 ):
  act = inspect.stack()[level][3]
  mod = re.search(r'(?P<module>[^/]+)/(?P<file>[^/\.]+)\.py', '%s'%inspect.stack()[level][1])# observer/api.py

  return act if mod is None else '.'.join(mod.groups()+(act,))
  

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
  def __init__(self, request, method='GUESS', verbose=False):
    try:
      self.payload = request.body
    except:
      self.payload = None
      pass # print e
    self.request = request
    
    self.response = { 'status':'ok' } # a ditionary of things
    self.filters = {}
    self.reduce = None
    self.search = None
    self.method = method
    self.limit = API_DEFAULT_LIMIT
    self.offset = API_DEFAULT_OFFSET
    self.order_by = []
    self.data = {} # data coming from REST and/or REQUEST
    self.process(verbose=verbose)

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


  def process(self, verbose=False):
    self.response['meta'] = {}
    self.response['meta']['action'] = whosdaddy(3)
    self.response['meta']['user'] = self.request.user.username

    self.response['meta']['language'] = self.request.LANGUAGE_CODE if 'LANGUAGE_CODE' in self.request else None

    try:
      if self.payload:
        self.data = json.loads(self.payload)

    except Exception, e:
      self.warning( 'request payload error', "Exception: %s" % e )
    finally:
      self.data.update(self.request.REQUEST)

    if 'verbose' in self.request.REQUEST:
      self.meta('request', self.data)
    # understand method via REQUEST params only if desired.
    if self.method == 'GUESS':

      if 'method' in self.request.REQUEST: # simulation
        method = self.request.REQUEST.get('method')
        if method not in API_AVAILABLE_METHODS:
          self.warning( 'method', "Method: %s is not available " % self.request.REQUEST.get('method') )
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
      else:
        # format filters ending with __REDUCE:  add a magic dict
        reduces = []
        pop_fields = []

        for field in self.filters:
          if field.endswith('__REDUCE'):
            f = field[:-8]
            pop_fields.append(field)
            if isinstance(self.filters[field], basestring):
              reduces = reduces + [(f, self.filters[field])]
            else:
              reduces = reduces + [(f, i) for i in self.filters[field]]
        
        for i in pop_fields:
          self.meta('reducing', i)
          self.filters.pop(i, None)

        #  reduces = [(u'tags__slug', u'sciences-po'), (u'tags__slug', u'2013')]
        self.reduce = reduces



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
          self.warning( 'invalid', form.errors )
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
    self.response['object'] = item.json(deep=deep) if hasattr(item, 'json') else model_to_dict(item)
    return self


  def queryset( self, queryset, model=None ):
    if self.search:
      if hasattr(queryset.model, "indexed_search"):
        self.meta( 'search', "using whoosh index model for the model %s" % queryset.model.__name__ )
        self.response['meta']['model'] = queryset.model.__name__
        # normally your model indexed search should provide totalcount, limit, offset. 
        queryset.model.indexed_search(query=self.search, epoxy=self, queryset=queryset)
        return self
      elif not hasattr(queryset.model, "search"):
        self.warning( 'search', "Model %s has no method to perform your search" % queryset.model.__name__ )
      else:
        queryset = queryset.filter( queryset.model.search(self.search) ).distinct()

    if self.reduce is not None:
      self.meta('reduce', self.reduce)
      for r in self.reduce:
        queryset = queryset.filter(r)
        #queryset = queryset.filter(self.reduce)
      queryset = queryset.distinct()

    if type( queryset ) == QuerySet:

      self.response['meta']['total_count'] = queryset.filter( **self.filters ).count()
      qs = queryset.filter( **self.filters ).order_by( *self.order_by )

    elif type( queryset ) == RawQuerySet:
      # Special exceptions for RawQuerySets (cannot filter, does not have count() method)
      self.response['meta']['total_count'] = sum( 1 for r in queryset )
      qs = queryset
    else:
      qs = queryset.filter()

    if self.response['meta']['total_count']:
      self.response['meta']['offset'] = self.offset
      self.response['meta']['limit'] = self.response['meta']['total_count'] if self.response['meta']['total_count'] < self.offset + self.limit else self.limit

    # apply limits
    if self.limit > -1:
      qs = qs[ self.offset : self.offset + self.limit ]

    self.response['meta']['model'] = queryset.model.__name__
    
    # "easier to ask for forgiveness than permission" (EAFP) rather than "look before you leap" (LBYL)
    try:
      self.response['objects'] = [o.json() for o in qs]
    except AttributeError, e:
      self.warning( 'objects', "Exception: %s" % e )
      self.response['objects'] = [model_to_dict(o) for o in qs]
    except Exception, e:
      self.warning( 'objects', "Exception: %s" % e )
      self.response['objects'] = [ ]#serializers.serialize(**kwargs)

    #except Exception, e:
    #  return self.throw_error( error="Exception: %s" % e, code=API_EXCEPTION_INVALID )
    self._queryset = qs
    return self


  def json( self, mimetype="application/json" ):
    if self.request is not None and self.request.REQUEST.has_key('indent'):
      return HttpResponse(json.dumps(self.response, default=Epoxy.encoder, indent=4),  content_type=mimetype)
    return HttpResponse(json.dumps(self.response, default=Epoxy.encoder), content_type=mimetype)


  def add( self, key, value, jsonify=False):
    self.response[ key ] = value.json() if jsonify else value
    return value


  def meta(self, key, value):
    self.response['meta'][ key ] = value
    return value


  def throw_error( self, error="", code=API_EXCEPTION ):
    self.response[ 'status' ] = 'error'
    self.response[ 'error' ] = error
    self.response[ 'code' ] = code
    self.response[ 'request' ] = self.data
    return self

  
  @staticmethod
  def encoder(obj):
    if hasattr(obj, 'isoformat'):
      return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


  @staticmethod
  def error( request, message="", code=API_EXCEPTION, mimetype="application/json" ):
    e = {
      'status': 'error',
      'error' : message,
      'code'  : code
    }
    return HttpResponse(json.dumps(e), mimetype=mimetype)
