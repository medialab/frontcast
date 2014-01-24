;(function(window, jQuery, domino, undefined) {
  'use strict';

  window.walt = window.walt || {};

  walt.domino = walt.domino || {};

  // Domino global settings:
  domino.settings({
    shortcutPrefix: '%3A%3A',
    displayTime: true,
    verbose:false,
    strict: true,
    clone: false
  });

  if (!domino.struct.isValid('walt.scene'))
    domino.struct.add({
      id: 'walt.scene',
      struct: function(v) {
        return !!~walt.SCENES.indexOf(v);
      }
    });

  if (!domino.struct.isValid('walt.ui_status'))
    domino.struct.add({
      id: 'walt.ui_status',
      struct: function(v) {
        return !!~walt.UI_STATUSES.indexOf(v);
      }
    });

  walt.domino.init = function(){
      walt.log('DOMINO instantiated');
    walt.domino.controller = new domino({
      name: 'walt',
      properties: [
        /*

          user Models
          ===========

        */
        {
          id: 'user',
          description: 'the frontcast user',
          type: {
            username: 'string',
            is_staff: 'boolean'
          },
          value: {
            username: walt.user.username, // default, cfr. middel.html template
            is_staff: walt.user.is_staff
          },
          triggers: 'user__update',
          dispatch: ['user__updated']
        },
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
            order_by: ['string'],
            length: 'number' // total_count of items - limit infinite loiading
          },
          value: {
            items: [],
            ids: [],
            limit: 0,
            offset: 0,
            length: 0,
            order_by: ['-rating'],
          },
          dispatch: ['data_documents__updated']
        },
        {
          id: 'data_references',
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

          Note: the layout actually change only when scene is updated.
          It involves routing mechanism, cfr Route module.
          Any other changement make only local changements.

        */
        {
          id: 'scene',
          description: 'basic app view',
          type: 'walt.scene',
          value: walt.SCENE_SPLASH,
          triggers: 'scene__update',
          dispatch: ['scene__updated']
        },
        {
          id: 'scene_args',
          description: 'basic app view arguments as given by route mechanism',
          type: 'object',
          value: {},
          triggers: 'scene_args__update',
          dispatch: ['scene_args__updated']
        },
        {
          id: 'scene_params',
          description: 'scene_args having filters are thus transformed into an editable dictionary',
          type: 'object',
          value: {},
          triggers: 'scene_params__update',
          dispatch: ['scene_params__updated']
        },
        /*

          Filtering mechanism
          ===================

          Data filters in place.

        */
        {
          id: 'data_documents_filters',
          description: 'the django-compatible documents filter object',
          type: 'object',
          value: {},
          triggers: 'data_documents_filters__update',
          dispatch: ['data_documents_filters__updated']
        },
        /*

          Creation/Editing mechanism
          ==========================


        */
        /*

          Ui status
          =========
        
          This proerty implements a status mechanism to prevent data overload

        */
        {
          id: 'ui_status',
          description: 'true or false lock mechanism to preserve data loading from overload',
          type: 'walt.ui_status',
          value: walt.UI_STATUS_UNLOCKED,
          triggers: 'lock__update',
          dispatch: ['lock__updated']
        },
        {
          id: 'ui',
          description: 'contains all necessary dimensions of the window object. Resize listener is stored in the layout module',
          type: {
            height: 'number',
            width: 'number'
          },
          value: {
            height: 0,
            width: 0
          },
          triggers: 'ui__update',
          dispatch: ['ui__updated']
        }
      ],
      shortcuts: [],
      hacks: walt.domino.hacks,

      
      services: walt.domino.services
    });

    /*

        instantiate Domino modules
        ---
    */
    walt.domino.controller.addModule( walt.domino.modules.Layout, [walt.domino.controller], {id:'layout'});
    walt.domino.controller.addModule( walt.domino.modules.Grid, null, {id:'menu'});
    walt.domino.controller.addModule( walt.domino.modules.Route, null, {id:'route'});
    //walt.domino.controller.addModule( walt.domino.modules.Filters, null, {id:'filters'});
    walt.domino.controller.addModule( walt.domino.modules.Search, null, {id:'search'});
    walt.domino.controller.addModule( walt.domino.modules.Form, null, {id:'form'});

    walt.log('module instantiated, launch init event ...');
    
    /*

        Start!
        ---
    */

    walt.domino.controller.dispatchEvent('init');
  };

})(window, jQuery, domino);
