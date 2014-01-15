/*
  Document Grid Module
  It handles item activation on scene__updated.
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Layout = function() {
    domino.module.call(this);

    var _self = this;

    this.triggers.events.ui__updated = function(){

    }
    
    this.resize = function(){
      _self.dispatchEvent('ui__update',{
        ui:{
          width: $(window).width(),
          height: $(window).height()
        }
      });
    }

    this.triggers.events.init = function(controller) {
      //walt.on(walt.events.LIST__LISTOF_COMPLETED, _self.listeners.LIST__LISTOF_COMPLETED);
      walt.on('resize', function(event) {
        walt.timers.resize = setTimeout(_self.resize, 200);
      });
      _self.resize();
      walt.verbose('(Layout) listens to init');
    };
  };

})();