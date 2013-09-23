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

      walt.log('listof:',data.length, 'items, selector:',settings.selector );
      
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
            walt.log( settings.prefix + data.ids[i], 'not found, populating');//, settings.template(data.items[i]) );
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

      _self.box.masonry({gutter:12, columnWidth:270});

    }

    

  };


  walt.domino.modules.ListDocuments = function(controller){
    walt.domino.modules.List.call(this, $('#list-of-documents') );
    var _self = this,
        item = {};

    this.create_document = function(item){
      _self.editor = $("#document-editor").remove();
      _self.item = item;

      _self.editor = _self.box.prepend(Handlebars.templates.document_editor(_self.item));
      _self.editor.find('textarea')
        .autosize()
        .first()
        .focus();
    };

    this.save_document = function(){
      var params = {};

      if( _self.item.id ){ // update known item

      } else {

        _self.editor.find('textarea').each(function(i, e){
          var el = $(e);
          params[el.attr('name')] = el.val();
        });

        _self.dispatchEvent('call_service', $.extend( params, {
          service: 'create_document',
          language: 'en',
          type: walt.DOCUMENT_TYPES[_self.item.type.toUpperCase()]
        }));
      }
    };

    this.create_text_document = function(event){
      _self.create_document({
        type:'text'
      });
    };
    
    this.create_media_document = function(event){
      _self.create_document({
        type:'video'
      });
    };
    
    this.evaluate_permalink = function(event){
      if( !_self.editor )
        return;

      var field = $(event.currentTarget),
          url = field.val();

      if( walt.misc.is_vimeo(url) ){
        _self.log('evaluating vimeo url');
        _self.dispatchEvent('fill_document_with_oembed',{
          url: url,
          provider: 'vimeo'
        });
      } else if( walt.misc.is_youtube(url) ){
        _self.log('evaluating youtube url');
        _self.dispatchEvent('fill_document_with_oembed',{
          url: url,
          provider: 'youtube'
        });
      } else if( walt.misc.is_flickr(url) ){
        _self.log('evaluating flickr url');
         _self.dispatchEvent('fill_document_with_oembed',{
          url: url,
          provider: 'flickr'
        });
      } else{
        _self.log('permalink has not been recognized');
      }
    }

    this.get_oembed_tags = function(oembed){
      var store_only_tags = [
            'width',
            'height',
            'license',
            'license_url',
            'provider_name',
            'type',
            "web_page"
          ],
          visible_tags = [
            "author_name",
            "author_url",
            "web_page_short_url"
          ],
          tags = [];

      for( var i in oembed){
        var visibility = 'hidden';

        if( store_only_tags.indexOf(i) != -1)
          visibility = 'store_only';
        else if (visible_tags.indexOf(i) != -1)
          visibility = '';
        tags.push({
          type: 'oembed_' + i,
          visibility: visibility,
          value: oembed[i]
        });
      };

      return tags;
    }

    $(document).on('click', '.actions .add-text', _self.create_text_document );
    $(document).on('click', '.save-document', _self.save_document );
    $(document).on('click', '.actions .add-media', _self.create_media_document );
    $(document).on('change', '.video .permalink textarea', _self.evaluate_permalink );
    
    /*
    
        Triggers
        ========

    */
    this.triggers.events.filled_document_with_oembed = function(controller, event){
      walt.log('filled_document_with_oembed', event.data);
      var result = event.data,
          oembed_tags = _self.get_oembed_tags(result.data),
          html_tags = [];

      _self.editor.find('textarea[name="document-title"]')
        .html(result.data.title)
        .trigger('autosize.resize');

      for( var i in oembed_tags)
        html_tags.push(Handlebars.templates.tag(oembed_tags[i]));
      debugger;
      switch( event.data.params.provider){
        case 'vimeo':
          _self.editor.find('.content')
            .html('<iframe src="//player.vimeo.com/video/'+ result.data.video_id + '" width="100%" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>');
          break;

        case 'flickr':
          _self.editor.find('.content')
            .html('<img src="'+ result.data.url + '" style="width:100%"/>');


          _self.editor.find('.tags')
            .append( 
              html_tags.join(", ")
            );

          break;

        case 'youtube':
          var iframe = $(result.data.html)
            .attr("width","100%")
            .attr("height", "");

          _self.editor.find('.content')
            .append(iframe);
          break;
      }

    }

    this.triggers.events.data_documents__updated = function(controller){
      _self.listof(controller, {
        namespace:'documents'
      });
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
