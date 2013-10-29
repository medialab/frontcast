frontcast
=========

Fedora
create and activate virtualenv, install dependecies
	

copy and modify local_settings according to your own django settings. Cfr. settings.py 
	
	mv frontcast/local_settings.sample.py frontcast/local_settings.py 




Mac & Unix installation

Note: we use '/path/to/' as base folder

Create your frontcast virtualenv:

	$ mkvirtualenv frontcast
	$ cd path/to/frontcast
	$ pip install -r requirements.txt

… and create the lacking folders (change permissions according to your system configuration)
	
	$ mkdir logs media locale sqlite
	

We added sqlite folder because we will use a sqlite db. Make sure that apache user has the right to write the .db parent folder.


Import Controverses with their references from a csv file
---
Let's assume you have a csv file named `frontcast-integral-2013.csv` containing the datas of a list of authors and a reference to a document (existing or not); let's also assume that this document is a *well structured* CSV file like this below, where the *document_reference* assures the uniqueness of the document across the rows while the other rows referring to the same document_reference value are the different authors involved:

	first_name,last_name,affiliation,affilition_acronym,user_ldap,course_name,course_code,document_title,document_reference,task,user_tag_role,document_tag_year
	Rossi,Piercarlo,Sciences Po,scpo,,cartographie de la controverse,XXXXXXXX,Les bonnes addresses ,rec_id_XXX,video,auteur,2013
	Verdi,Giancarlo Michele,MIT,mit,,cartographie de la controverse,XXXXXXXX,Les bonnes addresses ,rec_id_XXX,video,auteur,2013
	
	
We created a management command import_references to facilitate this task
	$ cd /path/to/frontcast
	$ workon frontcast
 	$ python manage.py import_references --csv=frontcast-integral-2013.csv --owner=daniele.guido
 	
 


How to compile handlebars templates
---
Frontcast makes use of handlebars templates.
So, firstly install all handlebars requirement for _precompilation. Cfr http://handlebarsjs.com/precompilation.html

	$ cd frontcast
	$ handlebars static/js/templates/* -f static/js/walt.handlebars.js


How to override Domino Handlebars Templates
---

Domino Handlebars templates can be overridden by changing the CustomTemplateUrl path in domino settings

How to override CSS templates
---
custom.css

Remote storage
---

Use the `settings.STORAGE_ROOT` and `settings.STORAGE_ROOT_PROTECTED` to set root path of files that are not available from outside.
This allows you to check for django user permission to access protected files.