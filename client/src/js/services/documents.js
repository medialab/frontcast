'use strict';

/**
 * @ngdoc service
 * @name frontcast.documents
 * @description
 * # documents
 * Factory in the frontcast.
 */
angular.module('frontcast')
  .factory('DocumentsFactory', function($resource) {
    return $resource('/api/document', {}, {
        query: { method: 'GET', isArray: false }
    });
  })
  .factory('DocumentFactory', function($resource) {
    return $resource('/api/document/:id', {}, {
        query: { method: 'GET', isArray: false }
    });
  })