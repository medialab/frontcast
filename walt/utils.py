import csv

from django.db.models import Count
from django.conf import settings
from walt.models import Assignment, Task, Tag, Document

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

#
#
#   @param user instance of<User>
#
#   @return <Assignment_set>
def get_pending_assignments( user ):
  assignments = Assignment.objects.filter(unit__profile__user=user)
  return assignments


def unicode_dict_reader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])

# #
# @param request
# @return <django.model.Queryset>
#
def get_available_documents(request):
  if request.user.is_staff:
    queryset =   Document.objects.filter().distinct()
  elif request.user.is_authenticated():
    queryset =   Document.objects.filter(Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user)).distinct()
  else:
    queryset = Document.objects.filter(status=Document.PUBLIC).distinct()
  return queryset


def get_document_filters(queryset):
  filters = {'type': {}, 'year': {}, 'tags':{} }
  ids = []

  for t in queryset.order_by().values('type').annotate(count=Count('id')):
    filters['type']['%s'%t['type']] = {
      'count': t['count']
    }

  for t in queryset.order_by().values('date').annotate(count=Count('id')):
    filters['year']['%s'%t['date']] = {
      'count': t['count']
    }

  # 2. get document ids involved
  for d in queryset:
    ids.append(d.id)

  # 3. get document tags. @TODO imporve performances
  
  tag_queryset = Tag.objects.filter(document__id__in=ids)
  
  for t in tag_queryset:
    _type = '%s' % t.type
    _slug = '%s' % t.slug

    if _type not in filters['tags']:
      filters['tags'][_type] = {}

    if _slug not in filters['tags'][_type]:
      filters['tags'][_type][_slug] = {
        'name': t.name,
        'slug': t.slug,
        'ids':[],
        'count': 0
      }
    
    # for debug purpose only, normally document-tag relationships are unique for each type and slug. filters['tags'][_type][_slug]['ids'].append(t.doc_id)
    filters['tags'][_type][_slug]['count'] += 1

  return filters
