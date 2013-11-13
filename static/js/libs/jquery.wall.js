;(function($, undefined) {
  'use-strict'
  var walls = {},
      cursor = 0;

  /*
    handle the collection of columns
  */
  var Wall = function() {
    var s = this;
    s.settings = {
      column_width: 400,
      column_height: 300,
      items_per_column: 3,
      selector: '.pin',
      column_selector: '.wall-column',
      templates:{
        column: '<div class="wall-column">' +
                '  <div class="wall-column-header">' +
                '    <div class="wall-column-header-line"></div>' + 
                '    <div class="wall-column-shadow"><div class="inner"></div></div>' + 
                '  </div>'+
                '  <div class="wall-column-box nano"><div class="content"></div></div>'+
                '  <div class="wall-column-footer"><div class="wall-column-shadow"><div class="inner"></div></div></div>'+
                '</div>'
      }
    };

    s.columns = {};

    s.events = {
      change_status: 'wall_change_status',
      update: 'wall_update',
      set_property: 'wall_set_property',
      get_propery: 'wall_get_property'
    };

    s.init = function(el, options) {
      s.el = el.css({
        position: 'relative',
        width: '100%',
        height: s.settings.column_height + 100,
        overflow: 'scroll'
      });

      s.settings = $.extend(s.settings, options);

      for(var i in s.events){
        s.on(s.events[i], s[i]);
      }
      
      
      //s.on(s.events.draw, s.draw);
      s.trigger(s.events.change_status, {
        status:'init'
      });

      

      
      return s;
    };

    s.update = function(event) {
      var items = $(s.settings.selector, s.el),
          columns = $(s.settings.column_selector, s.el),
          desired_columns = Math.ceil(items.length/s.settings.items_per_column),
          diff_columns = columns.length - desired_columns;

      if(diff_columns<0) {
        for(var i=0; i>diff_columns;i--) {
          s.el.append(s.settings.templates.column);

        }
        columns = $(s.settings.column_selector, s.el);
      };

     
      //alert(desired_columns);
      items.each(function(index,item) {
        var column_index = Math.floor(index/s.settings.items_per_column),
            column = $(columns.get(column_index));

        column.css({
            left: column_index * s.settings.column_width,
            width: s.settings.column_width,
            height: s.settings.column_height
        });

        $('.wall-column-box .content', column).append(item);
      });
      
      $('.wall-column-box .content', s.el).on('scroll', function() {
        var content = $(this),
            scrolldelta = content[0].scrollHeight - s.settings.column_height,
            box = content.closest('.wall-column-box'),
            header = box.prev(),
            footer = box.next(),
            scrolltop = content.scrollTop();

        if(scrolltop > 10)
          !header.hasClass('shadow') && header.addClass('shadow');
        else if(scrolltop < 10) 
          header.hasClass('shadow') && header.removeClass('shadow');
        
        if(scrolldelta - scrolltop > 10)
          !footer.hasClass('shadow') && footer.addClass('shadow');
        else
          footer.hasClass('shadow') && footer.removeClass('shadow');
        //if(scrolldelta)
        // console.log( scrolldelta,scrolltop);
      });

      $('.wall-column-box.nano', s.el).nanoScroller({alwaysVisible: true});
    
      
      
      s.trigger(s.events.change_status, {
        status:'updated'
      });
    }

    s.set_property = function(event, data) {
      $.extend(s.settings, data);
    }
    
    
    s.change_status = function(event, data) {
      s.el.attr('data-wall', data.status);
    }

    s.draw = function(event) {
      console.log(s.original_data);
    } 

    s.on = function(event, callback) {
      s.el.on(event, callback);
    };

    s.trigger = function (event, data) {
      s.el.trigger(event, data);
    };
  };

	$.fn.wall = function(options, data) {
    var len = this.length;

    return this.each(function(index) {
      var wall = $(this),
        instance;

      if(!wall.attr('data-wall-id')) {
        wall.attr('data-wall', 'pre-init');
        wall.attr('data-wall-id', cursor);
        walls[cursor] = (new Wall).init(wall, options);
        cursor ++;
      }

      if(typeof options == "string") {
        instance = walls[wall.attr('data-wall-id')];
        instance.trigger(instance.events[options], data);
      }
    });
  };
})(jQuery);