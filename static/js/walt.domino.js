;(function(window, jQuery, domino, undefined) {
  'use strict';

  window.walt = window.walt || {};
  walt.domino = {};

  // Domino global settings:
  domino.settings({
    shortcutPrefix: '::',
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
            length: 'number' // total_count of items - limit infinite loiading
          },
          value: {
            items: [],
            ids: [],
            limit: 0,
            offset: 0,
            length: 0
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
            length: 'number' // total_count of items - limit infinite loiading
          },
          value: {
            items: [],
            ids: [],
            limit: 0,
            offset: 0,
            length: 0
          },
          dispatch: ['data_assignments__updated']
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
      ],
      shortcuts: [
        {
          id: 'is_locked',
          description: 'Returns true if ui_status allows ui events to be performed',
          method: function() {
            return this.get('ui_status') == walt.UI_STATUS_UNLOCKED;
          }
        }
      ],
      hacks: [
        /*

          data Models Hacks
          =================

          Note that _changed is triggered every time the data model changed

        */
        {
          triggers: 'data__update',
          description: 'it updates data propertties only if needed',
          method: function(e) {
            var user = this.get('user');
            walt.log('(domino) on data__update', e.data);
            
            for(var i in e.data){
              var data_property = e.data[i],
                  data_hash = {},
                  item,
                  references = [];

              /* set permission UI and collect references */
              for(var j in data_property.items){
                item = data_property.items[j];

                if(item.owner && (user.is_staff || item.owner == user.username || item.authors.indexOf(user.username)!= -1 ))
                  data_property.items[j].permissions = walt.PERMISSION_CAN_EDIT;

                item.reference != '' && references.push(item.reference);
              };

              data_hash[i] = data_property;
              this.update(data_hash);
            }

            if( references.length )
              this.dispatchEvent('call_service', {
                service: 'get_references',
                params:{
                  method:'citation_by_rec_ids',
                  params:[ 'forccast', references, 'mla', 'html']
                }
              });
            
            
          }
        },
        /*

          SCENE Hacks
          ===========

        */
        {
          triggers: 'scene__updated',
          description: 'according to the scene to perrform, it loads related data through services',
          method: function(event) {
            var scene = this.get('scene'),
                scene_args = this.get('scene_args'),
                services = [],
                params = {};

            walt.log('(domino) on scene__updated, scene:', scene);
            walt.log('... scene_args:', scene_args);
            
            this.update('ui_status',walt.UI_STATUS_LOCKED);

            if(scene_args.params) {
              for(var i in scene_args.params) {
                if(i == "filters") {
                  try{
                    params[i] = JSON.parse(scene_args.params.filters);
                  } catch(e){
                    walt.error(e);
                  }
                } else {
                  params[i] = scene_args.params[i];
                }
              }
            };

            
            switch(scene){
              case walt.SCENE_SPLASH:
                params = $.extend(true, params, {
                  filters: {
                    type__in: [
                      walt.DOCUMENT_TYPES.REFERENCE_CONTROVERSY_VIDEO,
                      walt.DOCUMENT_TYPES.REFERENCE_CONTROVERSY_WEB,
                      walt.DOCUMENT_TYPES.REFERENCE_CONTROVERSY
                    ]
                  }
                });
                params.filters = JSON.stringify(params.filters);
                
                services = [
                  {
                    service: 'get_documents',
                    params: params
                  },
                  {
                    service: 'get_documents_filters',
                    params:{
                      limit: -1,
                      filters: JSON.stringify({
                        type__in: [walt.DOCUMENT_TYPES.REFERENCE_CONTROVERSY_VIDEO, walt.DOCUMENT_TYPES.REFERENCE_CONTROVERSY_WEB, walt.DOCUMENT_TYPES.REFERENCE_CONTROVERSY]
                      })
                    }
                  }
                ];

                break;
              case walt.SCENE_SEARCH:
                params.filters = JSON.stringify(params.filters);
                services = [
                  {
                    service: 'get_documents',
                    params: params
                  }
                ];

                break;
              case  walt.SCENE_DOCUMENT_VIEW:
                services = [
                  {
                    service: 'get_documents',
                    params:{
                      limit: 1,
                      offset:0,
                      filters: JSON.stringify({
                        slug: scene_args.slug
                      })
                    }
                  }
                ];
                break;
              case  walt.SCENE_DOCUMENT_EDIT:
              case  walt.SCENE_REFERENCE_EDIT:
                services = [
                  {
                    service: 'get_user_document',
                    shortcuts: {
                      username: walt.user.username,
                      slug: scene_args.slug 
                    },
                    params:{
                      limit: 1,
                      offset:0,
                      filters: JSON.stringify({
                        slug: scene_args.slug
                      })
                    }
                  }
                ];
                break;
              case walt.SCENE_REFERENCES:
                services = [
                  {
                    service: 'get_reference_documents',
                    params:{
                      limit: -1,
                      offset:0
                    }
                  }
                ];
                break;
              case walt.SCENE_PUBLIC:
                services = [
                  {
                    service: 'get_documents',
                    limit: -1,
                    offset:0
                  },
                  {
                    service: 'get_assignments',
                    limit: 10,
                    offset:0
                  }
                ];

                break;
              case walt.SCENE_ME:
                services = [
                  {
                    service: 'get_user_documents',
                    shortcuts: {
                      username: walt.user.username
                    },
                    limit: -1
                  },
                  {
                    service: 'get_user_documents_filters',
                    shortcuts: {
                      username: walt.user.username
                    },
                    params:{
                      limit: -1

                    }
                  },
                  {
                    service: 'get_assignments',
                    limit: 10,
                    offset:0
                  }
                ];

                break;
              case walt.SCENE_USER:
                services = [
                  {
                    service: 'get_user_documents',
                    shortcuts: {
                        username: scene_args.username
                      },
                    params:{
                      limit: -1,
                      
                    }
                  }
                ];
                break;
              case walt.SCENE_WORLD_DRAFTS:
                services = [
                  {
                    service: 'get_world_documents',
                    limit: 20,
                    offset:0,
                    filters: '{"status":"D"}'
                  }
                ];
                break;
            }; // end of switch scene

            this.request(services, {
              success: function() {
                walt.domino.controller.update('ui_status', walt.UI_STATUS_UNLOCKED);
                walt.domino.controller.dispatchEvent('scene__synced');
              }
            });

          }
        },
        {
          triggers: 'scene__synced',
          description: 'data loading completed, proceed according to the scene to perrform!',
          method: function(event) {
            walt.log('(domino) on scene__synced, ui status:', this.get('ui_status') )
          }
        },
        {
          triggers: 'scene_args__updated',
          description: 'transform the JSON strings into scene args and fill scene_params object accordingly',
          method: function(event) {
            var scene_args = this.get('scene_args'),
                params = {};

            walt.log('(domino) on scene_args__updated', scene_args);
            
            if(scene_args.params) {
              for(var i in scene_args.params) {
                if(i == "filters") {
                  try{
                    params[i] = JSON.parse(scene_args.params.filters);
                  } catch(e){
                    walt.error(e);
                  }
                } else {
                  params[i] = scene_args.params[i];
                }
              }
            };

            this.update('scene_params', params);
          }
        },
        /*

          content related hacks
          =====================

          fill_*_with__* load and complete related document field
        */
        {
          triggers: 'fill_document_with_oembed',
          description: 'execute the get_<event.data.provider>_oembed service and try to fill all fields given',
          method: function(event) {
            walt.domino.controller.update('ui_status',walt.UI_STATUS_LOCKED);

            this.request('get_'+ event.data.provider +'_oembed',{
              url:event.data.url,
              success: function(data, params) {
                walt.log(':success,','get_vimeo_oembed', data, params);
                params.provider = params.service.match('_([a-z]+)_').pop()
                walt.domino.controller.update('ui_status', walt.UI_STATUS_UNLOCKED);
                walt.domino.controller.dispatchEvent('filled_document_with_oembed',{
                  data:data,
                  params:params
                });
              }
            });
          }
        },
        {
          triggers: 'filled_document_with_oembed'
        },
        /*

          Modules hacks: Signals
          ======================
          
          Event type starts with uppercase letter.
          They usually intercepts modules interactions
          They are DOM events basically!!
        */
        {
          triggers: 'List__completed',
          description: 'list module just stopped moving...'
        },
        /*

          Services hacks
          ==============
          
          Lock and unlock UI fopr every request provided.
          usage: walt.domino.controller.dispatchEvent('call_service',{
            service: get_documents,
            params: {
              limit:2, offset:2
            }
          })
        */
        {
          triggers: 'call_service',
          method: function(event){
            walt.domino.controller.update('ui_status', walt.UI_STATUS_LOCKED);
            walt.log('(domino) call_service', event.data.service);
            
            this.request([{
              service: event.data.service || "untitled",
              shortcuts: event.data.shortcuts || {},
              params: event.data.params || {}
            }],{
              success:  function() {
                walt.domino.controller.update('ui_status', walt.UI_STATUS_UNLOCKED);
              }
            });
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
        { 
          id: 'get_documents',
          type: 'GET',
          url: walt.urls.documents,
          dataType: 'json',
          data: function(input) {
            walt.log('(Service) launch "get_documents"', input);
            return input.params;
          },
          success: function(data) {
            // todo infinite adding not replacing items.
            this.dispatchEvent('data__update', {
              data_documents: {
                items: data.objects,
                ids:$.map(data.objects, function(e){return ''+e.id;}),
                length: +data.meta.total_count,
                limit: +data.meta.limit || data.objects.length,
                offset: data.meta.offset || 0
              }
            });
          }
        },
        { 
          id: 'get_documents_filters',
          type: 'GET',
          url: walt.urls.documents_filters,
          dataType: 'json',
          data: function(input) {
            walt.log('(Service) launch "get_documents_filters"', input);
            return input.params;
          },
          success: function(data, params) {
            this.update('data_documents_filters', data.objects);
          }
        },
        { 
          id: 'get_user_documents',
          type: 'GET',
          url: walt.urls.user_documents,
          dataType: 'json',
          data: function(input) {
            return input.params;
          },
          success: function(data) {
            // todo infinite adding not replacing items.
           this.dispatchEvent('data__update', {
              data_documents: {
                items: data.objects,
                ids:$.map(data.objects, function(e){return ''+e.id;}),
                length: +data.meta.total_count,
                limit: +data.meta.limit || data.objects.length,
                offset: data.meta.offset || 0
              }
            });
          }
        },
        { 
          id: 'get_user_document',
          type: 'GET',
          url: walt.urls.user_document,
          dataType: 'json',
          data: function(input) {
            return input.params;
          },
          success: function(data) {
            var items = {};
            
            this.dispatchEvent('data__update', {
              data_documents: {
                items: [data.object],
                ids: [''+data.object.id],
                length: 1,
                limit: 1,
                offset: 0
              }
            });
          }
        },
        { 
          id: 'get_reference_documents',
          type: 'GET',
          url: walt.urls.user_documents,
          dataType: 'json',
          data: function(input) {
            return input.params;
          },
          success: function(data) {
            // todo infinite adding not replacing items.
           this.dispatchEvent('data__update', {
              data_documents: {
                items: data.objects,
                ids:$.map(data.objects, function(e){return ''+e.id;}),
                length: +data.meta.total_count,
                limit: +data.meta.limit || data.objects.length,
                offset: data.meta.offset || 0
              }
            });
          }
        },
        { 
          id: 'get_world_documents',
          type: 'GET',
          url: walt.urls.world_documents,
          dataType: 'json',
          data: function(input) {
            return input.params;
          },
          success: function(data) {
            // todo infinite adding not replacing items.
            this.dispatchEvent('data__update', {
              data_documents: {
                items: data.objects,
                ids:$.map(data.objects, function(e){return ''+e.id;}),
                length: +data.meta.total_count,
                limit: +data.meta.limit || data.objects.length,
                offset: data.meta.offset || 0
              }
            });
          }
        },
        { 
          id: 'create_document',
          type: 'POST',
          url: walt.urls.user_documents,
          before: function(params, xhr){
            xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);
          },
          dataType: 'json',
          data: function(input) {
            return input.params;
          },
          success: function(data) {
            
          }
        },
        { 
          id: 'modify_document',
          type: 'POST',
          url: walt.urls.user_document,
          before: function(params, xhr){
            xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);
          },
          dataType: 'json',
          data: function(input) {
            return input.params;
          },
          success: function(data, params) {
            // walt.log('(domino)
            walt.toast('modifications saved', {
              cleanup: true
            });

            walt.log('(domino) service:modify_document', data, params);

            this.dispatchEvent('scene_args__update',{
              scene_args: {
                slug: data.object.slug
              }
            });
            this.dispatchEvent('scene__update', {
              scene: walt.SCENE_DOCUMENT_VIEW
            });
          }
        },
        { 
          id: 'get_assignments',
          type: 'GET',
          url: walt.urls.user_assignments,
          dataType: 'json',
          data: function(params) {
            return params;
          },
          success: function(data, params) {
            var ids = [];

            for ( var i in data.objects)
              ids.push(''+data.objects[i].id);
            
            this.update({
              data_assignments: {
                items: data.objects,
                ids:ids,
                length: +data.meta.total_count,
                limit: +data.meta.limit || data.objects.length,
                offset: data.meta.offset || 0
              }
            });
          }
        },
        { 
          id: 'complete_assignments',
          type: 'GET',
          url: walt.urls.user_documents,
          dataType: 'json',
          data: function(params) {
            return params;
          },
          success: function(data, params) {


          }
        },
        { 
          id: 'get_user_documents_filters',
          type: 'GET',
          url: walt.urls.user_documents_filters,
          dataType: 'json',
          data: function(params) {
            return params;
          },
          success: function(data, params) {
            this.update('data_documents_filters', data.objects);
          }
        },
        /*
          
          Non WALTY endpoints
          ===================

          BIBLIB references, vimeo oembed endpoint etc...

        */
        {
          id: 'get_references',
          url: walt.urls.references, 
          type: walt.rpc.type,
          error: walt.rpc.error,
          expect: walt.rpc.expect,
          contentType: walt.rpc.contentType,
          before: function(params, xhr){
            xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);
          },
          async: true,
          data: function( input ) { // input={params:{method:'citation_by_rec_ids', params:[]}}
            walt.log('(Service) launch "get_references"', input);
             return walt.rpc.buildData( input.params.method, input.params.params);
          },
          success: function(data, params) {
            walt.log('(Service) success "get_references"', data);
            if(data.result) {
              var ids = data.result.map(function(i){return i.rec_id}),
                  items = {};

              if(ids.length) {
                for(var i in data.result) {
                  items[data.result[i].rec_id] = data.result[i];
                };

                this.update({
                  data_references: {
                    items: items,
                    ids: ids
                  }
                });
              };
            };
          }
        },
        {
          id: 'get_vimeo_oembed',
          url: 'http://vimeo.com/api/oembed.json',
          data: function(params) {
            var p = {
              url: params.url
            };
            return p;
          },
          success:function(data, params){
            this.log('get_vimeo_oembed', 'get_vimeo_oembed service success function');
          }
        },
        {
          id: 'get_youtube_oembed',
          url: walt.urls.oembed_youtube,
          data: function(params) {
            var p = {
              url: params.url,
              format: 'json'
            };
            return p;
          },
          success:function(data, params){
            this.log('get_youtube_oembed', 'get_youtube_oembed service success function');
          }
        },
        {
          id: 'get_flickr_oembed',
          url: walt.urls.oembed_flickr,
          data: function(params) {
            var p = {
              url: params.url,
              format: 'json'
            };
            return p;
          },
          success:function(data, params){
            this.log('get_flickr_oembed', 'get_flickr_oembed service success function');
          }
        }
      ]
    });

    /*

        instantiate Domino modules
        ---
    */
    walt.domino.controller.addModule( walt.domino.modules.Layout, [walt.domino.controller], {id:'layout'});
    walt.domino.controller.addModule( walt.domino.modules.Menu, null, {id:'menu'});
    walt.domino.controller.addModule( walt.domino.modules.Route, null, {id:'route'});
    walt.domino.controller.addModule( walt.domino.modules.Filters, null, {id:'filters'});
    walt.domino.controller.addModule( walt.domino.modules.Search, null, {id:'search'});

    walt.domino.controller.log('module instantiated');
    //walt.domino.controller.dispatchEvent('init');
    /*

        Start!
        ---
    */
  };

})(window, jQuery, domino);
