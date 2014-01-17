;(function(window, jQuery, domino, undefined) {
  'use strict';

  window.walt = window.walt || {};
  walt.domino = walt.domino || {};

  
  walt.domino.hacks = [
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

        walt.log('@data__update', e.data);
        
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

          // original
          data_hash[i] = data_property;
          this.update(data_hash);
        }

        walt.log('@data__update biblib references:', references.length);

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

      Scne Models Hacks
      =================

      Note that _changed is triggered every time the data model changed.

      E.g to test search:

      walt.domino.controller.dispatchEvent('scene_args__update',{scene_args:{params:{search:'histo'}}})
      walt.domino.controller.dispatchEvent('scene__update',{scenes:walt.SCENE_SEARCH})
    */
    {
          triggers: 'scene__updated',
          description: 'according to the scene to perrform, it loads related data through services',
          method: function(event) {
            var scene = this.get('scene'),
                scene_args = this.get('scene_args'),
                services = [],
                params = {};

            walt.log('@scene__updated', 'scene:', scene);
            walt.log('... scene_args:', scene_args);
            
            
            this.update('ui_status', walt.UI_STATUS_LOCKED);
            // ADD COMMENTS HERE
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
              case walt.SCENE_INDEX:
              case walt.SCENE_SEARCH:
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
                    }
                  }
                ];
                break;

              case walt.SCENE_DOCUMENT_VIEW:
              case walt.SCENE_DOCUMENT_EDIT:
                services = [
                  {
                    service: 'get_document',
                    shortcuts: {
                      slug: scene_args.slug 
                    },
                    params: {}
                  }
                ];
                break;
              default:
                walt.error('@scene__updated, remember that you must add the (probably) new scene choice inside the hacks.js!! unrecognized scene name:', scene)
                break;
            }; // end of switch scene
            walt.log('@scene__updated, services ', services, scene == walt.SCENE_INDEX);
                
            this.request(services, {
              success: function() {
                walt.domino.controller.update('ui_status', walt.UI_STATUS_UNLOCKED);
                walt.domino.controller.dispatchEvent('scene__synced');
              }
            });

          }
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
  ]

})(window, jQuery, domino);