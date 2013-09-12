;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.List = function(box) {
    domino.module.call(this);

    var _self = this;
    this.box = box;



    this.listof = function( controller, options ){
      var previous_item = null,
          item = null,
          settings = $.extend({
            selector:'.document', // css selector for the given item
            prefix: '#d-', // id prefix for the given stuff
            namespace: 'documents',
            template: Handlebars.templates.document,
            delay: 0,
            complete: function(){
              //_self.log(' listof: completed, calling event "scrolling_' + settings.namespace +'"' );
              //_self.toggle_shadow();
              //_self.dispatchEvent( 'scrolling_' + settings.namespace );
            }
          }, options ),
          _omissis = {},
          data = controller.get('data_' + settings.namespace );

      _self.log('listof:',data.length, settings.selector );
      //_self.unsticky();

      /*
        uhm..
        ids variable contains every 'must-in' item.
        So, (1) let's remove what should be removed, (2) let's add what have to be added
        according to ids sorting order.
      */
      $( settings.selector, _self.box ).each(function() {
        var item = $(this);
        if( data.ids.indexOf( item.attr('data-int-id') ) == -1 ){
          item.remove();
          /*maze.move.swipeout( item,{
            delay:settings.delay,
            callback:function(){
              item.remove();
              //_self.dispatchEvent('scrolling_voc');
            }
          });
          */
          settings.delay += 70;
        }
      });


      for( var i in data.ids ){
          item = $( settings.prefix + ids[i] );

          if( item.length == 0 ){
            if( previous_item == null )
              _self.box.prepend( settings.template(data.items[i]) );
            else
              $( previous_item ).after( settings.template(data.items[i]) );

            item = $( settings.prefix + ids[i] );

            var args = {
              delay: settings.delay
            };
          } else if( previous_item == null ){
            //_self.box.prepend( item );
          } else {
            $( previous_item ).after( item );
          }

          previous_item = settings.prefix + ids[i]; // maze.log(i, contents[ ids[i] ].name, ids[i] );
          settings.delay += 70;
      }
    }

  };


  walt.domino.modules.ListDocuments = function(controller){
    walt.domino.modules.List.call(this, $('#list-of-documents') );
    var _self = this;

    this.trigger.event.data_documents__updated = function(controller){
      _self.listof(controller, {
        namespace:'documents'
      });
    }
  };


  walt.domino.modules.ListReferences = function(controller){
    walt.domino.modules.List.call(this, $('#list-of-references') );
    var _self = this;
  };


  walt.domino.modules.ListAssignments = function(controller){
    walt.domino.modules.List.call(this, $('#list-of-references') );
    var _self = this;
  };
})();
