/*
  Search / filter implementation
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Filters = function() {
    domino.module.call(this);

    var _self = this,
        input,
        handlers ={ };

    

    handlers.set_property = function(event){
      var slug = $(this).attr('data-slug'),
          scene_args = $.extend({}, walt.domino.controller.get('scene_args')),
          filter = $(this).attr('data-filter');

      if(!filter){
        walt.error('(Filters) .set_property filter var not defined');
        return;
      };

      walt.log('(Filters) .set_property  "', filter, '":["', slug, '"]', scene_args);

      // setting filters accurately
      scene_args.params = scene_args.params || {};
      scene_args.params.filters = scene_args.params.filters || {};
      walt.verbose('... .set_property, filters already in place:', scene_args.params.filters);
      scene_args.params.filters[filter] = [slug]
      walt.verbose('... .set_property, filters modified:', scene_args.params.filters);

      _self.send_args(scene_args);
    };


    handlers.remove_property = function(event){
      var filter = $(this).attr('data-filter');

      scene_args.params = scene_args.params || {};
      scene_args.params.filters = scene_args.params.filters || {};
      
      if(scene_args.params.filters[filter])
        delete scene_args.params.filters[filter];

      _self.send_args(scene_args);
    };


    this.send_args = function(scene_args) {
      var scene = walt.domino.controller.get('scene');
      walt.verbose('(Filters) .send_args:', scene_args.params.filters);

      _self.dispatchEvent('scene_args__update', {
        scene_args: scene_args
      });
      
      _self.dispatchEvent('scene__update', {
        scene: scene
      });
    };


    this.triggers.events.init = function(controller) {
      walt.verbose('(Filters) listens to init');
      // REMOVED ! $(document).on('click', '.tag', handlers.set_property);
      // REMOVED ! $(document).on('click', '.type', handlers.set_property);
    };


  };

})();
