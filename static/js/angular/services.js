'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('walt.services', ['ngResource'])
  .factory('DocumentFactory', function($resource) {
    return $resource('/api/document/:id', {}, {
        query: { method: 'GET',  params: {id: '@id'} },
        update: { method: 'POST',  params: {id: '@id'} },
        attach_tags: { method: 'POST',  params: {id: '@id/attach-tags'} }
    });
  })
  .factory('DocumentListFactory', function($resource) {
    return $resource('/api/document', {}, {
        query: { method: 'GET', isArray: false },
        create: { method: 'POST' }
    });
  })



  .factory('DocumentFiltersFactory', function($resource) {
    return $resource('/api/document/filters', {}, {
        query: { method: 'GET', isArray: false },
    });
  })
  .factory('WorkingDocumentFiltersFactory', function($resource) {
    return $resource('/api/working-document/filters', {}, {
        query: { method: 'GET', isArray: false },
    });
  })


  

  .factory('DeviceFactory', function($resource) {
    return $resource('/observer/api/device/:id', {}, {
      delete: { method: 'DELETE', params: {id: '@id'}}
    });
  })
  .factory('DeviceListFactory', function($resource) {
    return $resource('/observer/api/device', {}, {
        query: { method: 'GET' },
    });
  })
        


  .factory('DocumentProfileFactory', function($resource) {
    return $resource('/observer/api/document-profile/:id', {}, {
        query: { method: 'GET',  params: {id: '@id'} },
        update: { method: 'POST',  params: {id: '@id'} },
        attach_tags: { method: 'POST',  params: {id: '@id/attach-tags'} }
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
      save: { method: 'POST',  params: {id: '@id'} },

    });
  })
  .factory('WorkingDocumentDetachTagFactory', function($resource) {
    return $resource('/api/working-document/:id/detach-tag/:tag_id', {}, {
      delete: { method: 'POST',  params: {id: '@id', tag_id: '@tag_id'} },
    });
  })

  .factory('WorkingDocumentListFactory', function($resource) {
    return $resource('/api/working-document', {}, {
        query: { method: 'GET', isArray: false },
        create: { method: 'GET'
        }
    });
  })

  .factory('TagsFactory', function($resource) {
    return $resource('/api/tag', {}, {
        query: { method: 'GET', isArray: false },
        suggest: { method: 'GET'}
    });
  })

  .factory('URLFactory', function($resource) {
    return $resource('/api/url/title', {}, {
        query: { method: 'GET', isArray: false }
    });
  })
  .value('version', '0.1');