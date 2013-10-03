;(function(w, $, undefined) {
  'use strict';

  var walt = w.walt || {};
  
  walt.move = {
		duration: 1250,
		calculate_duration: function(distance) {
			return Math.min( 750, Math.max( 350, distance / 0.6))
		},
		easing: "easeInOutQuad"
	};

	walt.move.DESTROY = 'd';
	walt.move.FADEOUT = 'f-';
	walt.move.FADEIN = 'f+';

  walt.move.factory = function(fn) {
		return function(el, options) {
			if (typeof el === 'string' )
				el = $(el); // transform automatically selector in 

			if(el.data().status == walt.move.DESTROY){
				walt.error('walt.move.factory: cannot move a destroyed elements ...', el.data().status);
				return;
			}
			fn.call(this, el, options || {}, function() {
				if (options && typeof options.complete === 'function')
					options.complete.apply(this, options.args || {});
			});
		}
	};

	/*


		Basic shared movement
		=====================

	*/
	walt.move.fadeout = walt.move.factory(function(el, options, complete) {
		el.data('status', walt.move.FADEOUT);
		el.stop().delay(options.delay || 0).animate({
			opacity: 0
		},{
			easing: walt.move.easing,
			duration: walt.move.duration,
			complete: complete,
			queue: false
		});
	});

	walt.move.fadein = walt.move.factory(function(el, options, complete) {
		el.data('status', walt.move.FADEIN);
		walt.log(options.delay);
		el.stop().delay(options.delay || 0).animate({
			opacity: 1
		},{
			easing:walt.move.easing,
			duration: walt.move.dutration,
			complete:complete,
			queue:false
		});
	});

	walt.move.destroy = walt.move.factory(function(el, options, complete) {
		walt.move.fadeout(el, {
			delay: options.delay || 0,
			complete:function(){
				el.data('status', walt.move.DESTROY);
				el.remove();
				complete();
			}
		});
	});

})(window, jQuery);
