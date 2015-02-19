from django.db.models.loading import get_model
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import ModelForm
from django.forms.models import model_to_dict

from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_ATTRIBUTEERROR



def index(request):
  '''
  Help or manual should be placed here
  '''
  result = Epoxy(request)
  return result.json()



def access_denied(request):
  '''
  Denial of access if user ios not staff.
  '''
  return Epoxy.error(request, message='access denied');



@staff_member_required
def get_objects(request, app_name, model_name):
  '''
  This is for debug purposes only. Please provide specific api method inside your own app.api.py file.
  '''
  epoxy = Epoxy(request)

  try:
    mod = get_model(app_name, model_name)
  except AttributeError, e:
    return epoxy.throw_error(error='model "%s" not found' % model_name, code=API_EXCEPTION_ATTRIBUTEERROR)
  
  if epoxy.is_POST():
    class ObjForm(ModelForm):
      class Meta:
        model = mod
        exclude =()

    form = ObjForm(epoxy.data)
    if form.is_valid():
      item = form.save(commit=False)
      epoxy.add('item', item.json() if hasattr(item, 'json') else model_to_dict(item))
      item.save()
    else:
      return epoxy.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
  queryset = mod.objects.filter()
  
  epoxy.queryset(
    queryset,
    model=mod
  )

  epoxy.meta('module', '%s.%s' % (mod.__module__, mod.__name__))
  return epoxy.json()



@staff_member_required
def get_object(request, app_name, model_name, pk):
  '''
  This is for debug purposes only. Please provide specific api method inside your own app.api.py file.
  '''
  result = Epoxy(request)
  mod = get_model(app_name, model_name)
  try:
    obj = mod.objects.get(pk=pk)
  except mod.DoesNotExist, e:
    return Epoxy.error(request, message="%s" % e, code=API_EXCEPTION_DOESNOTEXIST)

  if result.is_POST():
    class ObjForm(ModelForm):
      class Meta:
        model = mod
        exclude =[f.name for f in obj._meta.many_to_many]
    
    data = model_to_dict(obj)
    data.update(request.REQUEST)

    form = ObjForm(instance=obj, data=data)

    if form.is_valid():
      obj = form.save()
    else:
      return result.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
    
    result.item(obj)
  elif result.is_DELETE():
    obj.delete()
  else:
    result.item(obj)

  return result.json()



@staff_member_required
def get_object_m2m(request, app_name, model_name, pk, m2m_name):
  '''
  This is for debug purposes only. Please provide specific api method inside your own app.api.py file.
  '''
  result = Epoxy(request)
  mod = get_model(app_name, model_name)
  try:
    obj = mod.objects.get(pk=pk)
    result.item(obj)
    result.add('objects', [model_to_dict(i) for i in getattr(obj, m2m_name).all()])
  except mod.DoesNotExist, e:
    return Epoxy.error(request, message="%s" % e, code=API_EXCEPTION_DOESNOTEXIST)
  except AttributeError, e:
    return Epoxy.error(request, message="%s" % e, code=API_EXCEPTION_DOESNOTEXIST)

  return result.json()




def edit_object(instance, Form, epoxy):
  '''
  usage:
  def instanceapi(request):
    epoxy = Epoxy(request)
    # load the instance to be changed...
    if epoxy.is_POST:
      result, instance = edit_object(instance=instance, Form=InstanceModelForm)
    if not result:
      return epoxy.throw_error(error=instance, code=API_EXCEPTION_FORMERRORS).json()
    instance.save()
    return epoxy.item(instance, deep=True).json()
  '''
  data = model_to_dict(instance)
  data.update(epoxy.data)
  
  form = Form(instance=instance, data=data)
  if form.is_valid():
    instance = form.save(commit=False)
  return form, instance