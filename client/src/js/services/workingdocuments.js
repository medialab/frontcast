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
    return $resource('/api/document', {}, {
        query: { method: 'GET', isArray: false }
    });
  })
  .factory('WorkingDocumentFactory', function($resource) {
    return $resource('/api/document/:id', {}, {
        query: { method: 'GET', isArray: false }
    });
  })