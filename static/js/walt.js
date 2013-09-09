;(function(w, $, domino, undefined) {
  'use strict';

  w.walt = w.walt || {
    misc: {}
  };


  /*

      Common Useful Constants
      =======================

  */
  walt.VERSION = '0.0.0';

  walt.CSRFTOKEN = 'django crfr token';

  walt.DEBUG_NONE = 'N';
  walt.DEBUG_INFO = 'I'; // will show log and info
  walt.DEBUG_ERROR = 'E'; // will show error only

  walt.debug = walt.DEBUG_INFO;


  /*

      Toast
      =====

      Launch Toast Message in an android fashion.
      Require jquery.toastmessage plugin.
  */
  walt.toast = function(message, title, options){
    if(!options){
      options={}
    };
    if(typeof title=="object"){
      options=title;
      title=undefined;
    }
    if(options.cleanup!=undefined)
      $().toastmessage("cleanToast");

    var settings=$.extend({
      text: "<div>"+(!title?"<h1>"+message+"</h1>":"<h1>"+title+"</h1><p>"+message+"</p>")+"</div>",
      type: "notice",
      position: "middle-center",
      inEffectDuration: 200,
      outEffectDuration: 200,
      stayTime: 1900
    },options);

    $().toastmessage("showToast", settings);
  };


  /*

      Callback Factory
      ================

      Chain functions - even with a user defined delay if desired.
      Thanks to Alexis Jacomy

  */
  walt.factory = function(fn){
    return function(options) {
      var self = this,  // TODO check SCOPE
          settings = options || {},
          closure = function(){
            fn.call(self, settings, function() {
              if(settings.callback)
                settings.callback.apply(this, settings.args);
            });
          };

      if(settings.delay){
        setTimeout(closure, settings.delay);
      } else {
        closure();
      }
    }
  };


  /*

      Logs
      ====

  */
  walt.log = walt.info = function(){
    if(walt.debug == walt.DEBUG_INFO){
      try{
        var args = ['walt:' ].concat(Array.prototype.slice.call(arguments));
        console.log.apply(console, args);
      } catch(e){}
    }
  };

  walt.error = function(){
    if(walt.debug == walt.DEBUG_ERROR || walt.debug == walt.DEBUG_INFO){
      try{
        var args = ['   /\\  \n  /  \\\n / !! \\ ERROR walt:' ].concat(Array.prototype.slice.call(arguments));
        args.push('\n/______\\');
        console.log.apply(console, args);
        debugger;
      } catch(e){}
    }
  };


  /*

      Misc
      ====

  */
  walt.misc.slug = function( sluggable ){
    return sluggable.replace(/[^a-zA-Z 0-9-]+/g,'').toLowerCase().replace(/\s/g,'-');
  };

  walt.misc.get_cookie = function (e){
    var t=null;if(document.cookie&&document.cookie!=""){var n=document.cookie.split(";");for(var r=0;r<n.length;r++){var i=jQuery.trim(n[r]);if(i.substring(0,e.length+1)==e+"="){t=decodeURIComponent(i.substring(e.length+1));break}}}return t
  };

  walt.misc.is_array = function( variable ){
    return Object.prototype.toString.call( variable ) === '[object Array]';
  }


  /*

      Inits
      =====

  */
  walt.init = function(debug){
    walt.debug = debug || walt.DEBUG_INFO;
    walt.log('welcome', walt.VERSION, '\n----\n');

    //walt.engine.init();
    walt.domino.init();
  };

})(window, jQuery, domino);
