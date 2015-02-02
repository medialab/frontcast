#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q

from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_HTTPERROR
from observer.forms import DeviceForm, FullDocumentForm
from observer.models import Device, Document


# 
# helper is_number
# ===
# Determine if a string may be interpreted as a number (float value)
#
def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


# 
#  helper get_available_document
#  ===
#
#  @param request
#  @param django.db.models.Q instance
#  @return <observer.models.Dpcument> or raise exception
# 
def get_available_document(request, q):
  '''
  @param request
  @return <walt.models.Dpcument> or raise exception
  '''
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
#  api:/document
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


# 
#  api:/document/(?P<pk>[:a-zA-Z\.\-\d]+)
#  retrieve the requested document by numeric ID or by its SLUG field. and handle POST requests.
#  At present, only staff can add documents.
#
def document(req, pk):
  res = Epoxy(request)

  try:
    doc = get_available_document(req, Q(pk=pk) if is_number(pk) else Q(slug=pk))
  except Document.DoesNotExist, e:
    return res.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()
  
  if epoxy.is_POST():
    is_valid, doc = edit_object(instance=doc, Form=FullDocumentForm, request=req, epoxy=res)
    if is_valid:
      doc.save()

  return res.item(doc, deep=True).json()


#
# api:/device
# Get or create new device by using forms.DeviceForm
# accessible by staff only
@staff_member_required
def devices(req):
  res = Epoxy(req)
  
  if res.is_POST():
    form = DeviceForm(res.data)
    if form.is_valid():
      dev = form.save()
      res.item(dev)
      return res.json()
    else:
      return res.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
  
  res.queryset(Device.objects.filter())
  return res.json()


#
# api:/device
# Get or create new device by using forms.DeviceForm
# accessible by staff only
@staff_member_required
def device(req, pk):
  res = Epoxy(req)
  
  try:
    dev = Device.objects.get(pk=pk)
  except Device.DoesNotExist, e:
    return res.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()

  if res.is_DELETE():
    dev.delete()
  
  return res.item(doc, deep=True).json()

