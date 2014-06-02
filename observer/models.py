import json
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

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
    (ANALYSIS,      _('analysis')),
    (EXPLORATION,   _('exploration')),
    (METHODOLOGY,   _('methodology')),
    (PARTICIPATION, _('participation')), # max length 12 reached here
    (PRESENTATION,  _('presentation')),
    (SOURCES,       _('sources')),
    (STATISTICS,    _('statistics')),
  )
  # 3. property type. to be coupled with the question!
  ACTOR_DESC      = 'actor_desc'
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

  ACTOR_DESC_TABLE      = 'actor_desc_t'
  ACTOR_DESC_CLASSIF    = 'actor_desc_c'
  ACTOR_DESC_FLAT_LIST  = 'actor_desc_f'

  TYPE_ACTOR_DESC_CHOICES = ( # to be used as multiple choices inside the observer.forms.ProfileForm)
    (ACTOR_DESC_TABLE,   _('actor argument tables')),
    (ACTOR_DESC_CLASSIF, _('actor classification')),
    (ACTOR_DESC_FLAT_LIST, _('actor flat list')),
  )

  METH_DETAILS_DATASETS   = 'details_data'
  METH_DETAILS_INTERVIEWS = 'details_inte'
  METH_DETAILS_NEWSPAPERS = 'details_news'
  METH_DETAILS_SOCIALNETW = 'details_soci'
  METH_DETAILS_SITEVISIT  = 'details_site'

  TYPE_METH_DETAILS_CHOICES = ( # to be used as multiple choices inside the observer.forms.ProfileForm)
    (METH_DETAILS_DATASETS,   _('they detail datasets')),
    (METH_DETAILS_INTERVIEWS, _('they detail interview')),
    (METH_DETAILS_NEWSPAPERS, _('they detail newspapers')),
    (METH_DETAILS_SOCIALNETW, _('they detail social Network')),
    (METH_DETAILS_SITEVISIT,  _('they detail site visit')),
  )
  
  INTERVIEW_VIDEO      = 'interview_vi'
  INTERVIEW_AUDIO      = 'interview_au'
  INTERVIEW_TRANSCRIPT = 'interview_tr'
  INTERVIEW_NOTE       = 'interview_no'

  TYPE_INTERVIEW_CHOICES = (
    (INTERVIEW_VIDEO,      _('video interview')),
    (INTERVIEW_AUDIO,      _('audio interview')),
    (INTERVIEW_TRANSCRIPT, _('interview transcripted')),
    (INTERVIEW_NOTE,       _('interview detailed notes')),
  )

  TYPE_CHOICES = (
    (ACTOR_TABLE,     _('actor table')),
    (ARG_TREE,        _('Argument Trees')),
    (COSMOGRAPHY,     _('cosmography')),
    (DIAGRAM,         _('Schematic process diagrams')),
    (SC_LIT,          _('Analysis of scientific literature')),
    (SCIENTOMETRICS,  _('Scientometric maps')),
    (METHODOLOGY,     _('Methodology section')),
    (QUAL_DA,         _('Qualitative data analysis')),
    (SOURCES_DETAILS, _('Index or list of sources')),
    (COMMENTS,        _('Debate space')),
    (ANIMATION,       _('animation')),
    (COMIC,           _('Comics and Vignettes')),
    (GLOSSARY,        _('Glossary')),
    (VIZ_ANALOGY,     _('Visual Analogies')),
    (STATS,           _('Statistics')),
  )

  type     = models.CharField(max_length=12, choices=TYPE_CHOICES + TYPE_METH_DETAILS_CHOICES + TYPE_INTERVIEW_CHOICES + TYPE_ACTOR_DESC_CHOICES, null=True, blank=True) # e.g. 'author' or 'institution'
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
  @todo maybe in @save restrict to workingdocument of type tools ?
  Json property: cfr DocumentProfile
  '''
  DATABASE = 'database'
  ACTOR_DIAG = 'actor_diag'
  ANALYSIS_SPECIAL = 'analysis_spe'
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
    (DATABASE, _('Databases')),
    (ACTOR_DIAG, _('Actor diagrams')),
    (ANALYSIS_SPECIAL, _('Specialised analysis Tools')),
    (CHRONOLOGY, _('Controversy Timeline')),
    (CRAWL,           _('Web crawling maps')),
    (EXPLORE_SPECIAL, _('Specialised Search and Exploration Tools')),
    (MEDIA_ANALYSIS, _('Media and public opinion analysis')),
    (DISAGREEMENT, _('Presentation of the disagreement')),
    (EXT_CONTENT, _('External content')),
    (GEOLOCATION, _('Geographical maps')),
    (WEBTOOL, _('Web-site building tools')),
    (SNA, _('Social Network Analysis Tools')),
    (TAGCLOUD, _('Tag clouds')),
    (TEXT_ANALYSIS, _('Textual analysis')),
  )

  working_document = models.ForeignKey(WorkingDocument, related_name="supports")
  document = models.ForeignKey(Document, related_name="devices") # directly through a document
  type = models.CharField(max_length=24, choices=TYPE_CHOICES)


  def json(self, deep=False):
    d = {
      'id': self.id,
      'working_document_id': self.working_document.id,
      'working_document_slug': self.working_document.slug,
      'document_id': self.document.id,
      'type': self.type,
      'type_label': _(self.get_type_display()),
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
  ANALYSIS      = 'analysis'
  EXPLORATION   = 'exploration'
  METHODOLOGY   = 'methodology'
  PARTICIPATION = 'participatio'
  PRESENTATION  = 'presentation'
  SOURCES       = 'sources'
  STATISTICS    = 'statistics'

  QUESTIONS = ( # ex Property phase choices... keep them before changing their model.
    (ANALYSIS, (
      (Property.ACTOR_DESC_TABLE, _('question_actor_desc_t'), _('description_actor_desc_t')),
      (Property.ACTOR_DESC_CLASSIF, _('question_actor_desc_c'), _('description_actor_desc_c')),
      (Property.ACTOR_DESC_FLAT_LIST, _('question_actor_desc_f'), _('description_actor_desc_f')),
      (Property.ARG_TREE, _('question_arg_tree'), _('description_arg_tree')),
      (Property.COSMOGRAPHY, _('question_cosmography'), _('description_cosmography')),
      (Property.DIAGRAM, _('question_diagram'), _('description_diagram')),
      (Property.SC_LIT, _('question_sc_lit'), _('description_sc_lit')),
      (Property.SCIENTOMETRICS, _('question_scientometri'), _('description_scientometri')),
    )),
    #(EXPLORATION, (
    #
    #)),
    (METHODOLOGY, (
      (Property.METH_DETAILS_DATASETS   , _('question_details_data'), _('description_details_data')),
      (Property.METH_DETAILS_INTERVIEWS , _('question_details_inte'), _('description_details_inte')),
      (Property.METH_DETAILS_NEWSPAPERS , _('question_details_news'), _('description_details_news')),
      (Property.METH_DETAILS_SOCIALNETW , _('question_details_soci'), _('description_details_soci')),
      (Property.METH_DETAILS_SITEVISIT  , _('question_details_site'), _('description_details_site')),
      (Property.METHODOLOGY, _('question_tmethodology'), _('description_tmethodology')),
      (Property.QUAL_DA, _('question_qual_da'), _('description_qual_da')),
      (Property.SOURCES_DETAILS, _('question_sources_deta'), _('description_sources_deta')),
    )),
    (PARTICIPATION, (
      (Property.COMMENTS, _('question_comments'), _('description_comments')),
    )),
    (PRESENTATION, (
      (Property.ANIMATION, _('question_animation'), _('description_animation')),
      (Property.COMIC, _('question_comic'), _('description_comic')),
      (Property.GLOSSARY, _('question_glossary'), _('description_glossary')),
      (Property.VIZ_ANALOGY, _('question_viz_analogy'), _('description_viz_analogy')),
    )),
    (SOURCES, (
      (Property.INTERVIEW_TRANSCRIPT, _('question_interview_tr'), _('description_interview_tr')),
      (Property.INTERVIEW_VIDEO, _('question_interview_vi'), _('description_interview_vi')),
      (Property.INTERVIEW_AUDIO, _('question_interview_au'), _('description_interview_au')),
      (Property.INTERVIEW_NOTE, _('question_interview_no'), _('description_interview_no')),
    )),  
    (STATISTICS, (
      (Property.STATS, _('question_stats'), _('description_stats')),
    )),
  )

  QUESTION_DEVICES = (
    (Device.DATABASE, _('question_database'), _('description_database')),
    (Device.ANALYSIS_SPECIAL, _('question_analysis_spe'), _('description_analysis_spe')),
    (Device.CHRONOLOGY, _('question_chronology'), _('description_chronology')),
    (Device.CRAWL, _('question_crawl'), _('description_crawl')),
    (Device.EXPLORE_SPECIAL, _('question_explore_special'), _('description_explore_special')),
    (Device.MEDIA_ANALYSIS, _('question_media_analysis'), _('description_media_analysis')),
    (Device.DISAGREEMENT, _('question_disagreement'), _('description_disagreement')),
    (Device.EXT_CONTENT, _('question_ext_content'), _('description_ext_content')),
    (Device.GEOLOCATION, _('question_geolocation'), _('description_geolocation')),
    (Device.WEBTOOL, _('question_webtool'), _('description_webtool')),
    (Device.SNA, _('question_sna'), _('description_sna')),
    (Device.TAGCLOUD, _('question_tagcloud'), _('description_tagcloud')),
    (Device.TEXT_ANALYSIS, _('question_text_analysis'), _('description_text_analysis')),
  )

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

    d['questions'] = []
    d['properties'] = []
    d['properties_interviews'] = []
    d['properties_meth_detail'] = []
    d['devices'] = [] # just labels in order to fill the form

    properties = [p.type for p in self.properties.all()]

    #REPETITA IUVANT :D
    # start following questions
    for q in DocumentProfile.QUESTIONS:
      d['questions'].append({
        'section': q[0],
        'properties': [{'name':p[0], 'question': p[1], 'description': p[2], 'value': p[0] in properties} for p in q[1]]
      })

    for t in Property.TYPE_CHOICES:
      d['properties'].append({
        'label':_(t[1]),
        'name':t[0], # this should be the unique id.... @todo!
        'value': t[0] in properties, # does this profile has that type ?
        'question': _('question_%s' % t[0])
      })

    for t in Property.TYPE_INTERVIEW_CHOICES:
      d['properties_interviews'].append({
        'label':t[1],
        'name':t[0],
        'value': t[0] in properties,
        'question': _('question_%s' % t[0])
      })

    for t in Property.TYPE_METH_DETAILS_CHOICES:
      d['properties_meth_detail'].append({
        'label':t[1],
        'name':t[0],
        'value': t[0] in properties,
        'question': _('question_%s' % t[0])
      })

    for t in Device.TYPE_CHOICES:
      d['devices'].append({'label':t[1], 'name':t[0]})


    return d


  def __unicode__(self):
    return "%s" % self.document


  class Meta:
    ordering = ["-date_last_modified"]