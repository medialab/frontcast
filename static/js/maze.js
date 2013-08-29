( function( $, window, undefined ){
	'use strict';

	window.maze = window.maze || {};
	maze.vars = maze.vars || {};
	maze.urls = maze.urls || {};
	maze.timers = {};
	/*


	    Logs
	    ====

	*/
	maze.log = function(){
		if( typeof maze.debug == "undefined" ) return;
		// return
		try{
			var args = ['maze:' ].concat( Array.prototype.slice.call(arguments) );
			console.log.apply(console, args );
		} catch(e){

		}
	}

	maze.error = function(){
		try{
			var args = ['   /\\  \n  /  \\\n / !! \\ ERROR maze:' ].concat( Array.prototype.slice.call(arguments) );
			args.push('\n/______\\')
			console.log.apply( console, args );
		} catch(e){}
	}

	maze.info = function(){
		try{
			var args = ['>>>> INFO maze:'].concat( Array.prototype.slice.call(arguments) );
			console.log.apply( console, args );
		} catch(e){}

	}



	/*


		WINDOW On / Trigger helpers
		===========================

	*/
	maze.events = maze.events || {};
	maze.on = function( eventType, selector, callback ){
		typeof callback == "undefined"? $(window).on( eventType, selector ): $(document).on( eventType, selector, callback );
	};

	maze.trigger = function ( eventType, data, nextEvent ){
		// nextevent sample: nextevent: { event: 'event name', data:{} }
		if( typeof data != "undefined" && data.delay ){
			clearTimeout( maze.vars[ 'timer_event_' + eventType ] );
			maze.vars[ 'timer_event_' + eventType ] = setTimeout( function(){
				$(window).trigger( eventType, typeof nextEvent != "undefined"? maze.chain(data, nextEvent): data );
			}, data.delay );
		} else {
			$(window).trigger( eventType, typeof nextEvent != "undefined"? maze.chain(data, nextEvent): data );
		}
		return true;
	};

	maze.chain = function( data, nextEvent ){
		data.next = nextEvent;
		return data;
	}

	maze.propagate = function( data ){
		typeof data.next != "undefined" && typeof data.next.event != "undefined" && maze.trigger( data.next.event, data.next.data )
	}

	/*


	    Modals (Bmazetstrap)
	    ==================

	*/
	maze.modals = {}
	maze.modals.init = function(){
		$(".modal").each( function( i, el ){ var $el = $(el); $(el).css("margin-top",- Math.round( $(el).height() / 2 )); }); maze.log("[maze.modals.init]");
	};


	/*


	    Tooltip
	    =======

	*/
	maze.tooltip = {}
	maze.tooltip.init = function(){
		$('body').tooltip({ selector:'[rel=tooltip]', animation: false, placement: function( tooltip, caller ){ var placement = $(caller).attr('data-tooltip-placement'); return typeof placement != "undefined"? placement: 'top'; } }); maze.log("[maze.tooltip.init]");};


	/*


	    Toast
	    =====

	*/
	maze.toast = function( message, title, options ){
		if(!options){options={}}if(typeof title=="object"){options=title;title=undefined}if(options.cleanup!=undefined)$().toastmessage("cleanToast");var settings=$.extend({text:"<div>"+(!title?"<h1>"+message+"</h1>":"<h1>"+title+"</h1><p>"+message+"</p>")+"</div>",type:"notice",position:"middle-center",inEffectDuration:200,outEffectDuration:200,stayTime:1900},options);$().toastmessage("showToast",settings)
	};

	maze.fault = function( message ){ maze.log("[maze.fault] message:", message );
		message = typeof message == "undefined"? "": message;
		maze.toast( message, maze.i18n.translate("connection error"), {stayTime:3000, cleanup: true});
	}


	/*


	    Common function
	    ===============

	*/
	maze.fn = {};
	maze.fn.slug = function( sluggable ){
		return sluggable.replace(/[^a-zA-Z 0-9-]+/g,'').toLowerCase().replace(/\s/g,'-');
	};

	maze.fn.get_cookie = function (e){
		var t=null;if(document.cookie&&document.cookie!=""){var n=document.cookie.split(";");for(var r=0;r<n.length;r++){var i=jQuery.trim(n[r]);if(i.substring(0,e.length+1)==e+"="){t=decodeURIComponent(i.substring(e.length+1));break}}}return t
	};

	maze.fn.wait = function( fn, options ){
		var timer = [options.id, options.delay].join('-');
		clearTimeout( maze.timers[  timer ] );
		maze.timers[  timer ] = setTimeout( function(){
			fn.apply( this, options.args);
		}, options.delay );
	}

	maze.fn.is_array = function( variable ){
		return Object.prototype.toString.call( variable ) === '[object Array]';
	}

	maze.fn.grab = function( list, iterator ){
		var result;

		for( var i in list ){
			try{
				if( iterator( list[i] ) )
					return list[i];
			} catch(e){
				continue;
			}

			if( typeof list[i] == "object" ){
				result = maze.fn.grab( list[i], iterator );
				if( result !== false )
					return result;
			}
		}
		return false;
	};

	/*


	    I18n
	    ====

	*/
	maze.i18n = { lang:'fr'};
	maze.i18n.translate = function( key, lang ){
		if( typeof lang != "undefined" )
			maze.i18n.lang = lang;

		var l = maze.i18n.lang;
		if ( maze.i18n.dict[l][key] == undefined	)
			return key;
		return 	maze.i18n.dict[l][key];
	}

	maze.i18n.dict = {
		'fr':{
			'no results found':"votre recherche n'a donné aucun résultat",
			"page not found":"page non trouvée",
			"connection error":"Connection error",
			"warning":"Attention",
			"delete selected absence":"Voulez-vous supprimer cette absence?",
			"offline device":"Échec de la connexion.",
			"check internet connection":"Veuillez vérifier la connexion internet de la tablette.",
			"welcome back":"welcome back",
			"loading":"chargement en cours…",
			"form errors":"Erreurs dans le formulaire",
			"error":"Erreur",
			"invalid form":"Veuillez vérifier les champs en rouge.",
			"empty dates":"Les dates de dé en rouge.",
			"empty message field":"Le message est vide.",
			"message sent":"Message envoyé",
			"timeout device":"Connexion trop lente.",
			"try again later": "Veuillez réessayer dans quelques instants.",
			"saving":"enregistrement en cours…",
			"changes saved":"Modifications Sauvegardées",
			"changes saved successfully":"Modifications Sauvegardées",
			"password should be at least 8 chars in length":"Le mot de passe doit faire au moins 8 caractères.",
			"password tmaze short":"Le mot de passe est trop court",
			"password changed":"Le mot de passe a été changé",
			"new passwords not match":"Saisissez à nouveau le nouveau mot de passe.",
			"invalid password":"Veuillez vérifier votre ancien mot de passe en respectant les minuscules et les majuscules.",
			"sms message sent":"SMS envoyé(s) avec succès.",
			"sms message sent failed":"Le SMS n'a pas pu être envoyé.",
			"sms invalid message":"Le texte du SMS est invalide.",
			"sms invalid phone numbers":"Numéro(s) de téléphone invalide(s)",
			"list numbers sms failure":"Certains SMS n'ont pu être envoyés.",
			"to change password": "Veuillez changer votre <br/> <b>mot de passe</b>",
			"please check accepted terms": "Veuillez accepter les conditions d'utilisation",

		},
		'en':{
			'no results found':"no search result",
			"connection error":"Connection error",
			"warning":"Warning",
			"loading":"loading..."
		}
	};


	/*


	    Bibtex
	    ======

	*/
	maze.fn.bibtex = function ( bibtex ){
		var bibjson = bibtex.replace(/^\s+|\s+$/g,'')
			.replace(/(\w+)\s*=\s*\{+/g,"\"$1\": \"")
			.replace(/\}+(?=\s*[,\}+])/g,"\"")
			.replace(/@(\w+)\s*\{([^,]*)/,"{\"bibtext_key\":\"$1\",\"$1\": \"$2\"");
		maze.log( bibjson )
		return JSON.parse(bibjson);
	}


	maze.fn.unique = function( array ){ var u = {}, a = []; for(var i = 0, l = array.length; i < l; ++i){ if(u.hasOwnProperty(array[i])) { continue; } a.push(array[i]); u[array[i]] = 1;} return a;}

	maze.rpc = {};
  maze.rpc.type = 'POST';
  maze.rpc.contentType = 'application/x-www-form-urlencoded';
  maze.rpc.expect = function(data) {
    return data !== null &&
      typeof data === 'object' &&
      !('error' in data);
  };
  maze.rpc.error = function(data) {
    this.log('Error:' + data);
  };
  maze.rpc.buildData = function(method, params) {
    return JSON.stringify({
      id: 1,
      jsonrpc: '2.0',
      method: method,
      params: params
    });
  };

})( jQuery, window );

