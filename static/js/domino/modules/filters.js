/*
  Search / filter implementation
*/
;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Filters = function() {
    domino.module.call(this);

    var _self = this,
        input,
        glo = $('#counter-documents-global'),
        footer = $('footer'),
        active_filters = $('#active-filters'),
        facets_loaded = false,
        filters_loaded = false,
        handlers ={ };


    

    handlers.set_property = function(event){
      // respond to click on el like: <span class="type" data-slug="ControversyWeb" data-filter="type__in">ControversyWeb</span>
      var slug = $(this).attr('data-slug'),
          scene_params = $.extend({}, walt.domino.controller.get('scene_params')),
          filter = $(this).attr('data-filter');

      if(!filter){
        walt.error('(Filters) .set_property filter var not defined');
        return;
      };

      walt.log('(Filters) .set_property  "', filter, '":["', slug, '"]', scene_params);

      // setting filters accurately
      scene_params.filters = scene_params.filters || {};
      if(scene_params.filters[filter] && typeof scene_params.filters[filter] == 'object')
        scene_params.filters[filter].indexOf(slug) == -1 && scene_params.filters[filter].push(slug);
      else
        scene_params.filters[filter] = [slug];
      walt.verbose('... .set_property, scene_params.filters modified:', scene_params.filters);

      _self.send_args(scene_params);
    };


    handlers.remove_value = function(event) {
      var item = $(this).closest('[data-filter]'),
          filter = item.attr('data-filter'),
          slug = item.attr('data-slug'),
          scene_params = $.extend({}, walt.domino.controller.get('scene_params'));
      
      console.log("%c FILTERS REMOVE VALUE", walt.STYLE_CONSOLE_SERVICES, filter, slug)

      if(scene_params.filters && scene_params.filters[filter]){
         console.log("%c FILTERS REMOVE VALUE", walt.STYLE_CONSOLE_SERVICES, scene_params.filters[filter])
        if(typeof scene_params.filters[filter] == 'object'){
          var index = scene_params.filters[filter].indexOf(slug);
          console.log("%c FILTERS REMOVE VALUE", walt.STYLE_CONSOLE_SERVICES, index)

          index !== -1 && scene_params.filters[filter].splice(index, 1);
          console.log("%c FILTERS REMOVE VALUE", scene_params.filters)
          
          if(scene_params.filters[filter].length == 0)
            delete scene_params.filters[filter]

        };

      }
      _self.send_args(scene_params);
    }

    handlers.remove_property = function(event) {
      var filter = $(this).closest('[data-filter]'),
          scene_params = $.extend({}, walt.domino.controller.get('scene_params'));

          };



    handlers.remove_query = function(event) {
      var scene_params = $.extend({}, walt.domino.controller.get('scene_params'));

      scene_params.search = "";

      _self.send_args(scene_params);
    }

    handlers.toggle_filters = function(event) {
      footer.toggleClass('opened');
    }

    handlers.open_filters = function(event) {
      footer.addClass('opened');
    }

    handlers.close_filters = function(event) {
      footer.removeClass('opened');
    }

    this.send_args = function(scene_params) {
      var scene = walt.domino.controller.get('scene'),
          scene_args = $.extend({}, walt.domino.controller.get('scene_args'));

      walt.verbose('(Filters) .send_args received', scene_params);
      scene_args.params = {};
      scene_args.params.filters = JSON.stringify(scene_params.filters);
      scene_args.params.search = scene_params.search;
      walt.verbose('... .send_args outputting:', scene_args.params.filters,scene_args);

      _self.dispatchEvent('scene_args__update', {
        scene_args: scene_args
      });
      
      _self.dispatchEvent('scene__update', {
        scene: scene
      });
    };


    this.triggers.events.scene_params__updated = function(controller) {
      var scene_params = controller.get('scene_params'),
          has_filters = false;


      // clean filters
      active_filters.empty();
      if(scene_params.search && scene_params.search.length){
        active_filters.append(
            $('<span/>',{
              'class': 'property query',
              'data-query': scene_params.search
            }).html('<span class="special">SEARCH</span> "' + scene_params.search + '"<i class="fa fa-times-circle remove-query"></i>')
          );
        has_filters = true;
      }

      for (var i in scene_params.filters){
        var exempla = scene_params.filters[i],
            classname = i.split("__").shift();

        for(var j in exempla){
          active_filters.append(
            $('<span/>',{
              'class': 'property ' + classname,
              'data-slug': exempla[j],
              'data-filter': i
            }).html(exempla[j] + '<i class="fa fa-times-circle remove-value"></i>')
          );
        };

        has_filters = true;
      };
      
      if(has_filters)
        handlers.open_filters();
      else
        handlers.close_filters();


    };


    this.triggers.events.data_documents_filters__updated = function(controller) {
      filters_loaded = true;
      if(!facets_loaded)
        return; // ignore if facets haven't been initialized yet


      var data_documents_filters = controller.get('data_documents_filters');
      
      $('.facets').each(function(i,e) {
        var wrapper = $(this),
            types = wrapper.attr('data-facet').split('.'),
            data;

        if(!types.length)
          return;
        else if(types.length>1)
          data = data_documents_filters[types[0]][types[1]]; // UGLY!!!!!! I know, I know...
        else
          data = data_documents_filters[types[0]];


        wrapper.find('[data-slug]').each(function(i,e) {
          var item = $(this),
              slug = item.attr('data-slug'),
              value = item.find('.bar-value'),
              count = item.find('.count'),
              maximum = item.attr('data-maximum');

          //console.log(slug, data, maximum, data[slug].count);
          if(data && data[slug]){
            value.css({
              height: ((data[slug].count*33/maximum) + 3) + 'px'
            });
            count.text(data[slug].count).css({
              bottom: ((data[slug].count*33/maximum) + 3) + 'px',
              opacity: 1
            });
          } else {
            value.css({
              height: '1px',
              
            })
            count.text('0').css({
              bottom: '1px',
              opacity: 0
            });
          }
        })

      });
     
    };

    this.triggers.events.data_documents_facets__updated = function(controller) {
      var data_documents_facets = controller.get('data_documents_facets');

      //alert('facets');
      walt.verbose('(Filters) listens to data_documents_facets__updated', data_documents_facets);
      glo.text(data_documents_facets.total_count);

      // evaluate facets
      $('.facets').each(function(i,e) {
        var wrapper = $(this),
            types = wrapper.attr('data-facet').split('.'),
            type,
            data,
            max = 0,
            facet,
            facets = [],
            _facets = [];

        if(!types.length)
          return;
        else if(types.length>1)
          data = data_documents_facets[types[0]][types[1]]; // UGLY!!!!!! I know, I know...
        else
          data = data_documents_facets[types[0]];

        if(!data)
          return;

        type = types[0];

        // get max value
        for(var i in data) {
          max = Math.max(data[i].count, max);
          facets.push({
            type: type ,
            label: i,
            count: data[i].count
          });
        };

        if(facets.length == 0)
          return
        // todo sorting according to a function
        facets.sort();

        for(var i in facets){
          facet = facets[i];
          facet.step = 100/facets.length;
          facet.max = max;
          facet.value = facet.count*100/max; // box value
          facet.global = facet.count*100/max; // box hsadow value
          facet.filter = type + "__slug__REDUCE";
          facet.slug = facet.label;
          _facets.push(Handlebars.templates.facet(facet));
        }

        wrapper.append(_facets.join(''));
      });
      
      facets_loaded = true;
      if(filters_loaded) // filters loaded before facets (async problem we don't mean to solve now)
        _self.triggers.events.data_documents_filters__updated(controller);
    };


    this.triggers.events.init = function(controller) {
      walt.verbose('(Filters) listens to init');
      // REMOVED ! $(document).on('click', '.tag', handlers.set_property);
      // REMOVED ! 
      $(document).on('click', '.set-property', handlers.set_property);
      $(document).on('click', '.remove-value', handlers.remove_value);
      $(document).on('click', '.remove-query', handlers.remove_query);
      
      $(".toggle-filters", footer).on('click', handlers.toggle_filters);
    };


  };

})();
