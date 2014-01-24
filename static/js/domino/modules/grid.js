/*
  Document Grid Module
  It handles item activation on scene__updated.
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Grid = function() {
    domino.module.call(this);

    var _self = this,
        container = $("#grid-of-documents").nested({ // grid document viewer (nested plugin)
          minWidth: 190,
          gutter: 12,
          animate: false
        }),
        viewer = $("#single-document"),
        counter = $("#counter-documents"),
        actions = $("#actions"), //the jquery element for the counter
        downloads = $("#downloads"), //the jquery element for the counter
        countup; // the countup counter

    this.triggers.events.scene__synced = function(controller) {
      var scene = controller.get('scene');
      walt.verbose('(Grid) listens to scene__updated');
    };

    this.triggers.events.init = function(controller) {
      walt.verbose('(Grid) listens to init');
      
      
      
    };


    /*
      #Data stuff for the Grid Module
      It handles item activation on scene__updated.
    */
    this.triggers.events.data_documents__updated = function(controller) {
      var scene = controller.get('scene');

      walt.verbose('(Grid) listens to data_documents__updated', scene);
      
      // do the cleaning up
      viewer.empty();
      container.empty();
      actions.empty();
      downloads.empty();

      switch(scene){
        case walt.SCENE_INDEX:
        case walt.SCENE_SEARCH:
        case walt.SCENE_ME:
          _self.listof(controller, {namespace: 'documents'});
          break;
        case walt.SCENE_DOCUMENT_VIEW:
          _self.single(controller, {namespace: 'documents'});
          break;
        case walt.SCENE_DOCUMENT_EDIT:
          _self.edit(controller, {namespace: 'documents'});
          break;
        case walt.SCENE_DOCUMENT_ADD:
          _self.create(controller, {namespace: 'documents'});
          break;
      }
     
    };


    /*
      Print out the reference for the given document
    */
    this.triggers.events.data_references__updated = function(controller) {
      var references = controller.get('data_references'),
          single_reference_item = viewer.find('[data-reference-id]'),
          doc,
          ref,
          keywords = [];//pure js object of BIBLIB reference

      walt.verbose('(Grid) listens to data_references__updated');

      
      // single document references
      if(single_reference_item.length){
        ref = references.items[single_reference_item.attr('data-reference-id')];

        try {
          keywords = ref.keywords? ref.keywords.filter(function(a){return a.language=='en'}).pop().values: [];
        } catch(e) {
          walt.error(e, '(Grid) listens to data_references__updated (reference keyword have to be in english');
        }
        
        if(keywords.length)
          doc = single_reference_item.closest('.big-box').find('.keywords').html('#' + keywords.join(', #'));

        single_reference_item.html(ref.citations.html.mla);
        walt.verbose('... keywords', keywords);
      }

      // single document keywords


      /* grid documents references - not planned
      container.find('[data-reference-id]').each(function(i, e) {
        var el = $(this),
            reference_id = el.attr('data-reference-id');

        if( references.ids.indexOf(reference_id) != -1){
          el.html(references.items[reference_id].mla);
        }
      });
      */
    };


    this.single = function(controller) {  
      var doc = controller.get('data_documents').items[0],
          previouscount = countup? countup.endVal: 0;

      walt.verbose('(Grid) .single', doc);
      container.empty().height('auto');
      viewer.empty().append( Handlebars.templates.document_view(doc));
      viewer.find('.swiper-container').swiper({
        //Your options here:
        mode:'horizontal',
        loop: false,
        mousewheelControl: false,// boolean false true   Set to true to enable navigation through slides using mouse wheel.
        pagination: '.pagination',
        paginationClickable: 'true',
        createPagination: true
        //etc..
      });

      viewer.find("video").each(function() {
        var item = $(this),
            videoid = item.attr('id');

        if(videojs.players[videoid])
          delete videojs.players[videoid]
        walt.verbose('(Grid) .single video found:', videoid, videojs.players);
        videojs(videoid, {}, function(){
          walt.verbose('(Grid) .single video started');
          // Player (this) is initialized and ready.
        });
      });

      countup = new countUp("counter-documents", previouscount, 1, 0, 1.500);
      countup.start();


      // check if it has the right to edit, then add edit buttons
      _self.enable_edit(doc);
      _self.enable_buttons(doc);
    }

    this.enable_edit = function(doc){
      actions.empty().append($('<a/>',{'class':'boo', href:'/d/' + doc.slug + '/edit'}).html('edit <i class="fa fa-pencil"></i>'))
    }

    this.enable_buttons = function(doc){
      doc.permalink &&
        actions.append(Handlebars.templates.permalink({href:doc.permalink}));

      doc.attachments.pdf.length &&
        downloads.append(Handlebars.templates.download(doc.attachments.pdf));
        
     
    }
    
    this.enable_save = function(doc){
      actions.empty().append($('<a/>',{'class':'boo blue', href:'/#/d/' + doc.slug }).html('save <i class="fa fa-save"></i>'))
    }

    this.edit = function(controller) {  
      var doc = controller.get('data_documents').items[0];

      walt.verbose('(Grid) .edit', doc);
      container.empty().height('auto');
      viewer.empty().append( Handlebars.templates.document_edit(doc));
      _self.enable_save(doc);
    }

    this.create = function(controller) {  
      walt.verbose('(Grid) .create');
      container.empty().height('auto');
      viewer.empty().append( Handlebars.templates.document_add({}));
      //_self.enable_save({});
    }



    this.listof = function(controller, options) {
      var settings = $.extend({
            selector:'.document', // css selector for the given item
            prefix: '#d-', // id prefix for the given stuff
            namespace: 'documents',
            template: Handlebars.templates.document
          }),
          boxes = [],

          data = controller.get('data_' + settings.namespace),
          previouscount = countup? countup.endVal: 0;

      walt.verbose('(Grid) .listof');
      walt.verbose('...',data.length, 'items, selector:', settings.selector, ' replacing items...');

      
      
      
      countup = new countUp("counter-documents", previouscount, data.length, 0, 1.500);
      countup.start()

      for( var i in data.items){
        boxes.push(settings.template(data.items[i]));
      }

      container.append(boxes).nested('append', boxes);
      //container.append();
    }

  };

})();
