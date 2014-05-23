import logging

from django.contrib.admin.views.decorators import staff_member_required

from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_HTTPERROR

from observer.models import DocumentProfile, Device, Property
from observer.forms import DeviceForm
from walt.models import Document


def index(request):
  return Epoxy(request).json()



@staff_member_required
def document_profiles(request):
  return Epoxy(request).queryset(DocumentProfile.objects.filter()).json()



@staff_member_required
def document_profile(request, document_pk):
  epoxy = Epoxy(request)
  try:
    p = DocumentProfile.objects.get(document__pk=document_pk)
  except DocumentProfile.DoesNotExist, e:
    # create document profile
    p = DocumentProfile(document=Document.objects.get(pk=document_pk), owner=request.user)
    p.save()
  except Document.DoesNotExist, e:
    return epoxy.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()
  
  if epoxy.is_POST():
    '''
    if not p.layout:
      return epoxy.throw_error(error='%s' % 'There is no Layout, babe', code=API_EXCEPTION_DOESNOTEXIST).json()
    
    form = p.layout.get_form(data=request.REQUEST)

    if not form.is_valid():
      return epoxy.throw_error(error='%s' % form.errors, code=API_EXCEPTION_FORMERRORS).json()

    for f in p.layout.questions.all():
      print f
    epoxy.meta('answ',form.cleaned_data)
    '''
    pass
  epoxy.item(p)
  return epoxy.json()



@staff_member_required
def document_profile_attach_property(request, document_pk, property_type):
  epoxy = Epoxy(request)
  pro,created = DocumentProfile.objects.get_or_create(document__pk=document_pk, defaults={
    'owner': request.user
  })
  if epoxy.is_POST():
    try:
      prop = Property.objects.get(type=property_type)
    except Property.DoesNotExist, e:
      return epoxy.throw_error(error='%s. I.E is not a valid property'%e, code=API_EXCEPTION_FORMERRORS).json()

    pro.properties.add(prop)
    pro.save()

  epoxy.item(pro, deep=True)
  return epoxy.json()



@staff_member_required
def document_profile_detach_property(request, document_pk, property_type):
  epoxy = Epoxy(request)
  pro, created = DocumentProfile.objects.get_or_create(document__pk=document_pk, defaults={
    'owner': request.user
  })
  if epoxy.is_POST():
    try:
      prop = Property.objects.get(type=property_type)
    except:
      return epoxy.throw_error(error='%s is not a valid property', code=API_EXCEPTION_FORMERRORS).json()

    pro.properties.remove(prop)
    pro.save()

  epoxy.item(pro, deep=True)
  return epoxy.json()


@staff_member_required
def devices(request):
  epoxy = Epoxy(request)
  
  if epoxy.is_POST():
    form = DeviceForm(epoxy.data)
    if form.is_valid():
      dev = form.save()
      epoxy.item(dev)
      return epoxy.json()
    else:
      return epoxy.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
  
  epoxy.queryset(Device.objects.filter())
  return epoxy.json()



@staff_member_required
def device(request, pk):
  epoxy = Epoxy(request)

  if epoxy.is_DELETE:
    try:
      Device.objects.get(pk=pk).delete()
    except Device.DoesNotExist, e:
      return epoxy.json()
  return epoxy.json()


