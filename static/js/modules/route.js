;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Route = function() {
    domino.module.call(this);


    var _last_hash,
        _self = this,
        _dry = {
          scene: {
            shortcut: 's',
            defaultValue: walt.SCENE_STARTUP
          }
        },
        _expand = Object.keys(_dry).reduce(function(res, k) {
          res[_dry[k].shortcut] = k;
          return res;
        }, {});

    // Just a small tool to identify whether
    function isDisplayable(v) {
      switch (domino.struct.get(v)) {
        case 'object':
          return Object.keys(v).length > 0;
        case 'array':
          return v.length > 0;
        default:
          return !!v;
      }
    }

    function encode(o) {
      var k,
          o2 = {};

      o = o || {};
      for (k in o)
        if (isDisplayable(o[k]))
          o2[_dry[k] ? _dry[k].shortcut : k] = o[k];

      return decodeURIComponent($.param(o2));
    }

    function decode(s) {
      var k,
          o = $.deparam.fragment(),
          o2 = {};
      for (k in o)
        o2[_expand[k] || k] = o[k];

      for (k in _dry)
        o2[k] = (k in o2) ? o2[k] : _dry[k].defaultValue;

      return o2;
    }

    function change_hash(controller) {
      _last_hash = encode({
        scene: controller.get('scene')
      });
      window.location.hash = _last_hash;
    }

    function evaluate_hash() {
      walt.log('evaluate_hash')
      // Check that this update is not actually caused by the same Location
      // module:
      if (window.location.hash.substr(1) === _last_hash)
        return;

      var hash = decode(window.location.hash.substr(1));
      _self.log('Hash update:', hash);
      _self.dispatchEvent('scene__update', hash);
    }


    this.triggers.events.scene__stored = change_hash;
    this.triggers.events.scene__updated = change_hash;
    this.triggers.events.init = evaluate_hash;

    $(window).on('hashchange', evaluate_hash);
  };

})();
