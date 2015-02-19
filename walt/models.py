import re, os, operator, json
from datetime import datetime
from markdown import markdown

from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models, IntegrityError
from django.db.models import Q
from django.utils.text import slugify
from django.utils.timezone import utc

class Task(models.Model):
  DELIVERABLE = 'de'
  FILL_REFERENCE = 'rF'
  FILL_CONTROVERSY_REFERENCE = 'rC'

  TYPE_CHOICES = (
    (DELIVERABLE,'deliverable'),
    (FILL_REFERENCE,'fill reference'),
    (FILL_CONTROVERSY_REFERENCE,'fill controversy reference'),
  )

  name = models.CharField(max_length=128) # e.g. 'Controversy Course 2013 - controversy site due'
  notify_to = models.ForeignKey(User)
  type = models.CharField(max_length=2, choices=TYPE_CHOICES)
  content = models.TextField(default="", blank=True, null=True)

  def __unicode__(self):
    return "%s" % self.name

  def json(self):
    return{
      'id': self.id,
      'name':self.name,
      'type':self.type,
      'type_label':self.get_type_display(),
      'content': self.content
    }
#
#
#  PSEUDO FREE TAGS
#  ================
#
#
class Tag(models.Model):

  # feel free to add tag type to this model ... :D
  FREE = '' # i.e, no special category at all
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


  def save(self, *args, **kwargs):
    if self.pk is None:
      self.slug = uuslug(model=Tag, instance=self, value='%s-%s'% (self.type, self.name))
    super(Tag, self).save(*args, **kwargs)


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
    db_table = 'observer_tag'
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

    

# pedagogical unit
class Unit(models.Model):
  name = models.CharField(max_length=128)
  ldap_id = models.CharField(max_length=80)
  tags = models.ManyToManyField(Tag, null=True, blank=True)

  def __unicode__(self):
    return "%s [%s]" % (self.ldap_id, self.name)




class Profile(models.Model):
  '''
  A simple custom profile class, created on first LDAP access.
  Cfr frontcast/ldap.py
  '''
  user = models.OneToOneField(User)
  accept_cookies = models.BooleanField(default=False)
  language = models.CharField(max_length=2, default='EN', choices=settings.LANGUAGES) # favourite user language
  tags = models.ManyToManyField(Tag, null=True, blank=True)
  units = models.ManyToManyField(Unit, null=True, blank=True)

  class Meta:
    db_table = 'observer_profile'

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



class AbstractDocument(models.Model):
  '''
  base class for both Document and WorkingDocument
  '''
  # the text content
  slug = models.SlugField(max_length=160, unique=True)
  title = models.CharField(max_length=160, default="")
  abstract = models.TextField(default="", blank=True, null=True)
  content = models.TextField(default="", blank=True, null=True)
  language =  models.CharField(max_length=2, default='en', choices=settings.LANGUAGES, blank=True, null=True)
  rating = models.PositiveSmallIntegerField(default=0, blank=True, null=True) # 0 to 10

  # TIME
  date = models.DateField(blank=True, null=True) # main date, manually added
  date_last_modified = models.DateTimeField(auto_now_add=True) #cfr save() method

  # who first created it.
  owner = models.ForeignKey(User) # the original owner
  
  # external permalink.  
  permalink  = models.TextField(default="", blank=True, null=True) # remote link
  permalink_hash  = models.CharField(max_length=32, blank=True, null=True) # remote link

  
  class Meta:
    abstract = True



class WorkingDocument(AbstractDocument):
  '''
  This is a special document for internal purposes: to form a Scenario pedagogique, to collect sequences etc..
  Feel free to change / add type.
  Each object can refer to documents Pedagogical stuff like sequences, tools, tasks etc..
  Note that no hierarchy is specified!
  Comments probably via DISQUS. To be DISCUSSED.
  
  copies are symmetrical relationships between different forks.
  '''
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
  documents = models.ManyToManyField('Document', null=True, blank=True) # internal links with existings documents

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
    db_table = 'observer_workingdocument'
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


  def save(self, *args, **kwargs):
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

    super(WorkingDocument, self).save(*args, **kwargs)

    if created and self.permalink:
      alias = WorkingDocument.objects.exclude(pk=self.pk).filter(permalink=self.permalink).order_by('id')

      if alias.count() > 0:
        self.type = WorkingDocument.COPY
        alias[0].copies.add(self) # save as a copy automatically
        alias[0].save()
        super(WorkingDocument, self).save(*args, **kwargs)


  def json(self, deep=False):
    d = {
      'id': self.id,
      'slug':self.slug,
      'rating':self.rating,
      'type': self.type,
      'type_label': self.get_type_display(),
      'title': self.title,
      'abstract_raw': self.abstract,
      'abstract': markdown(self.abstract),
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



class Document(AbstractDocument):
  '''
  A normal document class(e.g. for the inquiry).
  It contains documents and their references
  '''
  WAITING_FOR_PUBLICATION = 'W'
  PUBLIC 	= 'P' # make the document publicly available
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

  LINK 	= 'B' # external link
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
  reference = models.CharField(max_length=60, default=0, blank=True, null=True)

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


  def save(self, *args, **kwargs):
    self.slug = helper_uuslug(model=Document, instance=self, value=self.title)
    
    if self.pk is None:
      super(Document, self).save(*args, **kwargs)

    if self.permalink:
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
    db_table = 'observer_document'
    
    unique_together = ("slug", "reference")
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

    
    return{
      'id': self.id,
      'slug':self.slug,
      'rating':self.rating,
      'status': self.get_status_display(),
      'title': self.title,
      'abstract': markdown(self.abstract),
      'abstract_raw': self.abstract,
      'content': markdown(self.content),
      'content_raw': self.content,
      'language': self.language,
      'mimetype': self.mimetype,
      'permalink': self.permalink,
      'reference': self.reference,
      'owner': self.owner.username,
      'tags': tags,
      'devices': devices_by_type,
      'type': self.type,
      'attachments':attachments,
      'remote': self.remote,
      'date_last_modified': self.date_last_modified.isoformat() if self.date_last_modified is not None else None,
      'authors': [a.username for a in self.authors.all()]

    }

  def tojson(self):
    return json.dumps(self.json())





class Assignment(models.Model):
  unit = models.ForeignKey(Unit)
  task = models.ForeignKey(Task)
  documents = models.ManyToManyField(Document, blank=True, null=True)
  date_last_modified = models.DateField( auto_now=True) # date last save()
  date_due = models.DateField()
  date_completed = models.DateField( blank=True, null=True) # when assignment is completed
  date_validated = models.DateField( blank=True, null=True) # by staff only
  notes = models.CharField(max_length=160, blank=True, null=True)

  def __unicode__(self):
    s = "%s -- %s %s" % ( self.unit.name, self.task.name, '@completed %s' % self.date_completed if self.date_completed is not None else '@todo')
    return s

  def json(self, deep=False):
    d = {
      'id': self.id,
      'task': self.task.json(),
      'date_last_modified':self.date_last_modified.isoformat(),
      'date_due':self.date_due.isoformat(),
      'date_completed':self.date_completed.isoformat() if self.date_completed is not None else None,
      'notes':self.notes
    }
    return d

  class Meta:
    ordering = ["-date_due", "-task" ]
    unique_together = ("unit", "task")


#
# Return an unique slug identifier for the given instance. Used only when pk is null
# @param text - the text to be slugified 
#
def uuslug(model, instance, value, max_length=128):
  slug = slugify(value)[:max_length] # safe autolimiting
  slug_base = slug
  i = 1;

  while model.objects.exclude(pk=instance.pk).filter(slug=slug).count():
    candidate = '%s-%s' % (slug_base, i)

    if len(candidate) > max_length:
      slug = slug[:max_length-len('-%s' % i)]

    slug = re.sub('\-+','-',candidate)
    i += 1

  return slug



def helper_uuslug(model, instance, value, max_length=128):
  '''
  produce a unique slug for a given text string given a model and an instance.
  If the instance has already a slug, just return the previous value.
  '''
  slug = slugify(value)[:max_length] # safe autolimiting
  slug_base = slug
  i = 1;

  while model.objects.exclude(pk=instance.pk).filter(slug=slug).count():
    candidate = '%s-%s' % (slug_base, i)
    if len(candidate) > max_length:
      slug = slug[:max_length-len('-%s' % i)]
    slug = re.sub('\-+','-',candidate)
    i += 1

  return slug


