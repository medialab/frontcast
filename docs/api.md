# API Documentation
The present document presents the Frontcast client API, that is, it is supposed to run with a django-session.

## Concept
RESTful API, it returns responses in JSON.

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

##  API and the Data Model: Routes

This api emploies where possible on standard HTTP methods described in RESTful specs: GET, PUT, POST, and DELETE.

`/api/`

Retrieving a list of document:

`GET /api/document/`

Retrieving a single document:

`GET /api/document/<id>` or `GET /api/document/<slug>`
where `<slug>` is the slugified version of the title of the document.

To edit a document, provide the POST params

```
POST /api/document/<id>
title=


```




##  API params
`indent` is always disponible.

### lists only
With lists (`document/`, `tag/`, `workingdocument/` etc..) you can use several GET params
`limit=n`, `offset=n`, `filter={...}`, `order_by=["", ...]`, `search=""`.

E.g in order to retrieve a list of the first 10 documents whose tag id is 525:

	/api/document/?filters={"tags__id":525}&limit=10&offset=0&order_by=["-id"]

