# API Documentation
The present document presents the Frontcast client API, that is, it is supposed to run with a django-session as pure RESTful JSON view. for more info about RESTful, cfr. http://jsonapi.org/. 

## concept
Since we're using JSON views, you're free to customize reqest and answer as you would do with HTML views. Anyway, there are some *helper methods* enabling you to use DJANGO Model. If the Django model contains a json() method returning a python dict, this method will be called to return the requested instance. Otherwise, a basic JSON serializer will do the job.

##  API responses
Basic Json response contains at least two properties: response `status`, basically `ok` or `error`, and `meta`, that gives you a feedback about the current user - if any; the language chosen; the function that served the response; the HTTP method.

```json
{
    "status": "ok", 
    "meta": {
        "action": "observer.api.index", 
        "user": {
            "username": "daniele.guido", 
            "first_name": "Daniele", 
            "is_staff": true
        }, 
        "language": "en-US", 
        "method": "GET"
    }
}
```

Once you set `settings.DEBUG = True` in your settings.js file, every response displays the given POST request params:

```json
{
   "status": "ok",
	"request": {
        "indent": "", 
        "type": "ControversyWeb", 
        "method": "POST", 
        "language": "en", 
        "title": "test"
    }, 
    ...
}
```

##  API and the Data Model: Routes

This api emploies where possible on standard HTTP methods described in RESTful specs: GET, PUT, POST, and DELETE.

`/api/`

### model observer.Document
Retrieving a list of document:

`GET /api/document/`

Retrieving a single document:

`GET /api/document/<id>` or `GET /api/document/<slug>`
where `<slug>` is the slugified version of the title of the document.

To edit a document, provide only the POST params you need to update

```
POST /api/document/<id>
title=New title
```

E.g., in order to create a blank new document:

```
POST /api/document/
type=ControversyWeb
title=test
language=en
```

Since instance creation involves Django Forms like a classic HTML view, failing request will specify lacking or error fields inside the `error` property:

```
POST /api/document/
title=test
language=en
```

will fail with

```json
{
   "status": "error",
	"error": {
        "type": [
            "This field is required."
        ]
    }
}
```

Otherwise, the server respond with a status:ok response (HTTP 200) showing the brand new object:

```json
{
   "status": "ok",
	"object": {
        "status": "draft", 
        "rating": null, 
        "permalink": "", 
        "remote": "", 
        "reference": "iso", 
        "language": "en", 
        "title": "test", 
        "abstract": "", 
        ...
    }
}
```




##  API params
`indent` is always disponible.

### lists only
With lists (`document/`, `tag/`, `workingdocument/` etc..) you can use several GET params
`limit=n`, `offset=n`, `filter={...}`, `order_by=["", ...]`, `search=""`.

E.g in order to retrieve a list of the first 10 documents whose tag id is 525, ordered by last inserted first:

	GET	/api/document/?filters={"tags__id":525}&limit=10&order_by=["-id"]

Or, to get the list of tag of type Institution, labelled `In`:

	GET /api/tag/?filters={"type":"In"}`

### links with manual m2m tables
Multiple updates at once is not yet supported since we employ m2m table ModelForm
E.g. in order to link the document id=1 with the working document id=3
	
	POST /api/device/
	
	document=1
	type=chronology
	working_document=3

Duplicates links are handeld as Django Form errors

``` json
{
    "status": "error", 
    "code": "FormErrors", 
    "error": {
        "__all__": [
            "Device with this Working document, Document and Type already exists."
        ]
    }
}
```

Of course, this relationships can be modified directly as a "normal" object:

	POST /api/device/271
	type=database

will change the relationship field labelled "type"

### links with automatic m2m tables (@todo)

	PUT /api/document/1/links/tag/3


## API basics: extensions and helpers
Frontcast API is a collection of JSON views handled by the special class glue.Epoxy. The `.json()` method of the class returns the proper `HTTPResponse` object.

A basic api view is something like:

```python
#
# observer/api.py
#
def index(req):
  return Epoxy(req).json()
```

and it should have a valid url path in `urls.py`
	
	```python
	apipatterns = patterns('observer.api',
   		url(r'^$', 'index'),
   		# ...
	```

Obvioulsy, you can create custom decorators, like `@staff_member_required_for_POST` that requires staff authorization for POST or DELETE requests while enables public access on GET:

```python
@staff_member_required_for_POST
def index(req):
  return Epoxy(req).json()
```
