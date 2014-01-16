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
        container, // grid document viewer (nested plugin)
        viewer; // single document viewer

    this.triggers.events.scene__synced = function(controller) {
      var scene = controller.get('scene');
      walt.verbose('(Grid) listens to scene__updated');
    };

    this.triggers.events.init = function(controller) {
      walt.verbose('(Grid) listens to init');
      container = $("#grid-of-documents").nested({
        minWidth: 190,
        gutter: 12,
        animate: false
      });
      viewer = $("#single-document");
    };


    /*
      #Data stuff for the Grid Module
      It handles item activation on scene__updated.
    */

    this.triggers.events.data_documents__updated = function(controller) {
      var scene = controller.get('scene');

      walt.verbose('(Grid) listens to data_documents__updated', scene);
      
      (scene == walt.SCENE_INDEX || walt.SCENE_SEARCH) && _self.listof(controller, {
        namespace:'documents'
      });

      scene == walt.SCENE_DOCUMENT_VIEW && _self.single(controller, {
        namespace:'documents'
      });
    };

    this.single = function(controller){
      
      var doc = controller.get('data_documents').items[0];

      walt.verbose('(Grid) .single');
      container.empty();
      viewer.append( Handlebars.templates.document_view(doc));
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
    }

    this.listof = function(controller, options){
      var settings = $.extend({
            selector:'.document', // css selector for the given item
            prefix: '#d-', // id prefix for the given stuff
            namespace: 'documents',
            template: Handlebars.templates.document
          }),
          boxes = [],

          data = controller.get('data_' + settings.namespace);

      walt.verbose('(Grid) .listof');
      walt.verbose('...',data.length, 'items, selector:', settings.selector, ' replacing items...');

      viewer.empty();
      container.empty();
      
      for( var i in data.items){
        boxes.push(settings.template(data.items[i]));
      }

      container.append(boxes).nested('append', boxes);
      //container.append();
    }

  };

})();
