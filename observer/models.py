import json
from django import forms
from django.contrib.auth.models import User
from django.db import models

from walt.models import uuslug, WorkingDocument, Document



class Property(models.Model):
  '''
  All possible Observed properties, flattened. E.g. multiple choices fields are yes / no / None on a property.
  1. phase
  2. specific tag 'observate' category
  '''
  # 2. phases
  ANALYSIS      = 'analysis'
  EXPLORATION   = 'exploration'
  METHODOLOGY   = 'methodology'
  PARTICIPATION = 'participatio'
  PRESENTATION  = 'presentation'
  SOURCES       = 'sources'
  STATISTICS    = 'statistics'

  PHASE_CHOICES = (
    (ANALYSIS,      'analysis'),
    (EXPLORATION,   'exploration'),
    (METHODOLOGY,   'methodology'),
    (PARTICIPATION, 'participation'), # max length 12 reached here
    (PRESENTATION,  'presentation'),
    (SOURCES,       'sources'),
    (STATISTICS,    'statistics'),
  )
  # 3. property type. to be coupled with the question!
  
  ACTOR_TABLE     = 'actor_table'
  ARG_TREE        = 'arg_tree'
  COSMOGRAPHY     = 'cosmography'
  DIAGRAM         = 'diagram'
  SC_LIT          = 'sc_lit'
  SCIENTOMETRICS  = 'scientometri'
  METHODOLOGY     = 'tmethodology'
  QUAL_DA         = 'qual_da'
  SOURCES_DETAILS = 'sources_deta'
  COMMENTS        = 'comments'
  ANIMATION       = 'animation'
  COMIC           = 'comic'
  GLOSSARY        = 'glossary'
  VIZ_ANALOGY     = 'viz_analogy'
  STATS           = 'stats'

  METH_DETAILS_DATASETS   = 'details_data'
  METH_DETAILS_INTERVIEWS = 'details_inte'
  METH_DETAILS_NEWSPAPERS = 'details_news'
  METH_DETAILS_SITEVISIT  = 'details_site'

  TYPE_METH_DETAILS_CHOICES = ( # to be used as multiple choices inside the observer.forms.ProfileForm)
    (METH_DETAILS_DATASETS,   'they detail datasets'),
    (METH_DETAILS_INTERVIEWS, 'they detail interview'),
    (METH_DETAILS_NEWSPAPERS, 'they detail newspapers'),
    (METH_DETAILS_SITEVISIT,  'they detail site visit')
  )
  
  INTERVIEW_VIDEO      = 'interview_vi'
  INTERVIEW_AUDIO      = 'interview_au'
  INTERVIEW_TRANSCRIPT = 'interview_tr'
  INTERVIEW_NOTE       = 'interview_no'

  TYPE_INTERVIEW_CHOICES = (
    (INTERVIEW_VIDEO,      'video interview'),
    (INTERVIEW_AUDIO,      'audio interview'),
    (INTERVIEW_TRANSCRIPT, 'interview transcripted'),
    (INTERVIEW_NOTE,       'interview detailed notes'),
  )

  TYPE_CHOICES = (
    (ACTOR_TABLE,     'actor table'),
    (ARG_TREE,        'Argument Trees'),
    (COSMOGRAPHY,     'cosmography'),
    (DIAGRAM,         'Schematic process diagrams'),
    (SC_LIT,          'Analysis of scientific literature'),
    (SCIENTOMETRICS,  'Scientometric maps'),
    (METHODOLOGY,     'Methodology section'),
    (QUAL_DA,         'Qualitative data analysis'),
    (SOURCES_DETAILS, 'Index or list of sources'),
    (COMMENTS,        'Debate space'),
    (ANIMATION,       'animation'),
    (COMIC,           'Comics and Vignettes'),
    (GLOSSARY,        'Glossary'),
    (VIZ_ANALOGY,     'Visual Analogies'),
    (STATS,           'Statistics'),
  )

  type     = models.CharField(max_length=12, choices=TYPE_CHOICES + TYPE_METH_DETAILS_CHOICES + TYPE_INTERVIEW_CHOICES, null=True, blank=True) # e.g. 'author' or 'institution'
  phase    = models.CharField(max_length=12, choices=PHASE_CHOICES, null=True, blank=True) 
  slug     = models.SlugField(max_length=128, unique=True) # a simple way to access integrated stuffs


  def save(self, **kwargs):
    if self.pk is None:
      self.slug = uuslug(model=Property, instance=self, value='-'.join([self.phase, self.type]))
    super(Property, self).save()


  def json(self, deep=False):
    d = {
      'id': self.id,
      'slug': self.slug,
      'type': self.type
    }
    return d


  def __unicode__(self):
    return "%s %s" % (self.phase, self.type)


  class Meta:
    ordering = ["phase", "type"]
    unique_together = ("phase", "type")
    verbose_name_plural = "properties"



class Device(models.Model):
  '''
  When A tool has been used for a specific document?
  Json property: cfr DocumentProfile
  '''
  DATABASE = 'database'
  ACTOR_DIAG = 'actor_diag'
  ANALYSIS_SPECIAL = 'analysis_special'
  CHRONOLOGY = 'chronology'
  CRAWL      = 'crawl'
  EXPLORE_SPECIAL = 'explore_special'
  MEDIA_ANALYSIS = 'media_analysis'
  DISAGREEMENT = 'disagreement'
  EXT_CONTENT = 'ext_content'
  GEOLOCATION = 'geolocation'
  WEBTOOL = 'webtool'
  SNA = 'sna'
  TAGCLOUD = 'tagcloud'
  TEXT_ANALYSIS = 'text_analysis'

  TYPE_CHOICES = (
    (DATABASE, 'Databases'),
    (ACTOR_DIAG, 'Actor diagrams'),
    (ANALYSIS_SPECIAL, 'Specialised analysis Tools'),
    (CHRONOLOGY, 'Controversy Timeline'),
    (CRAWL,           'Web crawling maps'),
    (EXPLORE_SPECIAL, 'Specialised Search and Exploration Tools'),
    (MEDIA_ANALYSIS, 'Media and public opinion analysis '),
    (DISAGREEMENT, 'Presentation of the disagreement'),
    (EXT_CONTENT, 'External content'),
    (GEOLOCATION, 'Geographical maps'),
    (WEBTOOL, 'Web-site building tools'),
    (SNA, 'Social Network Analysis Tools'),
    (TAGCLOUD, 'Tag clouds'),
    (TEXT_ANALYSIS, 'Textual analysis'),
  )

  working_document = models.ForeignKey(WorkingDocument, related_name="supports")
  document = models.ForeignKey(Document, related_name="devices") # directly through a document
  type = models.CharField(max_length=12, choices=TYPE_CHOICES)


  def json(self, deep=False):
    d = {
      'id': self.working_document.id,
      'type': self.type,
      'slug': self.working_document.slug,
      'title': self.working_document.title
    }
    return d
  

  class Meta:
    unique_together = ("working_document", "document", "type")



class DocumentProfile(models.Model):
  '''
  A simple profile to analyse documents, or better a mediated table Document-Properties:
  document are given as foreign key and they share a number of properties.
  
  '''
  document = models.ForeignKey(Document, related_name="profile", unique=True)
  owner = models.ForeignKey(User) # who has compiled it

  date = models.DateField(blank=True, null=True) # main date, manually added
  date_created = models.DateTimeField(auto_now=True)
  date_last_modified = models.DateTimeField(auto_now_add=True)

  notes = models.TextField(blank=True) # free evaluation

  properties = models.ManyToManyField(Property, null=True, blank=True)
  

  def json(self, deep=False):
    d = {
      'id': self.document.id,
      'date': self.date.isoformat() if self.date else None,
      'date_created': self.date_created.isoformat(),
      'date_last_modified': self.date_last_modified.isoformat(),
      'notes': self.notes,
      'owner': self.owner.username
    }

    d['properties'] = []

    properties = [p.type for p in self.properties.all()]

    for t in Property.TYPE_CHOICES:
      d['properties'].append({'label':t[1], 'value': t[0] in properties})



    return d


  def __unicode__(self):
    return "%s" % self.document


  class Meta:
    ordering = ["-date_last_modified"]