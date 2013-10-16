/*
  Intelligent filter module :D.
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Filters = function() {
    domino.module.call(this);

    var _self = this;

    this.triggers.events.scene_filters__updated = function(controller) {
      var scene = controller.get('scene'),
          scene_args = controller.get('scene_args');


      walt.verbose('(Filters) listen to scene__updated');

    };

    this.triggers.events.init = function(controller) {
      // initialize visualization plugin
    };
  };

})();
