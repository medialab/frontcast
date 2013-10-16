;(function() {
  'use strict';

  walt.domino.modules = walt.domino.modules || {};
  walt.domino.modules.Layout = function(controller) {
    domino.module.call(this);

    var _self = this,
        _lists = {
          documents: controller.addModule(walt.domino.modules.ListDocuments),
          assignments: controller.addModule(walt.domino.modules.ListAssignments),
          references: controller.addModule(walt.domino.modules.ListReferences)
        },
        blf_editor_is_enabled = false;

    this.enable_blf_editor = function(item) {
      blf_editor_is_enabled = true;

      blf.templates.override(
        'main',
        Handlebars.templates.blf_single_entry
      );

      var el = $("#d-" + item.id)
        .addClass('editor')
        .attr('data-override',true)
        .append( Handlebars.templates.reference_editor(item));

      blf.init({
        i18n:{
          lang: 'fr',
          url: walt.static_url + '/locales/__lng__/__ns__.json'
        },
        rpc:{
          before: function(params, xhr){
            xhr.setRequestHeader("X-CSRFToken", walt.CSRFTOKEN);
          }
        },
        baseURL: walt.urls.references,//http://localhost:8080',
        corpus: "forccast",
        baseDOM: el.find('#layout'),
        callbacks:{
          save: function(data) {
            walt.toast('saving...');
            _self.dispatchEvent('scene__update',{
              scene: walt.SCENE_DOCUMENT_VIEW,
              scene_args: {
                slug: item.slug
              }
            });
          },
          get_entry:function(data){
            if(data.result && data.result.length)
              blf.control.dispatchEvent('editEntry', { entry: data.result.pop() });
            else{
              // brand new reference (with a GIVEN rec_id)
              blf.control.dispatchEvent('openField', {field: 'ControversyVideo', entry: {
                title: item.title,
                rec_type: 'ControversyVideo',
                rec_id: item.reference
              }});
            }
            // resize 
            el.height(el[0].scrollHeight);
          }
        },
        onComplete: function() {
          if(item)
            blf.control.request('get_entry', { rec_id: item.reference });
          else
            blf.control.dispatchEvent('openField', { field: 'ControversyVideo' });
          
          $('#reference-editor').animate({
            left:0,
          });
        },
        advancedSearchPanel: {
          index: {
            property_source_index: 'search_index',
            property_source_operator: 'search_operator',
            default_operator: 'and',
            default_index: [
              'title',
              'author',
              'keyword'
            ]
          },
          filters: [
            {
              labels: {
                en: 'Publication year',
                fr: 'Année de publication'
              },
              property_start: 'filter_date_start',
              property_end: 'filter_date_end',
              type_ui: 'YearRangeField'
            },
            {
              labels: {
                en: 'Document types',
                fr: 'Types de document'
              },
              multiple: true,
              property: 'filter_types',
              type_source: 'document_type',
              type_ui: 'CheckboxField'
            },
            {
              labels: {
                en: 'Languages',
                fr: 'Langues'
              },
              multiple: true,
              property: 'filter_languages',
              type_source: 'language',
              type_ui: 'CheckboxField'
            }
          ]
        }
      });

    }
    
    this.disable_blf_editor = function() {
      if(!blf_editor_is_enabled)
        return;
      blf.control.kill();
      blf_editor_is_enabled = false;

    }


    this.enable_header = function() {
      $('header').show();
    }


    this.disable_header = function() {
      $('header').hide();
    }


    this.enable_editor = function(item) {
      var el = $("#d-" + item.id)
        .addClass('editor')
        .attr('data-override', true)
        .html( Handlebars.templates.document_editor(item));

      el.find('textarea').autosize();   
    }

    this.disable_editor = function(item) {

    }

    this.triggers.events.scene__synced = function(controller, event) {
      var scene = controller.get('scene'),
          collection,
          item;

      
      _self.disable_blf_editor();

      switch(scene){
        case walt.SCENE_SPLASH:
          
          break;
        case walt.SCENE_ME:
          _self.enable_header();
          break;

        case walt.SCENE_REFERENCE_EDIT:
          collection = controller.get('data_documents')
          item = walt.misc.first(collection.items);
          _self.disable_header();
          _self.enable_blf_editor(item);
          break;
        case walt.SCENE_DOCUMENT_EDIT:
          collection = controller.get('data_documents'),
          item = walt.misc.first(collection.items);
          _self.enable_editor(item);
          // enable blf editor the editor
          _self.disable_header();
          break;
      }

    };

  };

})();
