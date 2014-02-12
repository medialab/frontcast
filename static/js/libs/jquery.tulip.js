//
// usage $(document).tulip({selector: '.tip'})

;(function($, undefined) {
  'use-strict'

  var misc = {},
      tip,
      listeners = {},
      is_enabled = false;


  misc.enable = function(){
    is_enabled = true;
  }

  misc.init = function(options){
    var emitter = this.length? this: document;
    console.log('emit', emitter);
    $(emitter).on('mouseenter', '.facet', function(event){
      var item = $(this),
          content = item.attr('data-tip') || 'untitled';

      if(tip)
        tip.show({item: item, content: content})
      else
        tip = (new Tip()).show({item: item, content: content});
    }).on('mouseleave', '.facet', function(event){
      if(tip)
        tip.hide()
    });
  }

  var Tip = function(){
    var _self = this,
        
        t = $('<div/>',{
          'class': 'tulip'
        }).css({
          display: 'block',
          position: 'absolute',
          bottom: 0,
          width: '100%',
          'font-size': '1.3rem',  
          'border-radius': '2px',
          'background': 'rgba(255,255,255,0.9)',
        }),

        tb = $('<div/>',{
          'class': 'tulip-box'
        }).css({
          position: 'absolute',
          'text-align': 'left',
          'width': '120px',
          'margin-left': '-60px'
        }).append(t),

        tw = $('<div/>',{
          id: 'tulip-wrapper'
        }).css({
          position: 'fixed',
          top: 0,
          height: '100%',
          width: '100%',
          'z-index': 9999,
          display: 'block',
          'pointer-events': 'none'
        }).append(tb),

        initialized = false;

    this.init = function() {
      $('body').append(tw);
      initialized = true;
    };

    this.show = function(options) {
      var content = options.content || 'untitled<br/>untitled',
          gutter = options.gutter || 12,
          item = options.item;
      if(!options.item)
        return _self;

      t.show().html(content);

      tb.css({
          top:item.offset().top - gutter - $(document).scrollTop(),
          left: item.offset().left + item.outerWidth()/2
      });
      
      //console.log('show', content, item, item.offset().top, item.offset().left, item.width()/2);

      return _self;
    };

    this.hide = function() {
      t.hide();
    };

    _self.init();
    return _self;
  };

	$.fn.tulip = function(options) {
    

    // Method calling logic
    if (typeof options === "string" && misc[options] ) {
      return misc[options].apply(this, Array.prototype.slice.call(arguments, 1));
    } else if (typeof options === 'object' || ! options) {
      return misc.init.apply(this, arguments);
    } else {
      $.error( 'Method ' +  options + ' does not exist on jQuery.toastmessage' );
    }
  };
})(jQuery);