# frontcast



observer/local_settings.py then



configuration details are stored udner 
##installation (Unix)

```
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
Frontcast is a Django 1.7.4 project which uses LDAP authentication (python-ldap and django-aut-ldap) and MYSQL/PostgresSql database (MySQL-python lib by default). Every dependence is available as pip package.

```
Django==1.7.4
MySQL-python==1.2.5
django-auth-ldap==1.2.4
micawber==0.3.1
python-ldap==2.4.19
wsgiref==0.1.2. 
```
