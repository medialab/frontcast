# frontcast

Frontcast is the django application dedicated to the controversy mapping archive. Frontcast exposes an internal rest API that works like any html python view and uses LDAP as authentication protocoll.

observer/local_settings.py then set your *default* database, a secret key and ldap configs.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '***********',
        'USER': '***********',
        'PASSWORD': '***********',
        'HOST': '***********'
    }
}
```





##installation (Unix)
Clone or fork the project, then under the hood of a virtualenv, proceed to install requirements with pip installer.
```
mkvirtualenv observer
pip install -r requirements.txt
```

## configure and launch test
```
python manage.py migrate
python manage.py test

```

##data model
There are *two* basic document types: `Document`, assembling Controversy Mapping website and Controversy Mappping delivrables; and `WorkingDocument`, assembling tools and Controversy Mappping courses. Each `Document` or `WorkingDocument` can be distiguish by subtypes.
`DocumentProfile` is where we describe each `Document` and can be connected to some `Property`. Its representation on the rest API takes the form of a survey of Q&A.

```
	DocumentProfile -------- Property
		1
		|
		|
		1	
	Document ---------------.
		|					|
		|					|
		+ Device			+ Tag
		|					|
		|					|
	WorkingDocument --------'
	
```

## accessing SFTP resources
Frontcast has a direct link with a storage space. Cfr the api to understand how Frontcast access storage resource.

## dependencies
Frontcast is a Django 1.7.4 project for python 2.7 which uses LDAP authentication (python-ldap and django-aut-ldap). Every dependence is available as pip package.

```
Django==1.7.4
django-auth-ldap==1.2.4
micawber==0.3.1
python-ldap==2.4.19
wsgiref==0.1.2. 
```

feel free to install specific pip packages for db support.

```
MySQL-python==1.2.5
```

