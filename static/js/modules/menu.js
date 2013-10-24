/*
  Navigation menu module.
  It handles item activation on scene__updated.
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Menu = function() {
    domino.module.call(this);

    var _self = this,
        sidebar,
        entries,
        previous_scene;

    this.triggers.events.scene__synced = function(controller) {
      var scene = controller.get('scene');

      walt.verbose('(Menu) listen to scene__updated');

      if(scene != previous_scene) {
        entries.each(function(i) {
          var el = $(this),
              scenes = el.attr('data-scene').trim().split('|');
          walt.log(scenes, scene);
          if(scenes.indexOf(scene) != -1 )
            el.addClass('active');
          if(scenes.indexOf(previous_scene) != -1)
            el.removeClass('active');
        });
      }

      previous_scene = scene;
    };

    this.triggers.events.init = function(controller) {
      walt.verbose('(Menu) listen to init');
      sidebar = $('sidebar').first();
      entries = sidebar.find('li[data-scene]');

      sidebar.find('a[data-toggle="tooltip"]').tooltip();
    };


    

  };

})();
