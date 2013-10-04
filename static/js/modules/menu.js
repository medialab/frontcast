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
        entries = {},
        previous_scene;

    this.triggers.events.scene__updated = function(controller) {
      var scene = controller.get('scene');


      walt.verbose('(Menu) listen to scene__updated');

      if(previous_scene && entries[previous_scene])
        entries[previous_scene].removeClass('active');
      
      if(previous_scene != scene && entries[scene])
        entries[scene].addClass('active');

      previous_scene = scene;
    };

    this.triggers.events.init = function(controller) {
      walt.verbose('(Menu) listen to init');
      $('sidebar li[data-scene]').each(function(i){
        var entry = $(this),
            scene = entry.attr('data-scene');
        walt.verbose('... entry:',scene);
        entries[scene] = entry;
      });
    };
  };

})();
