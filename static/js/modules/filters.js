/*
  Intelligent filter module :D.
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Filters = function() {
    domino.module.call(this);

    var _self = this,
        collection,
        dropdown;

    this.triggers.events.data_documents_filters__updated = function(controller) {
      var scene = controller.get('scene'),
          filters = controller.get('data_documents_filters');


      walt.verbose('(Filters) listens to data_documents_filters__update', filters);

    };

    this.triggers.events.scene__synced = function(controller) {
      var filters = controller.get('data_documents_filters');
      
      walt.verbose('(Filters) listens to scene__synced', filters);
      walt.trigger('FILTERS__START', filters);
    }

    this.triggers.events.init = function(controller) {
      // initialize visualization plugin
      walt.verbose('(Filters) listens to init');
      collection = $(".filters").filters();
      dropdown = $("#dropdown-filters").on('click', '.toggle-dropdown', function(event) {
        if(!dropdown.hasClass('visible')) {
          dropdown.addClass('visible');
          $("#search").focus();
        } else {
          dropdown.removeClass('visible');
        }
      });
    };
  };

})();
