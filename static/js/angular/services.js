'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('walt.services', ['ngResource'])
  .factory('CorpusListFactory', function($resource) {
    return $resource('/api/corpus', {}, {
        query: { method: 'GET', isArray: false },
        create: { method: 'POST' }
    });
  })
  .factory('CorpusFactory', function($resource) {
    return $resource('/api/corpus/:id', {}, {
        query: { method: 'GET', params: {id: '@id'}},
        update: { method: 'POST' }
    });
  })
  .factory('DocumentListFactory', function($resource) {
    return $resource('/api/corpus/:id/document', {}, {
        query: { method: 'GET', isArray: false },
        create: { method: 'POST' }
    });
  })
  .factory('WorkingDocumentFactory', function($resource) {
    return $resource('/api/working-document/:id', {}, {
        query: { method: 'GET',  params: {id: '@id'} },
        update: { method: 'POST',  params: {id: '@id'} },
        attach_tags: { method: 'POST',  params: {id: '@id/attach-tags'} }
    });
  })
  .factory('WorkingDocumentTagsFactory', function($resource) {
    return $resource('/api/working-document/:id/attach-tags', {}, {
    });
  })
  .factory('WorkingDocumentListFactory', function($resource) {
    return $resource('/api/working-document', {}, {
        query: { method: 'GET', isArray: false },
        create: { method: 'GET'
        }
    });
  })
  .factory('URLFactory', function($resource) {
    return $resource('/api/url/title', {}, {
        query: { method: 'GET', isArray: false }
    });
  })
  .value('version', '0.1');