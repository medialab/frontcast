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
        container;

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
    };


    /*
      #Data stuff for the Grid Module
      It handles item activation on scene__updated.
    */

    this.triggers.events.data_documents__updated = function(controller) {
      walt.verbose('(Grid) listens to data_documents__updated');
      _self.listof(controller, {
        namespace:'documents'
      });
    };

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

      container.empty();
      
      for( var i in data.items){
        boxes.push(settings.template(data.items[i]));
      }

      container.append(boxes).nested('append', boxes);
      //container.append();
    }

  };

})();
