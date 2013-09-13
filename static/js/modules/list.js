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
          item = $( settings.prefix + data.ids[i] );

          if( item.length == 0 ){
            if( previous_item == null )
              _self.box.prepend( settings.template(data.items[i]) );
            else
              $( previous_item ).after( settings.template(data.items[i]) );

            item = $( settings.prefix + data.ids[i] );

            var args = {
              delay: settings.delay
            };
          } else if( previous_item == null ){
            //_self.box.prepend( item );
          } else {
            $( previous_item ).after( item );
          }

          previous_item = settings.prefix + data.ids[i]; // maze.log(i, contents[ ids[i] ].name, ids[i] );
          settings.delay += 70;
      }
    }



  };


  walt.domino.modules.ListDocuments = function(controller){
    walt.domino.modules.List.call(this, $('#list-of-documents') );
    var _self = this;

    this.create_document = function(d){
      _self.editor = $("#document-editor").remove();

      _self.editor = _self.box.prepend(Handlebars.templates.document_editor(d));
      _self.editor.find('textarea')
        .autosize()
        .first()
        .focus();
    };

    this.create_text_document = function(event){
      _self.create_document({
        type:'text'
      });
    }
    
    this.create_video_document = function(event){
      _self.create_document({
        type:'video'
      });
    }
    
    this.create_picture_document = function(event){
      _self.create_document({
        type:'picture'
      });
    }

    this.create_sound_document = function(event){
      _self.create_document({
        type:'sound'
      });
    }

    this.evaluate_permalink = function(event){
      if( !_self.editor )
        return;

      var field = $(event.currentTarget),
          url = field.val();

      if( walt.misc.is_vimeo(url) ){
        _self.dispatchEvent('fill_document_with_oembed',{
          url: url,
          provider: 'vimeo'
        });
      } else if( walt.misc.is_youtube(url) ){
        _self.dispatchEvent('fill_document_with_oembed',{
          url: url,
          provider: 'youtube'
        });
      }

    }

    $(document).on('click', '.actions .add-text', _self.create_text_document );
    $(document).on('click', '.actions .add-video', _self.create_video_document );
    $(document).on('click', '.actions .add-picture', _self.create_picture_document );
    $(document).on('click', '.actions .add-sound', _self.create_sound_document );
    $(document).on('change', '.video .permalink textarea', _self.evaluate_permalink );
    
    /*
    
        Triggers
        ========

    */
    this.triggers.events.filled_document_with_oembed = function(controller, event){
      walt.log('filled_document_with_oembed', event.data);
      var result = event.data;

      _self.editor.find('textarea[name="document-title"]')
        .html(result.data.title)
        .trigger('autosize.resize');

      if( event.data.params.provider == 'vimeo'){
        _self.editor.find('.content')
          .html('<iframe src="//player.vimeo.com/video/'+ result.data.video_id + '" width="100%" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>');
      }
    }

    this.triggers.events.data_documents__updated = function(controller){
      _self.listof(controller, {
        namespace:'documents'
      });
      _self.create_video_document();
    };
  };


  walt.domino.modules.ListReferences = function(controller){
    walt.domino.modules.List.call(this, $('#list-of-references') );
    var _self = this;
  };


  walt.domino.modules.ListAssignments = function(controller){
    walt.domino.modules.List.call(this, $('#list-of-assignments') );
    var _self = this;

    /*
    
        Triggers
        ========
    */
    this.triggers.events.data_assignments__updated = function(controller){
      _self.listof(controller, {
        selector:'.assignment', // css selector for the given item
        prefix: '#as-', // id prefix for the given stuff
        namespace:'assignments',
        template: Handlebars.templates.assignment
      });
    }
  };
})();
