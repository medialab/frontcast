/*
  Search / filter implementation
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Search = function() {
    domino.module.call(this);

    var _self = this,
        input,
        order_by;

    this.send_query = function(event) {
      var scene_args = walt.domino.controller.get('scene_args'),      
          query = input.val();
      
      walt.verbose('(Search) .send_query, query:',query);


      scene_args.params = scene_args.params || {};
      scene_args.params.search = query;

      _self.dispatchEvent('scene_args__update', {
        scene_args: scene_args
      });
      
      _self.dispatchEvent('scene__update', {
        scene: walt.SCENE_SEARCH
      });

    };
    
    this.order_by = function(order){
      var order_by = order.split("|"),
          scene_args = walt.domino.controller.get('scene_args'),
          scene = walt.domino.controller.get('scene');

      scene_args.params = scene_args.params || {};
      scene_args.params.order_by = JSON.stringify(order_by);

      walt.verbose('(Search) .order_by:',order_by);

      _self.dispatchEvent('scene_args__update', {
        scene_args: scene_args
      });
      
      _self.dispatchEvent('scene__update', {
        scene: scene
      });
    }

    this.triggers.events.scene__filled = function(controller) {
      var scene_params = controller.get('scene_params');
      walt.verbose('(Search) listens to scene__filled');
      if(scene_params.search){
        walt.verbose('...', 'setting input query');
        input.val(scene_params.search || '')
      }
    }

    this.triggers.events.init = function(controller) {
      walt.verbose('(Search) listens to init');
      input = $("#search-query").on('keydown', function(event) {
        if(event.which == 13) _self.send_query();
      });
      order_by = $("#order-by").on('change', function(event){
        _self.order_by($(this).val());
      });

      $(".search .icon").on('click', _self.send_query);


    };
  };

})();
