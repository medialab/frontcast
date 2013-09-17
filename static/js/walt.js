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

  walt.SCENE_STARTUP = 'startup';
  walt.SCENE_VIEW_DOCUMENT = 'document';
  walt.SCENES = [
    walt.SCENE_STARTUP,
    walt.SCENE_VIEW_DOCUMENT
  ]

  walt.DOCUMENT_TYPES = {
    MEDIA: 'I', // external iframe, image, audio or video
    TEXT: 'T', // a note (at least originally)
    COMMENT: 'C',
    REFERENCE_CONTROVERSY: 'rY'
  };

  walt.UI_STATUS_LOCKED = 'locked';
  walt.UI_STATUS_UNLOCKED = 'unlocked';
  walt.UI_STATUSES = [
    walt.UI_STATUS_LOCKED,
    walt.UI_STATUS_UNLOCKED
  ]
  

  /*

      JSONRPC configuration
      =====================

  */
  walt.rpc = {
    type: 'POST',
    contentType: 'application/x-www-form-urlencoded',
    expect: function(data) {
      return data !== null && typeof data === 'object' && !('error' in data);
    },
    error: function(data) {
      walt.error('Error:' + data);
    },
    buildData: function(method, params) {
      return JSON.stringify({
        id: 1,
        jsonrpc: '2.0',
        method: method,
        params: params
      });
    }
  };

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
        var args = ['\twalt:' ].concat(Array.prototype.slice.call(arguments));
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
      } catch(e){}
    }
  };


  /*

      Misc
      ====

  */
  walt.misc.slug = function(sluggable){
    return sluggable.replace(/[^a-zA-Z 0-9-]+/g,'').toLowerCase().replace(/\s/g,'-');
  };

  walt.misc.get_cookie = function (e){
    var t=null;if(document.cookie&&document.cookie!=""){var n=document.cookie.split(";");for(var r=0;r<n.length;r++){var i=jQuery.trim(n[r]);if(i.substring(0,e.length+1)==e+"="){t=decodeURIComponent(i.substring(e.length+1));break}}}return t
  };

  walt.misc.is_array = function(variable){
    return Object.prototype.toString.call( variable ) === '[object Array]';
  }

  walt.misc.is_vimeo = function(url){
    return (/^(http\:\/\/|https\:\/\/)?(www\.)?(vimeo\.com\/)([a-zA-Z0-9\/]+)$/).test(url);
  }

  walt.misc.is_youtube = function(url){   // http://www.youtube.com/watch?v=axZTv5YJssA
    return (/^(http\:\/\/|https\:\/\/)?(www\.)?(youtube\.com\/watch\?v=)([A-Za-z0-9]+)$/).test(url);
  }

  walt.misc.is_flickr = function(url){ // http://www.flickr.com/photos/99902797@N03/9736909194
    return (/^(http\:\/\/|https\:\/\/)?(www\.)?(flickr\.com\/photos\/)([0-9A-Za-z\/@]+)$/).test(url);
  }



  /*

      Inits
      =====

  */
  walt.init = function(debug){
    walt.debug = debug || walt.DEBUG_INFO;
    console.log('\n\t----\n','\twelcome to walt:', walt.VERSION, '\n\t----\n');

    walt.CSRFTOKEN = walt.misc.get_cookie('csrftoken');
    $.ajaxSetup({
      crossDomain: false, // obviates need for sameOrigin test
      beforeSend: function(xhr, settings) { if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type))){ xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);}}
    });
    walt.log('csfrtoken updated');

    //walt.engine.init();
    walt.domino.init();
  };

})(window, jQuery, domino);
