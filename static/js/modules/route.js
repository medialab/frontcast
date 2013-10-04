/*
  depede
  
  This module depends on crossroads.min.js and hasher.min.js
  to interprete the navigation hash.
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Route = function() {
    domino.module.call(this);

    var _self = this,
        _routes = [];


    function bind(route, scene) {
      _routes[ scene ] = route;

      route.matched.add(function(){
        var scene_args = {};

        // a delicate pairing! We trust the routing lib so much...
        for(var i=0; i<arguments.length; i++){
          scene_args[route._paramsIds[i]] = arguments[i];
        }

        walt.verbose('(Route) bind scene: [', scene,']', scene_args);

        _self.dispatchEvent('scene_args__update', {
          scene_args: scene_args
        });

        _self.dispatchEvent('scene__update', {
          scene: scene
        });
      });
    };


    function parse_hash(h, previous) {
      walt.verbose('(Route) parse_hash: ', h);
      crossroads.parse(h);
    };


    /* 

      Module Init.
      ------------

      Add browser hash listener, start hasher with the current value.
      An handlebar helper integrates the crossroads.interpolate() interpolation function with the stored walt routes.
      
      handlebars usage:
      {{#url <walt.SCENE> param param2 ... paramN}}{{/url}}

    */
    Handlebars.registerHelper("url", function(scene) {
      var params = {};

      for( var i=1; i<arguments.length-1; i+=2){
        params[arguments[i]] = arguments[i+1];
      };
      return _routes[scene].interpolate(params);
    });


    this.triggers.events.init = function(controller) {
      walt.verbose('(Route) listen to init');
      for(var i in walt.ROUTES){
        var route = crossroads.addRoute(walt.ROUTES[i].path),
            scene = walt.ROUTES[i].scene;
        
        bind(route, scene);
      }

      hasher.initialized.add(parse_hash); //parse initial hash
      hasher.changed.add(parse_hash); //parse hash changes
      hasher.init();
    }


    this.triggers.events.scene__update = function(controller) {
      walt.verbose('(Route) listen to scene__update');
    };
  };
})();
