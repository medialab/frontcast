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
	$ cd frontcast
	$ pip install -r requirements.txt

… and create the lacking folders (change permissions according to your system configuration)
	
	$ mkdir logs media locale sqlite
	

We added sqlite folder because we will use a sqlite db. Make sure that apache user has the right to write the .db parent folder.

How to compile handlebars templates
---
Frontcast makes use of handlebars templates.
So, firstly install all handlebars requirement for _precompilation. Cfr http://handlebarsjs.com/precompilation.html

	$ cd frontcast
	$ handlebars static/js/templates/* -f static/js/handlebars.templates.js


How to override Domino Handlebars Templates
---

Domino Handlebars templates can be overridden by changing the CustomTemplateUrl path in domino settings

How to override CSS templates
---
custom.css