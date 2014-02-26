;(function(window, jQuery, domino, undefined) {
  'use strict';

  window.walt = window.walt || {};
  walt.domino = walt.domino || {};

  /*

        Services
        ========

        How to test services:
        var d = walt.domino.controller;
        d.request('service_name',{offset:10, limit:20, query:'query search'})

        service types: get, create, modify, remove

      */
  walt.domino.services = [
    { 
      id: 'get_document',
      type: 'GET',
      url: walt.urls.document,
      dataType: 'json',
      data: function(input) {
        return input.params;
      },
      success: function(data) {
        var items = {};
        
        this.dispatchEvent('data__update', {
          data_documents: {
            items: [data.object],
            ids: [''+data.object.id],
            length: 1,
            limit: 1,
            offset: 0,
            order_by: []
          }
        });
      }
    },
    { 
      id: 'get_documents',
      type: 'GET',
      url: walt.urls.documents,
      dataType: 'json',
      data: function(input) {
        walt.log('(Service) launch "get_documents"', input);
        return input.params;
      },
      success: function(data) {
        // todo infinite adding not replacing items.
        walt.log('(Service) success "get_documents"', data.status);
        this.dispatchEvent('data__update', {
          data_documents: {
            items: data.objects,
            ids:$.map(data.objects, function(e){return ''+e.id;}),
            length: +data.meta.total_count,
            limit: +data.meta.limit || data.objects.length,
            offset: data.meta.offset || 0,
            order_by: data.meta.order_by || []
          }
        });
      }
    },
    { 
      id: 'get_documents_filters',
      type: 'GET',
      url: walt.urls.documents_filters,
      dataType: 'json',
      data: function(input) {
        console.log('%c (Service) ', walt.STYLE_CONSOLE_SERVICES, 'launch "get_documents_filters" with input', input);
        return input.params;
      },
      success: function(data, params) {
        console.log('%c (Service) ', walt.STYLE_CONSOLE_SERVICES, 'success "get_documents_filters"', data.status);
        this.update('data_documents_filters', data.objects);
      }
    },
    { 
      id: 'get_documents_facets',
      type: 'GET',
      url: walt.urls.documents_filters,
      dataType: 'json',
      data: function(input) {
        console.log('%c (Service) ', walt.STYLE_CONSOLE_SERVICES, 'launch "get_documents_facets" with input', input);
        return input.params;
      },
      success: function(data, params) {
        console.log('%c (Service) ', walt.STYLE_CONSOLE_SERVICES, 'success "get_documents_facets"', data.status);
        if(data.status == walt.API_OK)
          this.update('data_documents_facets', data.objects);     
        else
          this.dispatchEvent('service__error', data.error);
      }
    },
    { 
      id: 'get_documents_graph',
      type: 'GET',
      url: '/api/graph/bipartite/document/tags/',
      dataType: 'json',
      data: function(input) {
        console.log('%c (Service) ', 'color:#3887BE;background-color:gold', ' launch "get_documents_graph"', input);
        return input.params;
      },
      success: function(data, params) {
        console.log('%c (Service) ', walt.STYLE_CONSOLE_SERVICES, 'success "get_documents_graph"', data);
        
        this.update({data_documents_graph: {
          nodes: data.nodes,
          edges: data.edges
        }});

        this.dispatchEvent('data__update', {
          data_documents: {
            items: [],
            ids: [],
            limit: 0,
            offset: 0,
            length: 0,
            order_by: [],
          }
        });
      }
    },
    /*
      
      Non WALTY endpoints
      ===================

      BIBLIB references, vimeo oembed endpoint etc...

    */
    {
      id: 'get_references',
      url: walt.urls.references, 
      type: walt.rpc.type,
      error: walt.rpc.error,
      expect: walt.rpc.expect,
      contentType: walt.rpc.contentType,
      before: function(params, xhr){
        xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);
      },
      async: true,
      data: function( input ) { // input={params:{method:'citation_by_rec_ids', params:[]}}
        walt.log('(Service) launch "get_references"', input);
         return walt.rpc.buildData( input.params.method, input.params.params);
      },
      success: function(data, params) {
        walt.log('(Service) success "get_references"', data);
        if(data.result) {
          var ids = data.result.map(function(i){return i.rec_id}),
              items = {};

          if(ids.length) {
            for(var i in data.result) {
              items[data.result[i].rec_id] = data.result[i];
            };

            this.update({
              data_references: {
                items: items,
                ids: ids
              }
            });
          };
        };
      }
    },
    {
      id: 'get_metadata',
      url: walt.urls.references, 
      type: walt.rpc.type,
      error: walt.rpc.error,
      expect: walt.rpc.expect,
      contentType: walt.rpc.contentType,
      before: function(params, xhr){
        xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);
      },
      async: true,
      data: function( input ) { // input={params:{method:'citation_by_rec_ids', params:[]}}
        walt.log('(Service) launch "get_metadata"', input);
         return walt.rpc.buildData( input.params.method, input.params.params);
      },
      success: function(data, params) {
        walt.log('(Service) success "get_metadata"', data);
        
      }
    }
  ];
})(window, jQuery, domino);