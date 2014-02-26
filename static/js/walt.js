;(function(w, $, domino, undefined) {
  'use strict';

  w.walt = w.walt || {
    misc: {},
    user: {
      username: '',
      is_staff: false
    }
  };


  /*

      Common Useful Constants
      =======================

  */
  walt.VERSION = '0.0.0';
  walt.API_OK = "ok"
  walt.API_ERROR = "error"

  walt.STYLE_CONSOLE_SERVICES = 'color:#3887BE;background-color:gold';

  walt.CSRFTOKEN = 'django crfr token';
  walt.static_url = 'django static url for assets';
  walt.DEBUG_NONE = 0;
  walt.DEBUG_VERBOSE = 2; // will show walt.log() stuff and walt.verbose() stuff
  walt.DEBUG_INFO = 3; // will show walt.log() stuff
  walt.DEBUG_ERROR = 4; // will show error only
  
  walt.debug = walt.DEBUG_INFO;

  walt.PERMISSION_CAN_EDIT = 'CAN_EDIT'; // !WARNING this variable is actually used inside handlebar templates files. 

  walt.SCENES = [];
  walt.SCENE_INDEX = 'index';
  walt.SCENE_SEARCH = 'search';
  walt.SCENE_SEARCH_GRAPH = 'searchgr';
  
  walt.SCENE_DOCUMENT_VIEW = 'd';
  walt.SCENE_DOCUMENT_EDIT = 'de';
  walt.SCENE_DOCUMENT_ADD = 'da';
  walt.SCENE_REFERENCES = 'r';
  walt.SCENE_REFERENCE_EDIT = 're';

  walt.SCENE_PUBLIC = 'public'; // public documents
  walt.SCENE_ME = 'me';


  walt.SCENE_ARCHIVE = 'archive';

  walt.SCENE_USER = 'u';
  walt.SCENE_VIEW_DOCUMENT = 'document';
  walt.SCENE_MANAGE_REFERENCES = 'edit-references';
  walt.SCENE_WORLD_DRAFTS = 'drafts'; // show all drafts available to staff memers only (via api)

  walt.SCENE_WORKING_DOCUMENTS_INDEX = 'working-documents';
  

  walt.ROUTES = [
    {
      path: '/:?params:',
      scene: walt.SCENE_INDEX,
      description: ''
    },
    {
      path: '/s:?params:',
      scene: walt.SCENE_SEARCH,
      description: ''
    },
    {
      path: '/g:?params:',
      scene: walt.SCENE_SEARCH_GRAPH,
      description: 'filter/explore collection with graph view document/tag bipartite graph'
    },
    {
      path: '/d/add/',
      scene: walt.SCENE_DOCUMENT_ADD,
      description: ''
    },
    {
      path: '/d/{slug}:?params:',
      scene: walt.SCENE_DOCUMENT_VIEW,
      description: '',
      rules: {
        slug: /[0-9a-zA-Z\-]+/
      }
    },
    {
      path: '/d/{slug}/edit/:?params:',
      scene: walt.SCENE_DOCUMENT_EDIT,
      description: ''
    },
    {
      path: '/teaching/:?params:',
      scene: walt.SCENE_WORKING_DOCUMENTS_INDEX
    },
    {
      path: '/r/',
      scene: walt.SCENE_REFERENCES,
      description: ''
    },
    {
      path: '/reference/{slug}/edit',
      scene: walt.SCENE_REFERENCE_EDIT, 
      description: ''
    },
    {
      path: '/archive:?params:',
      scene: walt.SCENE_ARCHIVE
    },

    {
      path: '/public:?params:',
      scene: walt.SCENE_PUBLIC
    },
    {
      path: '/archive:?params:',
      scene: walt.SCENE_ARCHIVE
    },
    {
      path: '/me:?params:',
      scene: walt.SCENE_ME
    },
    {
      path: '/admin:?params:',
      scene: walt.SCENE_ADMIN
    },
    {
      path: '/u/{username}:?params:',
      scene: walt.SCENE_USER
    }
  ]

  for(var i in walt.ROUTES)
    walt.SCENES.push(walt.ROUTES[i].scene);
  

  walt.DOCUMENT_TYPES = {
    MEDIA: 'I', // external iframe, image, audio or video
    TEXT: 'T', // a note (at least originally)
    COMMENT: 'C',
    REFERENCE_CONTROVERSY: 'rY',
    REFERENCE_CONTROVERSY_VIDEO: 'ControversyVideo',
    REFERENCE_CONTROVERSY_WEB: 'ControversyWeb'
  };


  walt.UI_STATUS_LOCKED = 'locked';
  walt.UI_STATUS_UNLOCKED = 'unlocked';
  walt.UI_STATUSES = [
    walt.UI_STATUS_LOCKED,
    walt.UI_STATUS_UNLOCKED
  ]
  
  /*
     events for module interactions.
     Cfr module
  */
  walt.events = {};
  walt.timers = {}; // a collection of timers id for the cleartimeout functions

  walt.on = function(type, handler) {
    $(window).on(type, handler);
  };

  walt.trigger = function(type, data, options) {
    var d = data || {},
        o = options || {};

    if(o.delay > 0) {
      clearTimeout(walt.timers[type]);
      walt.timers[type] = setTimeout(function() {
        $(window).trigger(type, d);
      }, o.delay);
    } else {
      $(window).trigger(type, data);
    };
  };

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
      position: "bottom-right",
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
  walt.log = function(){
    if(walt.debug >= walt.DEBUG_INFO){
      try{
        var args = ['\t'].concat(Array.prototype.slice.call(arguments));
        console.log.apply(console, args);
      } catch(e){}
    }
  };

  walt.verbose = function(){
    if(walt.debug >= walt.DEBUG_VERBOSE){
      var index = '          ',
          counter;
      
      walt.debug_index = walt.debug_index || 0;      

      if(arguments[0] == '...'){
        counter = '      ';
      } else{
        walt.debug_index++;
        index = index + walt.debug_index;
      }

      counter = index.substr(-6);

      try{
        var args = ['\t', counter].concat(Array.prototype.slice.call(arguments));
        console.log.apply(console, args);
      } catch(e){}
    }
  };

  walt.error = function(){
    try{
        var args = ['   /\\  \n  /  \\\n / !! \\ ERROR walt:'].concat(Array.prototype.slice.call(arguments));
        args.push('\n/______\\');
        console.log.apply(console, args);
    } catch(e){}
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
    return the first element of a javascript dict.
    To be improved.
  */
  walt.misc.first = function(dict) {
    for(var i in dict)
      return dict[i];
  };

  /*

      Inits
      =====

  */
  walt.init = function(debug){
    walt.debug = debug || walt.DEBUG_INFO;
    walt.log('\n\t----\n','\twelcome to walt:', walt.VERSION, '\n\t----\n');

    walt.CSRFTOKEN = walt.misc.get_cookie('csrftoken');
    $.ajaxSetup({
      crossDomain: false, // obviates need for sameOrigin test
      beforeSend: function(xhr, settings) { if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type))){ xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);}}
    });
    walt.log('csfrtoken: ', walt.CSRFTOKEN);

    //walt.engine.init();
    walt.domino && walt.domino.init();
  };

})(window, jQuery, domino);
