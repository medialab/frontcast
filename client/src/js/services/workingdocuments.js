'use strict';

/**
 * @ngdoc service
 * @name frontcast.workingdocuments
 * @description
 * # workingdocuments
 * Tools, methods and other pedagogical resources in frontcast
 */
angular.module('frontcast')
  .factory('WorkingDocumentsFactory', function($resource) {
    return $resource('/api/working-document', {}, {
        query: { method: 'GET', isArray: false }
    });
  })
  .factory('WorkingDocumentFactory', function($resource) {
    return $resource('/api/working-document/:id', {}, {
        query: { method: 'GET', isArray: false }
    });
  })
  .factory('WorkingDocumentsFacetsFactory', function($resource) {
    return $resource('/api/document/facets', {}, {
      query: { method: 'GET', isArray: false }
    });
  })