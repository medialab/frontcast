from django.contrib.auth.models import User
from django.db import models

from walt.models import uuslug



class LayoutField(models.Model):
  BOOLEAN = 'BooleanField'
  CHAR = 'CharField'
  MODEL_CHOICE = 'ModelChoiceField'
  MODEL_MULTIPLE_CHOICE = 'ModelMultipleChoiceField'

  TYPE_CHOICES = (
    (BOOLEAN, 'BooleanField'),
    (CHAR, 'CharField'),
    (MODEL_CHOICE, 'ModelChoiceField. Cfr https://docs.djangoproject.com/en/dev/ref/forms/fields/#modelmultiplechoicefield'),
    (MODEL_MULTIPLE_CHOICE, 'ModelMultipleChoiceField. Cfr https://docs.djangoproject.com/en/dev/ref/forms/fields/#modelmultiplechoicefield'),
  )

  question = models.TextField() # that is the question
  
  type = models.CharField(max_length=12, choices=TYPE_CHOICES) 

  filters = models.TextField(blank=True, null=True) # in the form of a json dict only. cfr. validation
  modelname = models.CharField(max_length=128, blank=True, null=True) # in the form "app.model" 'walt.WorkingDocument'. useful to decide which LayoutValue class need to be used to store the value.
  

  def get_queryset(self):
    '''
    Return the queryset to be used inside the <observer.Layout instance>.get_form() method
    Note: for type MODEL_CHOICE or MODEL_MULTIPLE_CHOICE ONLY.
    '''
    mod = models.loading.get_model(*self.modelname.split('.',1))
    qs = mod.objects.filters(**self.filters)
    return qs


  def __unicode__(self):
    return "%s" % self.question


class LayoutValue(models.Model):
  field = models.ForeignKey(LayoutField)



class WorkingDocumentLayoutValue(LayoutValue):
  items = models.ManyToManyField('walt.WorkingDocument')



class Layout(models.Model):
  name = models.CharField(max_length=32)
  slug = models.SlugField(max_length=32, null=True, blank=True, unique=True)
  fields = models.ManyToManyField(LayoutField, through='Section')
  
  # create a form dynamically basesd on Layout information
  def get_form(self):
    pass


  def save(self, **kwargs):
    if self.pk is None:
      self.slug = uuslug(model=Layout, instance=self, value=self.name)
    super(Layout, self).save()


  def __unicode__(self):
    return "%s" % self.name



class Section(models.Model):
  '''
  Links LayoutField and Layout. Each Fielad belongs to a section. The list of
  Layout related field willl be sorted by section+position
  '''
  layout = models.ForeignKey(Layout)
  field = models.ForeignKey(LayoutField)
  position = models.IntegerField(default=0, blank=True, null=True) #the sorting index
  section = models.CharField(max_length=32)
  slug = models.SlugField(max_length=32)


  def save(self, **kwargs):
    if self.pk is None:
      self.slug = uuslug(model=Section, instance=self, value=self.section)
      if self.position == 0: # aka default, or the very first Item
        self.position = Section.objects.filter(layout=self.layout, slug=self.slug).count()
    super(Section, self).save()


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


  def __unicode__(self):
    return "%s" % self.document
