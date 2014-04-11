import logging

from django.contrib.admin.views.decorators import staff_member_required

from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_HTTPERROR

from observer.models import Layout, DocumentProfile



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
    return epoxy.throw_error(error='%s' % e, code=API_EXCEPTION_DOESNOTEXIST).json()
  
  if epoxy.is_POST():
    if not p.layout:
      return epoxy.throw_error(error='%s' % 'There is no Layout, babe', code=API_EXCEPTION_DOESNOTEXIST).json()
    
    form = p.layout.get_form(data=request.REQUEST)

    if not form.is_valid():
      return epoxy.throw_error(error='%s' % form.errors, code=API_EXCEPTION_FORMERRORS).json()

    for f in p.layout.questions.all():
      print f
    epoxy.meta('answ',form.cleaned_data)
  epoxy.item(p)
  return epoxy.json()



@staff_member_required
def layouts(request):
  '''
  get all available observers layouts
  '''
  return Epoxy(request).queryset(Layout.objects.filter()).json()



@staff_member_required
def layout(request):
  return Epoxy(request).json()