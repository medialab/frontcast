#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json, operator

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count, Q
from django.utils.translation import ugettext as _

from observer.helpers import uuslug, profiler





#
#  AbstractDocument
#   
#  base class for both Document and WorkingDocument
#  Among its porperties:
#  - ownership of the document
#  - last modification date
#
class AbstractDocument(models.Model):
  # the text content
  slug = models.SlugField(max_length=160, unique=True)
  title = models.CharField(max_length=160, default="")
  abstract = models.TextField(default="", blank=True, null=True)
  content = models.TextField(default="", blank=True, null=True)
  language =  models.CharField(max_length=2, default='en', choices=settings.LANGUAGES, blank=True, null=True)
  rating = models.PositiveSmallIntegerField(default=0, blank=True, null=True) # 0 to 10

  # TIME
  date = models.DateField(blank=True, null=True) # main date, manually added
  date_last_modified = models.DateTimeField(auto_now=True) #cfr save() method

  # who first created it.
  owner = models.ForeignKey(User) # the original owner
  
  # external permalink.  
  permalink  = models.TextField(default="", blank=True, null=True) # remote link
  permalink_hash  = models.CharField(max_length=32, blank=True, null=True) # remote link

  
  class Meta:
    abstract = True

#
#  Tag
#  
#  pseudo free tags
#  feel free to add tag type to this model ... :D
#
class Tag(models.Model):
  FREE = '' # i.e, no special category at all, given by default
  AUTHOR = 'Au'
  KEYWORD = 'Ke'
  INSTITUTION = 'In'
  RESEARCHER = 'Rs'
  PLACE = 'Pl'
  DATE = 'Da'
  GEOCOVER = 'GC'
  ACTION = '!A'
  RATING = 'Ra'
  COURSE = 'Co'
  COVER_URL = 'CU'
  FAMILY = 'CA' # type/value tag ! for working document
  COPYRIGHT = 'CP' # open source, for working document
  REMOTE = 'RE' # is remote or local for working document

  OEMBED_PROVIDER_NAME = 'OP' #tag specify an oembed field...
  OEMBED_TITLE = 'OT' #tag specify an oembed field...
  OEMBED_THUMBNAIL_URL = 'OH'

  TYPE_OEMBED_CHOICES = (
    (OEMBED_PROVIDER_NAME, 'oembed_provider_name'),
    (OEMBED_TITLE, 'oembed_title'),
    (OEMBED_THUMBNAIL_URL, 'oembed_thumbnail_url'),
  )

  TYPE_IN_FACETS = (
    (FREE, 'no category'),
    (AUTHOR, 'AUTHOR'),
    (KEYWORD, 'KEYWORD'),
    (INSTITUTION, 'Institution'),
  )

  TYPE_CHOICES = (
    (FREE, 'no category'),
    (AUTHOR, 'AUTHOR'),
    (KEYWORD, 'KEYWORD'),
    (INSTITUTION, 'Institution'),
    (RESEARCHER, 'Researcher'),
    (PLACE, 'Place'),
    (DATE, 'Date'),
    (GEOCOVER, 'Geographic coverage'),
    (ACTION, 'ACTION'),
    (RATING, 'RATING'),
    (COURSE, 'course code'),
    (COVER_URL, 'Cover URL (shorten url)'),
    (FAMILY, 'family of tags'),
    (COPYRIGHT, 'opensource or commercial?'),
    (REMOTE, 'local or remote?')
  )
  
  name = models.CharField(max_length=128) # e.g. 'Mr. E. Smith'
  slug = models.SlugField(max_length=128) # e.g. 'mr-e-smith'
  type = models.CharField(max_length=2, choices=TYPE_CHOICES + TYPE_OEMBED_CHOICES, default=FREE) # e.g. 'author' or 'institution'

  # tag specification e.g. we want to specify an institution for a given author
  related = models.ManyToManyField('self', symmetrical=False, null=True, blank=True)

  def save(self, **kwargs):
    if self.pk is None:
      self.slug = uuslug(model=Tag, instance=self, value='%s-%s'% (self.type, self.name))
    super(Tag, self).save()


  @staticmethod
  def search(query):
    argument_list =[
      Q(name__icontains=query),
      Q(slug__icontains=query),   # add this only when there are non ascii chars in query. transform query into a sluggish field. @todo: prepare query as a slug
    ]
    return reduce(operator.or_, argument_list)


  def __unicode__(self):
    return "%s : %s"% (self.get_type_display(), self.name)


  class Meta:
    ordering = ["type", "id" ]
    unique_together = ("type", "name")


  def json(self, deep=False):
    return{
      'id': self.id,
      'slug':self.slug,
      'name':self.name,
      'type':self.type,
      'type_label':self.get_type_display()
    }

#
#  WorkingDocument
#   
#  This is a special document for internal purposes: it could be a Scenario pedagogique, a course, a tool, etc...
#  Cfr related type and feel free to add types. Note that no hierarchy is specified!
#  Comments probably via DISQUS. To be DISCUSSED.
# 
#
class WorkingDocument(AbstractDocument):
  SEQUENCE  = 'B'
  TASK      = 'I'
  TOOL      = 'T'
  COPY      = 'C'
  DONTKNOW  = '?'

  TYPE_CHOICES = (
    (SEQUENCE, 'pedagogical sequence'),
    (TASK,     'pedagogical task'),
    (TOOL,     'tool'),
    (COPY,     'carbon copy'),
    (DONTKNOW, 'I really don\'t know yet...'),
  )

  # various course type, from lycee to Phd
  COURSE_SECONDARY_SCHOOL = 'course_secondary_school'
  COURSE_MASTER = 'course_master'
  COURSE_PHD = 'course_phd'
  COURSE = 'course' # generic course

  COURSE_TYPE_CHOICES = (
    (COURSE_SECONDARY_SCHOOL,  'secondary school course'),
    (COURSE_MASTER,            'master course'), # ex tag cursus, it must be enlightened
    (COURSE_PHD,            'phd course'), 
    (COURSE,            'generic course'), 
  )
  
  # various sessions inside a course. feature to be tested.
  SESSION_ATELIER = 'session_atelier'
  SESSION_THEORY  = 'session_theory'
  SESSION_DEBATE  = 'session_debate'
  SESSION_MASTER  = 'session_magistral'

  SESSION_TYPE_CHOICES = (
    (SESSION_ATELIER, 'atelier'),
    (SESSION_DEBATE, 'debate'),
    (SESSION_THEORY, 'theoric course'),
    (SESSION_MASTER, 'cours magistral'),
  )

  TYPE_TREE = (SEQUENCE, TASK, TOOL, COURSE_MASTER)

  # various status. feature to be tested, not used.
  WAITING_FOR_PUBLICATION = 'W' # ask for peer review !
  PUBLIC                  = 'P' # make the document publicly available
  PRIVATE                 = 'M' # read and edit only to owner

  STATUS_CHOICES = (
    (WAITING_FOR_PUBLICATION, 'publish it, please!'),
    (PUBLIC,                  'public'),
    (PRIVATE,                 'private'),
  )
  
  parent  = models.ForeignKey("self", null=True, blank=True, related_name="children") # filiation
  dependencies = models.ManyToManyField("self", symmetrical=False, null=True, blank=True, related_name="dependents") # forkz! woring copies of the same pedagogical documents. A versioning likeLike related for documents
  copies = models.ManyToManyField("self", symmetrical=True, null=True, blank=True) # forkz! woring copies of the same pedagogical documents. A versioning likeLike related for documents
  tags = models.ManyToManyField(Tag, blank=True, null=True) # add tags !

  documents = models.ManyToManyField('Document', null=True, blank=True, through='Device', related_name='supportedby') # internal links with existings documents

  status  = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PRIVATE, blank=True, null=True)
  type = models.CharField(max_length=32, choices=TYPE_CHOICES + COURSE_TYPE_CHOICES + SESSION_TYPE_CHOICES)


  def get_tags(self):
    tags = {};
    for t in self.tags.all():
      t_type = '%s'%t.type
      if t_type not in tags:
        tags[t_type] = []
      tags[t_type].append(t.json())
    return tags


  class Meta:
    ordering = ('-type', '-rating', '-id',)


  def __unicode__(self):
    return "[%s] %s" % (self.get_type_display(), self.slug)


  @staticmethod
  def search(query):
    argument_list =[
      Q(title__icontains=query),
      Q(slug__icontains=query),   # add this only when there are non ascii chars in query. transform query into a sluggish field. @todo: prepare query as a slug
      Q(abstract__icontains=query),
      Q(tags__name__icontains=query)
    ]
    return reduce(operator.or_, argument_list)


  def save(self, **kwargs):
    # handle type-driven validation when parent is given. must we put this logic into the form? Nope because of parent stuff.
    created = self.pk is None
    self.slug = uuslug(model=WorkingDocument, instance=self, value=self.title)
    
    if self.parent:
      if self.parent.type not in WorkingDocument.TYPE_TREE:
        print WorkingDocument.TYPE_TREE
        raise IntegrityError("WoringDocumentparent is not of the type SEQUENCE, TASK or TOOL") #print self.slug, self.type,' child of', self.parent.slug, self.parent.type, '?'
      if self.type == WorkingDocument.SEQUENCE or self.type == WorkingDocument.COURSE:
        raise IntegrityError("WoringDocument of type SEQUENCE or COURSE Can't have parents")
      elif self.type == WorkingDocument.COPY:
        raise IntegrityError("WoringDocument of type COPY Can't have parents! It is just a local copy and herites the type of the clone")
      elif self.type == WorkingDocument.TASK and self.parent.type not in [WorkingDocument.SEQUENCE, WorkingDocument.TASK]:
        raise IntegrityError("WoringDocument of type TASK must be below SEQUENCE or TASK parent type")
      elif self.type == WorkingDocument.TOOL and self.parent.type not in [WorkingDocument.TASK, WorkingDocument.TOOL]:
        raise IntegrityError("WoringDocument of type TOOL must be below TASK or TOOL parent type")

    super(WorkingDocument, self).save()

    if created and self.permalink:
      alias = WorkingDocument.objects.exclude(pk=self.pk).filter(permalink=self.permalink).order_by('id')

      if alias.count() > 0:
        self.type = WorkingDocument.COPY
        alias[0].copies.add(self) # save as a copy automatically
        alias[0].save()
        super(WorkingDocument, self).save()


  def json(self, deep=False):
    d = {
      'id': self.id,
      'slug':self.slug,
      'rating':self.rating,
      'type': self.type,
      'type_label': self.get_type_display(),
      'title': self.title,
      'abstract': self.abstract,
      'permalink': self.permalink,
      'owner': self.owner.username,
      'date': self.date.strftime('%Y-%m-%d') if self.date else None,
      'count': {
        'documents': self.supports.count()
      }
    }

    if self.parent:
      d['parent'] = self.parent.json() # simple. just id and title
    
    if deep:
      d['supports'] = [doc.document.json() for doc in self.supports.all()]
      
      d['children'] = [doc.json() for doc in self.children.all()]
      
      if self.type == WorkingDocument.COPY:
        d.update({
          'copy_of': [{'id':c.id, 'type':c.type} for c in self.copies.all()]
        })
    else:
      d['documents'] = self.documents.count()

    d.update({
      'tags': self.get_tags()
    })
    return d

#
#  Document
#   
#  A normal document class(e.g. for the inquiry).
#  It contains documents and their references
# 
#
class Document(AbstractDocument):
  WAITING_FOR_PUBLICATION = 'W'
  PUBLIC  = 'P' # make the document publicly available
  SHARED   = 'S' # editable only to authors, viewable by watchers
  DRAFT   = 'D'  # working draft, read and edit only to owner, shown as draft in your working platform
  PRIVATE = 'M' # read and edit only to owner


  STATUS_CHOICES = (
    (WAITING_FOR_PUBLICATION, 'publish it, please!'),
    (PUBLIC, 'public'),
    (SHARED, 'shared'), # allow watchers to view it, it remains private and it is not draft
    (DRAFT, 'draft'), # draft is viewable/editable by authors and owner only.
    (PRIVATE,'private'), # will not appears on drafts, but it is not published
  )

  LINK  = 'B' # external link
  MEDIA   = 'I' # external iframe, image, audio or video
  TEXT   = 'T' # a note (at least originally)
  COMMENT  = 'C' # a cpomment,
  REFERENCE_COURSE = 'rO'
  REFERENCE_RESOURCE = 'rD'
  REFERENCE_RIGHTS = 'rR'
  REFERENCE_CONTROVERSY = 'rY'
  REFERENCE_CONTROVERSY_WEB = 'ControversyWeb'
  REFERENCE_CONTROVERSY_VIDEO = 'ControversyVideo'

  TYPE_CHOICES = (
    #( REFERENCE_COURSE, 'ref. course'),
    #( REFERENCE_RESOURCE, 'ref. resource'),
    #( REFERENCE_RIGHTS, 'ref. rights'),
    (REFERENCE_CONTROVERSY, 'ref. global controversy object'),
    (REFERENCE_CONTROVERSY_WEB, 'ref. controversy site'),
    (REFERENCE_CONTROVERSY_VIDEO, 'ref. controversy video'),
    (LINK,  'just a link'),
    (MEDIA, 'media'),
    (TEXT,  'text'), # notes and other stories
    (COMMENT, 'comment')
  )

  PDF = 'application/pdf'
  STORED_VIDEO = 'video/storedvideo'

  MIMETYPES_CHOICES = (
    (PDF, 'pdf'),
    (STORED_VIDEO, 'video - storage')
  )
  
  mimetype = models.CharField(max_length=255, default="", choices=MIMETYPES_CHOICES, blank=True, null=True) # according to type, if needed (like imagefile)
  # URL LOCATION
  local = models.FileField(upload_to='documents/%Y-%m/',  blank=True, null=True) # local stored file inside media folder (aka upload)
  remote = models.TextField(blank=True, null=True) # DEPRECATED local stored file inside storage folder. IT DOES NOT ALLOW UPLOAD! format: either http:/// or 
  # document friendship
  related = models.ManyToManyField("self", symmetrical=True, null=True, blank=True) # forkz!
  parent  = models.ForeignKey("self", null=True, blank=True, related_name="children") # comments
  status  = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT, blank=True, null=True)
  type = models.CharField(max_length=32, choices=TYPE_CHOICES, default=TEXT)
  # tags and metadata. Reference is thre Reference Manager ID field (external resource then)
  tags = models.ManyToManyField(Tag, blank=True, null=True) # add tags !
  reference = models.CharField(max_length=60, default=0, blank=True, null=True, unique=True)

  authors = models.ManyToManyField(User, blank=True, null=True,  related_name="document_authored") # co-authors User.pin_authored
  watchers = models.ManyToManyField(User, blank=True, null=True, related_name="document_watched") # User.pin_watched


  @staticmethod
  def search(query):
    argument_list =[
      Q(title__icontains=query),
      Q(slug__icontains=query),   # add this only when there are non ascii chars in query. transform query into a sluggish field. @todo: prepare query as a slug
      Q(abstract__icontains=query),
      Q(reference__icontains=query),
      Q(tags__name__icontains=query)
    ]
    return reduce(operator.or_, argument_list)


  def save(self, **kwargs):
    self.slug = uuslug(model=Document, instance=self, value=self.title)
    
    if self.pk is None:
      super(Document, self).save()

    if self.permalink:
      print 'permalink', self.permalink
      import micawber
      mic = micawber.bootstrap_basic()

      try:
        oem = mic.request(self.permalink)
      except micawber.exceptions.ProviderNotFoundException, e:
        pass
      else: # store as oembed tags
        t1, created = Tag.objects.get_or_create(type=Tag.OEMBED_PROVIDER_NAME, name=oem['provider_name'])
        t1, created = Tag.objects.get_or_create(type=Tag.OEMBED_TITLE, name=oem['title'])
        t2, created = Tag.objects.get_or_create(type=Tag.OEMBED_THUMBNAIL_URL, name=oem['thumbnail_url'])
        
        self.tags.add(t1)
        self.tags.add(t2)

    super(Document, self).save()


  class Meta:
    unique_together = ("slug",)
    ordering = ('-rating',)


  def __unicode__(self):
    return "[%s] %s" % (self.slug, self.reference)

  
  def bib(self):
    return bibtex(self.content)

  def plaintext(self):
    return """
      |

      %s
      ===

        #%s %s
        language: %s
        mimetype: %s

      ___""" %(self.title, self.id, self.slug, self.language, self.mimetype)

  def get_attachments(self, deep=True):
    attachments = {
      'thumb':{
        'id': '%s-%s' % (self.id, 0),
        'type': 'thumb',
        'ext': 'png',
        'src': reverse('frontcast_storage', args=['%s'%self.reference if self.reference else 'common', 'cover','png'])
      },
      'video':{}, #  video gallery, src index
      'gallery':[], # images and videos
      'pdf':[] #pdf attached (or other downloadable format)
    }
    
    if not deep: # massive get, show thmbs only
      return attachments

    # get every file for the single reference
    path = os.path.join(settings.STORAGE_ROOT_PROTECTED, self.reference)

    if not os.path.isdir(path):
      return attachments

    files = os.listdir(path)

    for i,f in enumerate(files):
      parts = re.split('[/.]', f)

      if len(parts) != 2 or f == 'cover.png': # esclude double extension and file without extension as well. will be client  added
        continue

      ext = parts[-1]
      name = parts[0]
      src = reverse('frontcast_storage', args=[self.reference, name, ext])


      # check extension and collect attachments. Check readme.md file for storage settings.
      if ext in ['mp4', 'ogg']:
        if name not in attachments['video']:
          attachments['video'][name] = {
            'id': '%s-%s' % (self.id, i+1),
            'sources':[],
            'name' : name,
            'poster': reverse('frontcast_storage', args=[self.reference, name, "%s.png" % ext])
          }
        attachments['video'][name]['sources'].append({
          'src': src,
          'ext': ext
        })

      elif ext in ['jpg', 'png']:
        attachments['gallery'].append({
          'id': '%s-%s' % (self.id, i+1),
          'src': src,
          'ext': ext
        })

      elif ext in ['pdf', 'doc']:
        attachments['pdf'].append({
          'id': '%s-%s' % (self.id, i+1),
          'src': src,
          'ext': ext,
          'name': name
        })

    attachments['video'] = attachments['video'].values()
    return attachments


  def get_organized_tags(self):
    tags = {}

    for t in self.tags.all():
      t_type = '%s'%t.get_type_display()
      if t_type not in tags:
        tags[t_type] = []
      tags[t_type].append(t)
    return tags


  def json(self, deep=False):
    # divide tags according to type
    tags = {}

    for t in self.tags.all():
      t_type = '%s'%t.get_type_display()
      if t_type not in tags:
        tags[t_type] = []
      tags[t_type].append(t.json())

    # attach working docs!
    devices = [d for d in self.devices.all()]
    devices_by_type = {}

    for d in devices:
      if str(d.type) not in devices_by_type:
        devices_by_type[str(d.type)] = []
      devices_by_type[str(d.type)].append(d.json())


    # undesratnd remote/ locales file
    attachments = self.get_attachments(deep);

    
    d = {
      'id': self.id,
      'slug':self.slug,
      'rating':self.rating,
      'status': self.get_status_display(),
      'title': self.title,
      'abstract': self.abstract,
      'language': self.language,
      'mimetype': self.mimetype,
      'permalink': self.permalink,
      'reference': self.reference,
      'owner': profiler(self.owner),
      'tags': tags,
      'devices': devices_by_type,
      'type': self.type,
      'attachments':attachments,
      'remote': self.remote,
      'date_last_modified': self.date_last_modified.isoformat() if self.date_last_modified is not None else None,
      'authors': [a.username for a in self.authors.all()]
    }

    return d

  def tojson(self):
    return json.dumps(self.json())



#
#  Profile
#   
#  A simple custom profile class, created on first LDAP access.
#  Cfr observer/ldap.py
# 
class Profile(models.Model):
  user = models.OneToOneField(User)
  accept_cookies = models.BooleanField(default=False)
  language = models.CharField(max_length=2, default='en', choices=settings.LANGUAGES) # favourite user language
  tags = models.ManyToManyField(Tag, null=True, blank=True)
  
  def __unicode__(self):
    return "%s" % self.user.username

  def json(self, deep=False):
    d = {
      'id': self.id,
      'user': {
        'id':self.user.id,
        'username': self.user.username,
      },
      'accept_cookies': self.accept_cookies,
      'language':self.language
    }
    if deep:
      d['tags'] = [ t.json() for t in self.tags.all() ]
    return d

#
#  Property
#   
#  observed property for a specific phase. We will be able to answer the following question:
#  E.g. multiple choices fields are yes / no / None on a property.
#  Cfr observer/ldap.py
# 
class Property(models.Model):
  '''
  All possible Observed properties, flattened. 
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
  EXT_VIDEO_CONTENT     = 'ext_vid_cont'
  SC_LIT          = 'sc_lit'
  SCIENTOMETRICS  = 'scientometri'
  MEDIA_ANALYSIS  = 'media_analys'
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
    (ACTOR_DESC_TABLE,   _('actor_desc_t')),
    (ACTOR_DESC_CLASSIF, _('actor_desc_c')),
    (ACTOR_DESC_FLAT_LIST, _('actor_desc_f')),
  )

  METH_DETAILS_DATASETS   = 'details_data'
  METH_DETAILS_INTERVIEWS = 'details_inte'
  METH_DETAILS_NEWSPAPERS = 'details_news'
  METH_DETAILS_SOCIALNETW = 'details_soci'
  METH_DETAILS_SITEVISIT  = 'details_site'
  METH_DETAILS_SURVEYS    = 'details_surv'

  TYPE_METH_DETAILS_CHOICES = ( # to be used as multiple choices inside the observer.forms.ProfileForm)
    (METH_DETAILS_DATASETS,   _('details_data')),
    (METH_DETAILS_INTERVIEWS, _('details_inte')),
    (METH_DETAILS_NEWSPAPERS, _('details_news')),
    (METH_DETAILS_SOCIALNETW, _('details_soci')),
    (METH_DETAILS_SITEVISIT,  _('details_site')),
    (METH_DETAILS_SURVEYS,    _('details_surv')),
  )
  
  INTERVIEW_VIDEO      = 'interview_vi'
  INTERVIEW_AUDIO      = 'interview_au'
  INTERVIEW_TRANSCRIPT = 'interview_tr'
  INTERVIEW_NOTE       = 'interview_no'

  TYPE_INTERVIEW_CHOICES = (
    (INTERVIEW_VIDEO,      _('interview_vi')),
    (INTERVIEW_AUDIO,      _('interview_au')),
    (INTERVIEW_TRANSCRIPT, _('interview_tr')),
    (INTERVIEW_NOTE,       _('interview_no')),
  )

  TYPE_CHOICES = (
    (ACTOR_TABLE,     _('actor_table')),
    (ARG_TREE,        _('arg_tree')),
    (COSMOGRAPHY,     _('cosmography')),
    (DIAGRAM,         _('diagram')),
    (EXT_VIDEO_CONTENT, _('ext_vid_cont')),
    (SC_LIT,          _('sc_lit')),
    (SCIENTOMETRICS,  _('scientometri')),
    (MEDIA_ANALYSIS,  _('media_analys')),
    (METHODOLOGY,     _('tmethodology')),
    (QUAL_DA,         _('qual_da')),
    (SOURCES_DETAILS, _('sources_deta')),
    (COMMENTS,        _('comments')),
    (ANIMATION,       _('animation')),
    (COMIC,           _('comic')),
    (GLOSSARY,        _('glossary')),
    (VIZ_ANALOGY,     _('viz_analogy')),
    (STATS,           _('stats')),
  )

  type     = models.CharField(max_length=12, choices=TYPE_CHOICES + TYPE_METH_DETAILS_CHOICES + TYPE_INTERVIEW_CHOICES + TYPE_ACTOR_DESC_CHOICES, null=True, blank=True) # e.g. 'author' or 'institution'
  phase    = models.CharField(max_length=12, choices=PHASE_CHOICES, null=True, blank=True) 
  slug     = models.SlugField(max_length=128, unique=True) # a simple way to access integrated stuffs


  def save(self, **kwargs):
    if self.pk is None:
      self.slug = uuslug(model=Property, instance=self, value=self.type)
    super(Property, self).save()


  def json(self, deep=False):
    d = {
      'id': self.id,
      'slug': self.slug,
      'type': self.type
    }
    return d


  def __unicode__(self):
    return "%s" % self.type


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
  GEOLOCATION = 'geolocation'
  WEBTOOL = 'webtool'
  SCIENTOMETRICS = 'scientometri'
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
    (GEOLOCATION, _('Geographical maps')),
    (WEBTOOL, _('Web-site building tools')),
    (SNA, _('Social Network Analysis Tools')),
    (TAGCLOUD, _('Tag clouds')),
    (TEXT_ANALYSIS, _('Textual analysis')),
  )

  TYPE_CHOICES_DICT = dict(TYPE_CHOICES)

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



#
#  DocumentProfile
#   
#  A "simple" FORM to analyse documents: add notes and answer questions.
#  Each question has a specific answer type: yes/no/nope for Property types
#  and Device objects for Device types.
#  It has also the links with the Property table.
#  A document given as foreign key can have a number of properties.
#  Cfr observer/ldap.py
# 
class DocumentProfile(models.Model):
  ANALYSIS      = 'analysis'
  EXPLORATION   = 'exploration'
  METHODOLOGY   = 'methodology'
  PARTICIPATION = 'participatio'
  PRESENTATION  = 'presentation'
  SOURCES       = 'sources'
  STATISTICS    = 'statistics'

  QUESTIONS = ( # ex Property phase choices... keep them before changing their model.
    (SOURCES, (
      (Property.SOURCES_DETAILS, _('question_sources_deta'), _('description_sources_deta')),
      (Property.METH_DETAILS_DATASETS   , _('question_details_data'), _('description_details_data')),
      (Property.METH_DETAILS_INTERVIEWS , _('question_details_inte'), _('description_details_inte')),
      (Property.METH_DETAILS_NEWSPAPERS , _('question_details_news'), _('description_details_news')),
      (Property.METH_DETAILS_SOCIALNETW , _('question_details_soci'), _('description_details_soci')),
      (Property.METH_DETAILS_SITEVISIT  , _('question_details_site'), _('description_details_site')),
      (Property.METH_DETAILS_SURVEYS  , _('question_details_surv'), _('description_details_surv')),
      (Property.INTERVIEW_TRANSCRIPT, _('question_interview_tr'), _('description_interview_tr')),
      (Property.INTERVIEW_VIDEO, _('question_interview_vi'), _('description_interview_vi')),
      (Property.INTERVIEW_AUDIO, _('question_interview_au'), _('description_interview_au')),
      (Property.INTERVIEW_NOTE, _('question_interview_no'), _('description_interview_no')),
    )),  
    (METHODOLOGY, (
      (Property.SC_LIT, _('question_sc_lit'), _('description_sc_lit')),
      (Property.QUAL_DA, _('question_qual_da'), _('description_qual_da')),
      (Device.SNA, _('question_sna'), _('description_sna')),
      (Device.DATABASE, _('question_database'), _('description_database')),
      (Device.CRAWL, _('question_crawl'), _('description_crawl')),
      (Device.SCIENTOMETRICS, _('question_scientometri'), _('description_scientometri')),
      (Device.ANALYSIS_SPECIAL, _('question_analysis_spe'), _('description_analysis_spe')),
      (Device.EXPLORE_SPECIAL, _('question_explore_special'), _('description_explore_special')),
      (Device.TEXT_ANALYSIS, _('question_text_analysis'), _('description_text_analysis')),
      (Property.MEDIA_ANALYSIS, _('question_media_analysis'), _('description_media_analysis')),
      (Property.STATS, _('question_stats'), _('description_stats')),
    )),
    (PRESENTATION, (
      (Property.METHODOLOGY, _('question_tmethodology'), _('description_tmethodology')),
      (Property.ACTOR_DESC_TABLE, _('question_actor_desc_t'), _('description_actor_desc_t')),
      (Property.ACTOR_DESC_CLASSIF, _('question_actor_desc_c'), _('description_actor_desc_c')),
      (Property.ACTOR_DESC_FLAT_LIST, _('question_actor_desc_f'), _('description_actor_desc_f')),
      (Property.ARG_TREE, _('question_arg_tree'), _('description_arg_tree')),
      (Property.ANIMATION, _('question_animation'), _('description_animation')),
      (Property.COMIC, _('question_comic'), _('description_comic')),
      (Device.GEOLOCATION, _('question_geolocation'), _('description_geolocation')),
      (Device.CHRONOLOGY, _('question_chronology'), _('description_chronology')),
      (Property.COSMOGRAPHY, _('question_cosmography'), _('description_cosmography')),
      (Property.DIAGRAM, _('question_diagram'), _('description_diagram')),
      (Device.ACTOR_DIAG, _('question_actor_diag'), _('description_actor_diag')),
      (Property.GLOSSARY, _('question_glossary'), _('description_glossary')),
      (Property.VIZ_ANALOGY, _('question_viz_analogy'), _('description_viz_analogy')),
      (Device.TAGCLOUD, _('question_tagcloud'), _('description_tagcloud')),
      (Property.COMMENTS, _('question_comments'), _('description_comments')),
      (Device.WEBTOOL, _('question_webtool'), _('description_webtool')),
      (Property.EXT_VIDEO_CONTENT, _('question_ext_vid_cont'), _('description_ext_vid_cont')),
      (Device.DISAGREEMENT, _('question_disagreement'), _('description_disagreement')),
    )),
  )

  document = models.ForeignKey(Document, related_name="profile", unique=True)
  owner = models.ForeignKey(User) # who has compiled it

  date = models.DateField(blank=True, null=True) # main date, manually added
  date_created = models.DateTimeField(auto_now_add=True)
  date_last_modified = models.DateTimeField(auto_now=True)

  notes = models.TextField(blank=True) # free evaluation

  properties = models.ManyToManyField(Property, null=True, blank=True, through='DocumentProfile_Properties')
  

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

    properties = [(p.property.type, p.value) for p in DocumentProfile_Properties.objects.filter(documentProfile=self)]
    available_types = [p[0] for p in properties]
    #[(p.property.type, p.value) for p in DocumentProfile_Properties.objects.filter(documentProfile=pro)]
    #properties = []#p.type for p in self.properties.filtersall()]

    #REPETITA IUVANT :D
    # start following questions
    for q in DocumentProfile.QUESTIONS:
      d['questions'].append({
        'section': q[0],
        'label': _(q[0]), 
        'properties': [{
          'name':p[0],
          'label': _(p[0]),
          'question': _('question_%s' % p[0]),
          'description': p[2],
          'value': [v for v in properties if v[0] == p[0]][0][1] if p[0] in available_types else None,
          'is_device': p[0] in Device.TYPE_CHOICES_DICT,
        } for p in q[1]]
      })

    for t in Property.TYPE_CHOICES:
      d['properties'].append({
        'label':_(t[1]),
        'name':t[0], # this should be the unique id.... @todo!
        'value': t[0] in available_types, # does this profile has that type ?
        'question': _('question_%s' % t[0])
      })

    for t in Property.TYPE_INTERVIEW_CHOICES:
      d['properties_interviews'].append({
        'label':t[1],
        'name':t[0],
        'value': t[0] in available_types,
        'question': _('question_%s' % t[0])
      })

    for t in Property.TYPE_METH_DETAILS_CHOICES:
      d['properties_meth_detail'].append({
        'label':t[1],
        'name':t[0],
        'value': t[0] in available_types,
        'question': _('question_%s' % t[0])
      })

    for t in Device.TYPE_CHOICES:
      d['devices'].append({'label':t[1], 'name':t[0]})


    return d


  def __unicode__(self):
    return "%s" % self.document


  class Meta:
    ordering = ["-date_last_modified"]



class DocumentProfile_Properties(models.Model):
  documentProfile = models.ForeignKey(DocumentProfile)
  property = models.ForeignKey(Property)
  value = models.BooleanField(default=True)

  class Meta:
    unique_together = ["documentProfile", "property"]