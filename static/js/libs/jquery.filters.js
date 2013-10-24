;(function($, undefined) {
  var v_histogram = function() {
    var settings = {
            title: 'untitled',
        }

    this.init = function(el, options, data){
      settings = $.extend(settings, options);
      filter = $('<div></div>').html('<h2>'+settings.title+'</h2>');
      for(var key in data){

      }
      el.append(filter);
    }
  }
  /*
    handle the collection of filters
  */
  var Filters = function() {
    var s = this;
        
    
    
    s.el = null;
    
    s.events = {
      start: 'FILTERS__START',
      change: 'FILTERS__CHANGE',
      changed: 'FILTERS__CHANGED',
      draw: 'FILTERS__DRAW'
    };

    s.settings = {
      templates: [
        {
          id: 'years',
          data: 'tags.Da',
          type: 'timeline'
        },
        {
          id: 'years',
          data: 'tags.In',
          type: 'v_histogram'
        },
        {
          data: 'type',
          type: 'v_histogram'
        }
      ]
    };

    s.original_data = {}; // the original data
    s.filtered_data = {};

    s.init = function(el, options, uuid) {
      s.el = el;
      s.settings = $.extend(s.settings, options);

      s.on(s.events.start, s.start);
      s.on(s.events.change, s.change);
      s.on(s.events.draw, s.draw);
    };

    
    s.start = function(event, data) {
      s.original_data = data;
      s.filtered_data = data;
      s.trigger(s.events.draw);
    };

    s.change = function(event, data) {
      s.filtered_data = data;
      s.trigger(s.events.draw);
    };

    s.draw = function(event) {
      console.log(s.original_data);
    } 

    s.on = function(event, callback) {
      $(window).on(event, callback);
    };

    s.trigger = function (event, data) {
      $(window).trigger(event, data);
    };
  };

	$.fn.filters = function(options) {
    var len = this.length;

    return this.each(function(index) {
      var me = $(this),
          uuid = 'filters' + (len > 1 ? '-' + ++index : ''),
          instance = (new Filters).init(me, options, uuid);
    });
  };
})(jQuery);