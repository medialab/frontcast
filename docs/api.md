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

Entrypoint

`/api/`

Retrieving document

`/api/document/`


##  API params
When applicable.
