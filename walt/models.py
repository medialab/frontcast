from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


class Task(models.Model):
	NOTE = 'Sn'
	TYPE_CHOICES = (
		(NOTE, 'note'),
  )

	name = models.CharField(max_length=128) # e.g. 'Controversy Course 2013 - controversy site due'
	type = models.CharField(max_length=2, choices=TYPE_CHOICES)


#
#
#	PSEUDO FREE TAGS
#	================
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

	TYPE_CHOICES = (
		(FREE, 'no category'),
    (AUTHOR, 'AUTHOR'),
    (KEYWORD, 'KEYWORD'),
    (INSTITUTION, 'Institution'),
    (RESEARCHER, 'Researcher'),
    (PLACE, 'Place'),
    (DATE, 'Date'),
    (GEOCOVER, 'Geographic coverage'),
    (ACTION, 'ACTION') # cfr walt.setup to
  )

	name = models.CharField(max_length=128) # e.g. 'Mr. E. Smith'
	slug = models.SlugField(max_length=128) # e.g. 'mr-e-smith'
	type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=FREE) # e.g. 'author' or 'institution'

	def __unicode__(self):
		return "%s : %s"% (self.get_type_display(), self.name)

	class Meta:
		ordering = ["type", "slug" ]
		unique_together = ("type", "slug")

	def json(self ):
		return{
			'id': self.id,
			'slug':self.slug,
			'name':self.name,
			'type':self.type,
			'type_label':self.get_type_display()
		}


class Profile(models.Model ):
	user = models.OneToOneField(User)
	accept_cookies = models.BooleanField(default=False)
	language = models.CharField(max_length=2, default='EN', choices=settings.LANGUAGES) # favourite user language
	tasks = models.ManyToManyField(Task, null=True, blank=True)
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
			d['tasks'] = [ t.json() for t in self.tasks.all() ]
		return d


class Assignment(models.Model):
  profile = models.ForeignKey(Profile)
  task = models.ForeignKey(Task)
  date_last_modified = models.DateField( auto_now=True ) # date last save()
  date_due = models.DateField()
  date_completed = models.DateField( blank=True, null=True )
  notes = models.CharField(max_length=160, blank=True, null=True )

  class Meta:
		ordering = ["-date_due", "-task" ]
		unique_together = ("profile", "task")


class Document( models.Model ):

	PUBLIC 	= 'P' # make the document publicly available
	SHARED 	= 'S' # editable only to authors, viewable by watchers
	DRAFT 	= 'D'  # working draft, read and edit only to owner, shown as draft in your working platform
	PRIVATE = 'M' # read and edit only to owner


	STATUS_CHOICES = (
		( PUBLIC,'published'),
		( SHARED,'shared'),
		( DRAFT,'draft'),
		( PRIVATE,'private'),
	)

	LINK 	= 'B' # external link
	MEDIA 	= 'I' # external iframe, image, audio or video
	TEXT 	= 'T' # a note (at least originally )
	COMMENT  = 'C' # a cpomment,

	TYPE_CHOICES = (
		( LINK,  'just a link'),
		( MEDIA, 'media'),
		( TEXT,  'text'), # notes and other stories
		( COMMENT, 'comment')

	)

	# the text content
	slug = models.SlugField( max_length=160 )
	title = models.CharField( max_length=160, default="", blank=True, null=True )
	abstract = models.TextField( default="", blank=True, null=True )
	content = models.TextField( default="", blank=True, null=True )
	language =  models.CharField( max_length=2, default='EN', choices=settings.LANGUAGES )
	mimetype = models.CharField( max_length=255, default="", blank=True, null=True ) # according to type, if needed (like imagefile)


	# TIME
	date = models.DateField( blank=True, null=True ) # main date, manually added
	date_last_modified = models.DateField( auto_now=True ) # date last save()

	# URL LOCATION
	local = models.FileField( upload_to='documents/%Y-%m/',  blank=True, null=True ) # local stored file inside media folder
	permalink  = models.TextField( default="", blank=True, null=True ) # remote link
	permalink_hash  = models.CharField( max_length=32, blank=True, null=True ) # remote link

	# document friendship
	related = models.ManyToManyField("self", symmetrical=True, null=True, blank=True)
	parent  = models.ForeignKey("self", null=True, blank=True, related_name="children" )
	status  = models.CharField( max_length=1, choices=STATUS_CHOICES, default=DRAFT )
	type = models.CharField( max_length=1, choices=TYPE_CHOICES, default=TEXT )

	# tags and metadata. Reference is thre Reference Manager ID field ( external resource then)
	tags = models.ManyToManyField( Tag, blank=True, null=True ) # add tags !
	reference = models.IntegerField( default=0 )

	owner = models.ForeignKey( User ) # the original owner
	authors = models.ManyToManyField( User, blank=True, null=True,  related_name="document_authored" ) # co-authors User.pin_authored
	watchers = models.ManyToManyField( User, blank=True, null=True, related_name="document_watched"  ) # User.pin_watched

	class Meta:
		unique_together = ( "slug", "language" )
		ordering = ['-date_last_modified']

	def __unicode__(self):
		return "%s (%s) a.k.a. %s" % (self.slug, self.language, self.title)

	# use this function if and only if the pin content is in bibtex (CLEAN) format
	def bib( self ):
		return bibtex( self.content )

	def plaintext( self ):
		return """
			|

			%s
			===

				#%s %s
				language: %s
				mimetype: %s

			___""" %( self.title, self.id, self.slug, self.language, self.mimetype )

	def json( self ):
		return{
			'id': self.id,
			'slug':self.slug,
			'title': self.title,
			'abstract': self.abstract,
			'content': self.content,
			'language': self.language,
			'mimetype': self.mimetype,
			'permalink': self.permalink
		}

