/*
  Document Grid Module
  It handles item activation on scene__updated.
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Layout = function() {
    domino.module.call(this);

    var _self = this,
        w = 0,
        h = 0,
        main = $("#main"),
        header = $('header'),
        footer = $('footer');

    this.triggers.events.ui__updated = function(){

    }
    
    this.resize = function(){
      w = $(window).width();
      h = $(window).height();

      _self.ghostscroll();

      _self.dispatchEvent('ui__update',{
        ui:{
          width: w,
          height: h
        }
      });
    }

    this.ghostscroll = function(){
      if(w == 0)
        return;

      var y = $(document).scrollTop(),
          scrollheight =main.outerHeight();

      if(y < 12) // header shadow invisible
        header.hasClass('drop-shadow') && header.removeClass('drop-shadow');
      else 
        header.addClass('drop-shadow');
      /*
      if( y > scrollheight - h - 12){ // footer shadow invisible
        footer.hasClass('drop-shadow') && footer.removeClass('drop-shadow');
      } else if(){

      } else {

      }
      console.log('start',  y, scrollheight - h);*/
    }

    this.triggers.events.init = function(controller) {
      //walt.on(walt.events.LIST__LISTOF_COMPLETED, _self.listeners.LIST__LISTOF_COMPLETED);
      walt.on('resize', function(event) {
        walt.timers.resize = setTimeout(_self.resize, 200);
      });
      _self.resize();
      walt.verbose('(Layout) listens to init');

      $(document).scroll(_self.ghostscroll);
    };
  };

})();