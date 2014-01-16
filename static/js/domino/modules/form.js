/*
  Search implementation
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Form = function() {
    domino.module.call(this);

    var _self = this,
        input;


    this.triggers.events.init = function(controller) {
      walt.verbose('(Form) listens to init');
      
      $("select").fancySelect();

    };
  };

})();
