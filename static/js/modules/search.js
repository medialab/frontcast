/*
  Search implementation
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Search = function() {
    domino.module.call(this);

    var _self = this,
        input;

    this.send_query = function(event) {
      var scene_args = walt.domino.controller.get('scene_args') || {},      
          query = input.val();
          
      scene_args.params = scene_args.params || {};
      scene_args.params.search = query;

      _self.dispatchEvent('scene_args__update', {
        scene_args: scene_args
      });
      _self.dispatchEvent('scene__update', {
        scene: walt.SCENE_SEARCH
      });
    };
    
    this.triggers.events.scene__synced = function(controller) {
      var scene_params = controller.get('scene_params');
      
      input.val(scene_params.search || '')
      walt.verbose('(Search) listens to scene__synced');
    }

    this.triggers.events.init = function(controller) {
      walt.verbose('(Search) listens to init');
      input = $("#search").on('keydown', function(event) {
        if(event.which == 13) _self.send_query();
      });
      $(".search .icon").on('click', _self.send_query);
    };
  };

})();
