#!/usr/bin/python
# -*- coding: utf-8 -*-

from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_HTTPERROR
from observer.forms import FullDocumentForm
from observer.models import Document

# 
#  helper get_available_documents
#  ===
#
#  Return a queryset according to user auth level and document status
#  
#  @param request
#  @return django.model.Queryset
# 
def get_available_documents(request):
  
  if request.user.is_staff:
    queryset = Document.objects.filter().distinct()
  elif request.user.is_authenticated():
    queryset = Document.objects.filter(Q(status=Document.PUBLIC) | Q(owner=request.user) | Q(authors=request.user)).distinct()
  else:
    queryset = Document.objects.filter(status=Document.PUBLIC).distinct()
  return queryset

# 
#  api:/
#  main entrance
#
def index(req):
  return Epoxy(req).json()


# 
#  api:/documents
#  retrieve the requested documents and handle POST requests.
#  At present, only staff can add documents.
#
def documents(req):
  res = Epoxy(req)
  if res.is_POST(): # staff only can add document via api
    if not req.user.is_staff:
      return res.throw_error(error='', code=API_EXCEPTION_AUTH).json()

    form = FullDocumentForm(res.data)
    if not form.is_valid():
      return res.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()

    doc = form.save(commit=False)
    doc.owner = req.user

    doc.save()
    return res.item(doc).json()

  queryset = get_available_documents(req)
  res.queryset(queryset)
  res.meta('query', '%s' % res._queryset.query)
  return res.json()



