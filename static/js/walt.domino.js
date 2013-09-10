;(function(window, jQuery, domino, undefined) {
  'use strict';

  window.walt = window.walt || {};
  walt.domino ={};

  // Domino global settings:
  domino.settings({
    shortcutPrefix: '::',
    displayTime: true,
    verbose: true,
    strict: true,
    clone: false
  });

  walt.domino.init = function(){
    walt.domino.controller = new domino({
      name: 'maze',
      properties: [
        /*

          data Models
          ===========

        */
        {
          id: 'data_documents',
          type: {
            items: ['object'],
            ids: ['string'],
            limit: 'number',
            offset: 'number',
            length: 'number', // total_count of items - limit infinite loiading
          },
          value: {
            items: [],
            ids: [],
            limit: 0,
            offset: 0,
            length: 0,
          },
          dispatch: ['data_documents__updated']
        },
        {
          id: 'data_assignments',
          type: {
            items: ['object'],
            ids: ['string'],
            limit: 'number',
            offset: 'number',
            length: 'number', // total_count of items - limit infinite loiading
          },
          value: {
            items: [],
            ids: [],
            limit: 0,
            offset: 0,
            length: 0,
          },
          dispatch: ['data_assignments__updated']
        },
        {
          id: 'data_reference',
          type: {
            items: 'object',
            ids: ['string']
          },
          value: {
            items: {},
            ids: []
          },
          dispatch: ['data_references__updated']
        },
        /*

          Routing mechanism
          =================

          Note: the layout actually change only when scene action is updated.
          Any other changement make only local changements.

        */
      ],
      shortcuts: [],
      hacks: [
        /*

          data Models Hacks
          =================

          Note that _changed is triggered every time the data model changed

        */
        {
          triggers: 'data_document__changed',
          description: 'documents items collection changed',
          method: function() {

          }
        },
        /*

          Modules Hacks
          =============

          Note Module name must be specified as prefix mod_

        */
        {
          triggers: 'mod_location_changed',
          description: 'location changed',
          method: function() {

          }
        }
      ],

      /*

        Services
        ========

        How to test services:
        var d = domino.instances('maze');
        d.request('service_name',{offset:10, limit:20, query:'query search'})

        service types: get, create, modify, remove

      */
      services: [
        { id: 'get_documents',
          type: 'GET',
          url: walt.urls.user_documents,
          dataType: 'json',
          data: function(params) {
            return params;
          },
          success: function(data, params) {

            this.update({
              data_documents: {
                items: data.objects,
                ids:[],
                length: +data.meta.total_count,
                limit: +data.meta.limit || data.objects.length,
                offset: data.meta.offset || 0
              }
            });
          }
        },
        { id: 'create_document',
          type: 'POST',
          url: walt.urls.user_documents,
          before: function(params, xhr){
            xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);
          },
          dataType: 'json',
          data: function(params) {
            return params;
          },
          success: function(data, params) {

          }
        },
        { id: 'modify_document',
          type: 'POST',
          url: walt.urls.user_document,
          before: function(params, xhr){
            xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);
          },
          dataType: 'json',
          data: function(params) {
            return params;
          },
          success: function(data, params) {

          }
        }
      ]
    });

    /*

        instantiate Domino modules
        ---
    */
    // maze.domino.controller.addModule( maze.domino.modules.__Notebook,null, {id:'notebook'});

    /*

        Start!
        ---
    */
  };

})(window, jQuery, domino);
