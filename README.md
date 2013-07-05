frontcast
=========

Mac & Unix installation

Note: we use '/path/to/' as base folder

Create your frontcast virtualenv:

	$ mkvirtualenv frontcast
	$ cd frontcast
	$ pip install -r requirements.txt

… and create the lacking folders (change permissions according to your system configuration)
	
	$ mkdir logs media locale sqlite
	

We added sqlite folder because we will use a sqlite db. Make sure that apache user has the right to write the .db parent folder.



How to override Handlebars Templates
---

Domino Handlebars templates can be overridden by changing the CustomTemplateUrl path in domino settings

How to override CSS templates
---
custom.css