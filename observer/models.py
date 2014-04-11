import json
from django import forms
from django.contrib.auth.models import User
from django.db import models

from walt.models import uuslug



class LayoutField(models.Model):
  NULL_BOOLEAN = 'NullBooleanField'
  CHAR = 'CharField', # max 160 chars
  TEXT = 'TextField', # charfield with TEXTAREA widget
  CHOICE = 'ChoiceField', # use filters as LIST
  MODEL_CHOICE = 'ModelChoiceField'
  MODEL_MULTIPLE_CHOICE = 'ModelMultipleChoiceField'

  TYPE_CHOICES = (
    (NULL_BOOLEAN, 'Checkbox'),
    (CHAR, 'CharField, max 160 chars'),
    (TEXT, 'TextField'),
    (CHOICE, 'ChoiceField'),
    (MODEL_CHOICE, 'ModelChoiceField. Cfr https://docs.djangoproject.com/en/dev/ref/forms/fields/#modelmultiplechoicefield'),
    (MODEL_MULTIPLE_CHOICE, 'ModelMultipleChoiceField. Cfr https://docs.djangoproject.com/en/dev/ref/forms/fields/#modelmultiplechoicefield'),
  )

  question = models.TextField() # that is the question
  
  type = models.CharField(max_length=24, choices=TYPE_CHOICES) 

  filters = models.TextField(blank=True, null=True) # in the form of a json dict only. cfr. validation
  modelname = models.CharField(max_length=128, blank=True, null=True) # in the form "app.model" 'walt.WorkingDocument'. useful to decide which LayoutValue class need to be used to store the value.
  

  def get_queryset(self):
    '''
    Return the queryset to be used inside the <observer.Layout instance>.get_form() method
    Note: for type MODEL_CHOICE or MODEL_MULTIPLE_CHOICE ONLY.
    '''
    mod = models.loading.get_model(*self.modelname.split('.',1))
    qs = mod.objects.filter(**json.loads(self.filters))
    return qs


  def json(self, deep=False):
    d = {
      'question': self.question,
      'type': self.type
    }

    if self.type in [LayoutField.MODEL_CHOICE, LayoutField.MODEL_MULTIPLE_CHOICE]:
      d['filters'] = json.loads(self.filters)
      d['modelname'] = json.loads(self.modelname)
    elif self.type == LayoutField.CHOICE:
      d['filters'] = json.loads(self.filters) # json as key value props just like choice field.

    return d


  def __unicode__(self):
    return "%s %s" % (self.section, self.question)



class LayoutValue(models.Model):
  field = models.ForeignKey(LayoutField)

  # possible values below
  null_boolean_value = models.NullBooleanField(null=True)
  char_value = models.CharField(max_length=160, null=True, blank=True) # this is the answer. A generic container, we do not need it to be dynamic.
  text_value = models.TextField(null=True, blank=True)

  # multiple items. 
  items = models.ManyToManyField('walt.WorkingDocument')


  def save(self, **kwargs):
    '''
    this method verify that a null_boolean FIELD correspond a null_boolean value.. Raise Exception.
    '''
    super(LayoutValue, self).save()



class Layout(models.Model):
  name = models.CharField(max_length=32)
  slug = models.SlugField(max_length=32, null=True, blank=True, unique=True)
  fields = models.ManyToManyField(LayoutField, through='Question')
  
  # return a form dynamically basesd on Layout information
  def get_form(self, **kwargs):
    class DForm(forms.Form):
      def __init__(self, layout, *args, **kwargs):
        super(DForm, self).__init__(*args, **kwargs)
        for fs in layout.questions.all():
          fieldclass = getattr(forms, fs.field.type)
          if fs.field.type in [LayoutField.MODEL_CHOICE, LayoutField.MODEL_MULTIPLE_CHOICE]:
            self.fields['field_%s_%s' % (fs.slug, fs.id)] = fieldclass(queryset=fs.field.get_queryset(), label=fs.field.question)
          else:
            self.fields['field_%s_%s' % (fs.slug, fs.id)] = fieldclass(label=fs.field.question)
    
    return DForm(self, **kwargs)


  def save(self, **kwargs):
    if self.pk is None:
      self.slug = uuslug(model=Layout, instance=self, value=self.name)
    super(Layout, self).save()


  def json(self, deep=False):
    d = {
      'id': self.pk,
      'name': self.name,
      'fields': [q.json() for q in self.questions.all()]
    }
    return d


  def __unicode__(self):
    return "%s" % self.name



class Question(models.Model):
  '''
  Links LayoutField and Layout. Each Fielad belongs to a section. The list of
  Layout related field willl be sorted by section+position
  '''
  layout = models.ForeignKey(Layout, related_name="questions")
  field = models.ForeignKey(LayoutField, related_name="section")
  position = models.IntegerField(default=0, blank=True, null=True) #the sorting index
  section = models.CharField(max_length=32)
  slug = models.SlugField(max_length=32)


  def save(self, **kwargs):
    if self.pk is None and self.position == 0: # aka default position, or the very first Item
      self.position = Question.objects.filter(layout=self.layout, slug=self.slug).count() + 1
    super(Question, self).save()


  def json(self, deep=False):
    d = {
      'id': self.pk,
      'section' : self.section,
      'position': self.position,
      'field': self.field.json()
    }
    return d


  def __unicode__(self):
    return "%s/%s: %s" % (self.section, self.position, self.field.type)


  class Meta:
    ordering = ['slug','position']
    unique_together = ("layout", "field")



class DocumentProfile(models.Model):
  '''
  A simple profile to analyse documents (instead of multiple tags).
  Document are given as foreign key and there are profile specific boolean tags and Profile Tags.
  Profile tags' model is Tag, because those tags can be used somewhere else like "audio interviews".
  '''
  document = models.ForeignKey('walt.Document', unique=True)
  layout = models.ForeignKey(Layout)
  owner = models.ForeignKey(User) # who has compiled it

  date = models.DateField(blank=True, null=True) # main date, manually added
  date_created = models.DateTimeField(auto_now=True)
  date_last_modified = models.DateTimeField(auto_now_add=True)

  notes = models.TextField(blank=True)

  values = models.ManyToManyField(LayoutValue, null=True, blank=True)
  tags = models.ManyToManyField('walt.Tag', null=True, blank=True)


  def json(self, deep=False):
    d = {
      'id': self.document.id,
      'layout': self.layout.json(),
      'date': self.date.isoformat() if self.date else None,
      'date_created': self.date_created.isoformat(),
      'date_last_modified': self.date_last_modified.isoformat(),
      'notes': self.notes,
      'owner': self.owner.username
    }
    return d


  def __unicode__(self):
    return "%s" % self.document
