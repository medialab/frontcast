#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

from django.db.models import Count, Q
from django.conf import settings
from django.utils.text import slugify
from walt.models import Assignment, Task, Tag, Document, WorkingDocument



def is_number(s):
  '''
  Determine if a string may be interpreted as a number (float value)
  '''
  try:
    float(s)
    return True
  except ValueError:
    return False



def get_pending_assignments( user ):
  '''
  get pending assignments
  DEPRECATED

    @param user instance of<User>
    @return <Assignment_set>
  '''
  assignments = Assignment.objects.filter(unit__profile__user=user)
  return assignments



def unicode_dict_reader(utf8_data, **kwargs):
  '''
  Smart csv reader for unicode chars
  '''
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
      yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])



def get_available_document(request, pk):
  '''
  @param request
  @return <walt.models.Dpcument> or raise exception
  '''
  q = Q(pk=pk) if is_number(pk) else Q(slug=pk)

  try:
    if request.user.is_staff:
      d = Document.objects.get(q)
    elif request.user.is_authenticated():
      d = Document.objects.get(q, Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user))
    else:
      d = Document.objects.get(q, status=Document.PUBLIC)
  except Document.DoesNotExist, e:
    raise

  return d



def get_available_documents(request):
  '''
  Return a queryset according to user auth level and document status
  @param request
  @return <django.model.Queryset>
  '''
  if request.user.is_staff:
    queryset = Document.objects.filter().distinct()
  elif request.user.is_authenticated():
    queryset = Document.objects.filter(Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user)).distinct()
  else:
    queryset = Document.objects.filter(status=Document.PUBLIC).distinct()
  return queryset



def get_available_working_documents(request):
  '''
  Return a queryset according to user auth level and document status
  @param request
  @return <django.model.Queryset>
  '''
  queryset = WorkingDocument.objects.filter().distinct()
  return queryset
  


def get_document_filters(queryset):
  filters = {'type': {}, 'year': {}, 'tags':{}, 'tools':{} }
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

  #print 'IDS', ids, ','.join(str(v) for v in ids)
  # 3. get document tags. @TODO imporve performances.
  # TOO MANY VALUE ERROR POSSIBLE. TO be reviewed!!!!!!
  # possible solution: split ids in array of 50.
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


  tools = WorkingDocument.objects.raw('''
    SELECT 
    COUNT(od.document_id) as distribution,
    wd.id,
    wd.slug,
    wd.title
    FROM observer_device od
    JOIN walt_workingdocument wd ON od.working_document_id = wd.id
    JOIN walt_document d ON od.document_id = d.id
    WHERE d.id in (%s)
    GROUP BY working_document_id
    ORDER BY distribution DESC
    ''' % ','.join(str(v) for v in ids)
  )

  for t in tools:
    _slug = '%s' % t.slug
    print t.slug
    filters['tools'][_slug] = {
      'id':    t.id, 
      'slug':  t.slug,
      'title': t.title,
      'count': t.distribution
    }

   

  return filters



def get_working_document_filters(queryset):
  filters = {'type': {}, 'year': {}, 'tags':{}, 'tools':{} }
  ids = []

  # 2. get document ids involved
  for d in queryset:
    ids.append(d.id)

  #print 'IDS', ids, ','.join(str(v) for v in ids)
  # 3. get document tags. @TODO imporve performances.
  # TOO MANY VALUE ERROR POSSIBLE. TO be reviewed!!!!!!
  # possible solution: split ids in array of 50.
  tag_queryset = Tag.objects.filter(workingdocument__id__in=ids)
  print tag_queryset.query
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