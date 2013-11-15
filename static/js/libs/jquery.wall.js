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
      column_width: 320,
      column_height: 300,
      items_per_column: 3,
      selector: '.pin',
      item_id_prefix: '#pin-',
      column_selector: '.wall-column',
      item_template:  function(){ return '<div></div>'}, // handlebar function
      data:{}, /* {
                      ids: Array[49],
                      items: Array[49],
                      length: 49,
                      limit: 49
                      offset: 0
                    }
                */
      column_template : Handlebars.templates.column,
      column_placeholders_template: Handlebars.templates.column_placeholders
    };

    s.columns = {};
    s.lis = {}; // collection of mouse listeners
    s.timers = {}; //timeout vars 

    s.events = {
      change_status: 'wall_change_status',
      update: 'wall_update',
      set_property: 'wall_set_property',
      get_propery: 'wall_get_property',
      resize: 'wall_resize'
    };


    s.lis.wall_scroll = function(event){
      var scrollleft = s.wall.scrollLeft(),
          width = s.wall_width,
          available_width = s.wall[0].scrollWidth,
          p_left = s.placeholders.first(),
          p_right = p_left.next();

      if(scrollleft > 0)
        !p_left.hasClass('shadow') && p_left.addClass('shadow');
      else{
        p_left.hasClass('shadow') && p_left.removeClass('shadow');
      } 

      if(available_width > scrollleft +  width)
        !p_right.hasClass('shadow') && p_right.addClass('shadow');
      else
        p_right.hasClass('shadow') && p_right.removeClass('shadow');

      clearTimeout(s.timers.scrollabilly);
      s.timers.scrollabilly = setTimeout( function(){s.scrollabilly(scrollleft)}, 200); // evaulate reader position
    };

    s.cursor = {
      column: -1,
      item: -1
    }

    s.scrollabilly = function(scrollleft){
      return
      var column_cursor = -1;

      for(var i in s.columns){
        if(s.columns[i].left < scrollleft)
          continue;
        if(s.columns[i].left > scrollleft + s.settings.column_width)
          break;
        
        column_cursor = i;
        break;
      }
      walt.verbose('old', s.cursor.column, 'new',column_cursor);

      if(s.cursor.column == -1){
        s.columns[column_cursor].el.addClass('active');
      }else if(column_cursor != s.cursor.column){
        s.columns[column_cursor].el.addClass('active');
        s.columns[s.cursor.column].el.removeClass('active');
        walt.verbose(  'chanced', column_cursor);
      }

      s.cursor.column = column_cursor;

    };





    s.init = function(el, options) {
      s.el = el;
      s.wall = $('<div/>',{
          "class": "wall"
        }).css({
          position: 'relative',
          width: '100%',
          'overflow-y': 'hidden',
          'overflow-x': 'scroll'
        });
      
      s.el.empty()
        .css({position: 'relative', overflow: 'hidden'})
        .append(s.wall);

      s.wall.scroll(s.lis.wall_scroll);
      s.wall.on('mouseenter', s.settings.selector, function(event){
        var item = $(this),
            column = item.closest('.wall-column'),
            column_cursor = column.index(),
            item_cursor =  column_cursor* s.settings.items_per_column + item.index();
        
        if(s.cursor.item == -1)
          item.addClass('active')
        else if(s.cursor.item  != item_cursor){
          $(s.settings.selector + '.active',s.wall).removeClass('active');
          item.addClass('active');
        }
        s.cursor.item = item_cursor;

        walt.verbose(s.cursor.item);
        
        if(s.cursor.column == -1){
          s.columns[column_cursor].el.addClass('active');
        }else if(column_cursor != s.cursor.column){
          s.columns[column_cursor].el.addClass('active');
          s.columns[s.cursor.column].el.removeClass('active');
          walt.verbose(  'chanced', column_cursor);
        }

        s.cursor.column = column_cursor;

      })
      /*s.wall.pep({
        axis: "x",
        easeDuration: 500,
        constrainTo: 'parent'
      });*/

      s.settings = $.extend(s.settings, options);

      $('.wall-column-placeholder', s.el).remove();
      s.el.append(s.settings.column_placeholders_template());
      s.placeholders = $('.wall-column-placeholder', s.el);

      for(var i in s.events){
        s.on(s.events[i], s[i]);
      }
      
      
      //s.on(s.events.draw, s.draw);
      s.trigger(s.events.change_status, {
        status:'init'
      });

      s.resize();

      return s;
    };

    s.resize = function(event, data) {
      var data = data || {},
          column_height = column_height || s.settings.column_height;

      s.wall.height(column_height + 48);
      s.el.height(column_height + 48);

      s.wall_width = s.wall.width();

      s.placeholders
        .height(column_height + 1)
        .css({
          top: '25px'
        }).find(".shadow").height(column_height-12).css({
          position: 'relative',
          top: '13px'
        });

      s.lis.wall_scroll();
    };

    s.update = function(event) {
      var data = s.settings.data,
          items = [],
          total = data.length,
          loaded = data.ids.length,
          desired_columns = Math.ceil(data.ids.length/s.settings.items_per_column),
          previous_item;

      // reset columns
      s.columns = {};
      s.wall.empty();

      console.log(data.length, data.ids.length,s.settings.items_per_column);
      for(var i in data.ids) {
        items.push(s.settings.template(data.items[i]));
      };
      
      /*
        Build columns
      */
      for(var i=0; i<desired_columns; i++) {
        var column = $('<div/>').html(s.settings.column_template()).contents();
        
        column.css({
          left: i * s.settings.column_width,
          width: s.settings.column_width,
          height: s.settings.column_height
        });

        s.wall.append(column);

        s.columns[i] = {
          el: column,
          left: i * s.settings.column_width,
          items: []
        }
      }
      

     
      //alert(desired_columns);
      for(var index in items){
        var column_index = Math.floor(index/s.settings.items_per_column),
            column = s.columns[column_index].el;

        $('.wall-column-box .content', column).append(items[index]);

        s.columns[column_index].items.push(index);
      };
      
      $('.wall-column-box .content', s.wall).off();
      $('.wall-column-box .content', s.wall).on('scroll', function scroll() {
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

      $('.wall-column-box.nano', s.wall).nanoScroller({alwaysVisible: true});
    
      // why ton't we draw some left-side shadow?
      
      
      s.trigger(s.events.change_status, {
        status:'updated'
      });

      s.resize();
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