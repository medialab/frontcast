;(function($, undefined) {
  'use-strict'
  var walls = {},
      cursor = 0;

  var Cursor = function(){
    var self = this;

    this.column = -1; // current column index
    this.item = -1; // current item index
    this.length = 0; // current length

    this.update = function(property, value){
      self[property] = value;
    }
  };
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
      column_placeholders_template: Handlebars.templates.column_placeholders,

      view: 'wall',
      selected: 0,
      next: 1,
      prev: -1,
      column: 0
    };


    s.switch_view = function(event, view){
      s.settings.view = view;
      if(s.settings.view=='wall') {
        s.single.css('margin-top', -s.settings.column_height - 48);
      } else {
        s.navigate(event, s.selected_index);
        s.single.css('margin-top', 0);
      }
    }

    s.update_info = function(event){
      s.wall_index.text(s.selected_index + 1);
      s.wall_total.text(s.settings.data.length);
      s.wall_cursor.animate({
        left: (s.selected_index/s.settings.data.length)*100 + '%',
        width: Math.max(2, 100/s.settings.data.length )+ '%',
      },{
        queue:false
      });
    }

    /*
      visualize selected item in single view
    */
    s.navigate = function(event, index){
      s.single.empty().append(s.items[index]);
    }


    s.columns = {};
    s.items = [];
    s.selected_index = -1;
    s.selected_column = -1;

    s.lis = {}; // collection of mouse listeners
    s.timers = {}; //timeout vars 

    s.events = {
      change_status: 'wall_change_status',
      update: 'wall_update',
      set_property: 'wall_set_property',
      get_propery: 'wall_get_property',
      resize: 'wall_resize',
      change_cursor: 'wall_change_cursor',
      switch_view: 'switch_view',
      update_info: 'update_info',
      select: 'wall_select'
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

    s.cursor = new Cursor();

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


    s.select = function(event, index){
      if(!s.settings.data.ids[index])
        return;
      var item = $(s.settings.item_id_prefix + ''+s.settings.data.ids[index]),
          column = item.closest('.wall-column'),
          column_cursor = column.index(),
          item_cursor =  index,
          t = item.position().top;
      
      s.selected_item = item;

      if(s.selected_index == -1)
        item.addClass('active')
      else if(s.selected_index != item_cursor) {
        $(s.settings.selector + '.active', s.wall).removeClass('active');
        item.addClass('active');
      }
      s.selected_index = item_cursor;

      s.selected_next_index = item_cursor+1;
      s.selected_prev_index = item_cursor+1;

      if(s.selected_column == -1){
        walt.log(column_cursor)
        s.columns[column_cursor].el.addClass('active');
      }else if(column_cursor != s.selected_column){
        s.columns[column_cursor].el.addClass('active');
        s.columns[s.selected_column].el.removeClass('active');
        walt.verbose(  'chanced', column_cursor);
      }

      s.selected_column = column_cursor;
      s.trigger('update_info');

      if(s.settings.view == 'single')
        s.navigate(event, s.selected_index);
      
      // scroll left
      //if( item.position().top > s.settings.column_height){
      if(s.columns[column_cursor].left + s.settings.column_width - s.wall.scrollLeft() > s.wall_width || s.columns[column_cursor].left < s.wall.scrollLeft())
        $(".wall").animate({
          'scrollLeft':s.columns[column_cursor].left-s.wall_width/2+s.settings.column_width/2
        },{
          queue: false
        });
      
     
      if( t > s.settings.column_height - 48 || t < 0){
        column.find('.content').animate({
          scrollTop: t < 0? 0 : t-s.settings.column_height/2
        },{
          queue: false
        })
      }
    

    }

    s.previous = function(event){
      s.settings.data.ids[s.selected_index - 1] && s.select(event, s.selected_index - 1);

    };

    s.next = function(event){
      s.settings.data.ids[s.selected_index + 1] && s.select(event, s.selected_index + 1);
    };

    s.init = function(el, options) {
      s.el = el;
      /*
        dom elements
      */
      s.wall = $('<div/>',{
        "class": "wall"
      }).css({
        position: 'relative',
        width: '100%',
        'overflow-y': 'hidden',
        'overflow-x': 'scroll'
      });

      s.single = $('<div/>',{
        'class': 'wall-single'
      });
      
      s.el.empty()
        .css({position: 'relative', overflow: 'hidden'})
        .append(s.single)
        .append(s.wall);
      
      s.wall_index = $('#wall-index');
      s.wall_total = $('#wall-total');
      s.wall_cursor = $('#wall-cursor')/*.pep({
        axis: "x",
        easeDuration: 500,
        constrainTo: 'parent'
      });*/

      s.wall.scroll(s.lis.wall_scroll);
      s.wall.on('click', s.settings.selector, function(event){
        
        var id = $(this).attr('data-id');
        s.select(event, s.settings.data.ids.indexOf(id));
        
        if($(this).hasClass('active'))
          s.switch_view(event,'single');

      });

      $('#wall-switch-to-list').on('click', function(event){
        s.switch_view(event, 'wall');
      });
      

      $('#wall-previous').on('click', s.previous);

      $('#wall-next').on('click', s.next);
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
      s.single.height(column_height + 48).css('margin-top', -column_height - 48);
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
          total = data.length,
          loaded = data.ids.length,
          desired_columns = Math.ceil(data.ids.length/s.settings.items_per_column),
          previous_item;

      // reset columns
      s.columns = {};
      s.items = [];
      s.selected_index = -1;
      s.selected_column = -1;
      s.wall.empty();

      // reset selected_index

      for(var i in data.ids) {
        s.items.push(s.settings.template(data.items[i]));
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
      for(var index in s.items){
        var column_index = Math.floor(index/s.settings.items_per_column),
            column = s.columns[column_index].el;

        $('.wall-column-box .content', column).append(s.items[index]);

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
      debugger
      s.select(event,0);
      s.update_info();

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