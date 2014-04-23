frontcast
=========


### Mac & Unix installation

Git-clone the project, create and activate a virtualenv, install dependecies



Note: we use '/path/to/frontcast' as base folder

#### 1. Create your frontcast virtualenv:

		$ mkvirtualenv frontcast
		$ cd path/to/frontcast
		$ pip install -r requirements.txt

#### 2. create the lacking folders
change permissions according to your system configuration.
	
		$ mkdir logs media locale sqlite
	
#### 3. copy and modify local_settings according to your own django settings. Cfr. settings.py
  
  		$ mv frontcast/local_settings.sample.py frontcast/local_settings.py 

We added sqlite folder because we will use a sqlite db. Make sure that apache user has the right to write the .db parent folder.
