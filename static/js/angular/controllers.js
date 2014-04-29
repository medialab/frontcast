'use strict';

/* Controllers */
var CONTROLLER_STATUS_AVAILABLE = 'available',
    CONTROLLER_STATUS_WORKING = 'busy',
    CONTROLLER_PARAMS_UPDATED = "CONTROLLER_PARAMS_UPDATED",

    STYLE_INFO = 'color: #b8b8b8';


angular.module('walt.controllers', [])
  /*
    
    The very main controller. Handle filters.
    ===

  */
  .controller('layoutCtrl', ['$scope', '$rootScope','$location', '$route', function($scope, $rootScope, $location, $route) {
    $scope.filters = {};
    $scope.query = "";
    
    $scope.limit = 10;
    $scope.offset = 0;
    $scope.default_limit = 10;
    $scope.default_offset = 0;
    $scope.total_count = 0;

    $scope.page = 0;
    $scope.numofpages = 0;
    $scope.pages = [];

    $scope.viewname = 'overview';

   


    $scope.pageto = function(page) {
      var page = Math.max(0, Math.min(page, $scope.numofpages));
      console.log('page to', page);
      $scope.offset = page * $scope.limit;
      $scope.loadFilters();
    };


    $scope.nextPage = function() {
      $scope.pageto(+$scope.page + 1);
    };
            

    $scope.prevPage = function() {
      $scope.pageto(+$scope.page - 1);
    };



    $scope.paginate = function(options) {
      var options = options || {},
          pages = [],
          left = 0,
          right = 0;

      $scope.total_count = options.total_count;
      
      
      $scope.numofpages = Math.floor($scope.total_count / $scope.limit );
      $scope.page = Math.floor($scope.offset / $scope.limit);

      if($scope.numofpages < 10) {
        left = 0;
        right = +$scope.numofpages;
      } else{
        right = Math.min($scope.numofpages, $scope.page<10?10:$scope.page + 5);
        left = right - 10;
      }

      for(var i=left; i<right+1; i++)
        pages.push(i+1);

      $scope.pages = pages;
      console.log('$scope.paginate', pages);
    }

    $scope.follow = function(link) {
      //alert(link)
      var path = Array.prototype.slice.call(arguments).join('/').replace(/\/+/g,'/');
      $location.path(path);
    }
    
    $scope.search = function() {
      console.log("%c search ", 'color:white; background-color:#383838', $scope.query);
      $scope.limit = $scope.default_limit;
      $scope.offset = $scope.default_offset;
      $location.search({
        'search': $scope.query
      });
    }

    $scope.selected = undefined;
    $scope.states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Dakota', 'North Carolina', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'];

    $scope.typeaheadOpts = {
      templateUrl: 'bower_components/bootstrap/template/typeahead/typeahead-popup.html'
    };

    $scope.switchOrderby = function(o) {
      console.log($scope);
      $scope.orderby = o;
    }

    $scope.loadFilters = function(options) {
      var candidates = $location.search().filters,
          query = $location.search().search;

      if(query) {
        $scope.query = query;
      };

      if(candidates) {
        try{
          var filters = JSON.parse(candidates);
          $scope.filters = filters;
        } catch(e){
          console.log("%c! filters failed ", 'color:white; background-color:crimson', e.message);
          
        }
      } else {
        $scope.filters = {};
      }

      console.log("%c loading filters ", 'color:white; background-color:green', 'query:',$scope.query, $scope.offset, $scope.limit);   
      $scope.$broadcast(CONTROLLER_PARAMS_UPDATED, options);
    };

    $rootScope.$on('$routeUpdate', function(e, r){
      console.log("%c route updated", STYLE_INFO);
      $scope.loadFilters({controller: r.$$route.controller}); // push current controllername
    });

    $rootScope.$on('$routeChangeSuccess', function(e, r){
      console.log("%c    route change success", STYLE_INFO);
      $scope.filters = {};
      $scope.limit = $scope.default_limit;
      $scope.offset = $scope.default_offset;
      $scope.query = $location.search().search;
    });
    
    $scope.setViewName = function(viewname) {
      $scope.viewname = viewname;
    };


    // commont filter propertiues here
    $scope.setProperties = function(property, value) {
      $scope.filters[property] = [value];
      console.log('%c filters setProperties', STYLE_INFO, property, value, $scope.filters);
      $scope.limit = $scope.default_limit;
      $scope.offset = $scope.default_offset,
        
      $location.search({
        'filters': JSON.stringify($scope.filters)
      });
    };


    $scope.setProperty = function(property, value) {
      $scope.filters[property] = value;
      console.log('%c filters setProperty', 'background: crimson; color: white',property, value, $scope.filters);
      $location.search('filters', JSON.stringify($scope.filters))
    };


    $scope.removeProperty = function(property, value) {
      console.log('removing', property, value, 'from filters');
      delete $scope.filters[property];
      $location.search({
        'filters': JSON.stringify($scope.filters)
      });
    }


    $scope.extendFilters = function(filter) {
      var filters = angular.extend({}, $scope.filters, filter);
      return JSON.stringify(filters)
    };

    console.log('%c layoutCtrl ', 'background: #151515; color: white', $scope.filters);
    $scope.loadFilters();

  }])
  /*
    
    View related controllers
    ===

  */
  .controller('overviewCtrl', ['$scope', function($scope){
    console.log('%c overviewCtrl ', 'background: gold;');
  }])

  /*
    
    Document List controller.
    ===

  */
  .controller('documentsCtrl', ['$scope', 'DocumentListFactory', function($scope, DocumentListFactory){
    $scope.setViewName('documents');

    $scope.sync = function() {
      DocumentListFactory.query({search: $scope.query, limit:$scope.limit, offset:$scope.offset, filters: $scope.filters}, function(data){
        $scope.items = data.objects;
        $scope.paginate({
          total_count: data.meta.total_count
        });
      });
    };

    $scope.$on(CONTROLLER_PARAMS_UPDATED, function(e, options) {
      console.log('received...');
      $scope.sync();
    });

    $scope.sync();
    console.log('%c documentsCtrl ', 'background: lime;');
  }])


  .controller('documentProfileCtrl', ['$http', '$scope', '$routeParams', 'DocumentFactory', 'WorkingDocumentFactory', 'DocumentProfileFactory', 'DeviceFactory', 'DeviceListFactory', function($http, $scope, $routeParams, DocumentFactory, WorkingDocumentFactory, DocumentProfileFactory, DeviceFactory, DeviceListFactory){
    $scope.setViewName('documents');

    $scope.document_types = [
      {value: 'ControversyWeb', text: 'ControversyWeb'},
      {value: 'ControversyVideo', text: 'ControversyVideo'},
      {value: 'Ebook', text: 'Ebook'}
    ]; 

    $scope.sync = function() {
      DocumentFactory.get({id: $routeParams.id}, function(data){
        $scope.document = data.object;
        console.log(data);
      });
      DocumentProfileFactory.get({id: $routeParams.id}, function(data){
        $scope.profile = data.object;
        console.log(data);
      });
    };


    $scope.updateDocument = function(field, value) {
      console.log('%c documentProfileCtrl.updateDocument ', 'background: lime;', field, value);
      var params = {};
      params[field] = value;
      return DocumentFactory.update({id: $routeParams.id}, params, function(data){
        $scope.document = data.object;
        console.log(data);
      });
    }


    $scope.removeDevice = function(device_id) {
      if (confirm('are you really sure')){
        DeviceFactory.delete({id: device_id}, function(res){
          console.log(res);
        });
        $scope.sync();
      }
      
    }

    $scope.saveDevice = function(device_type, doc) {
      
      DeviceListFactory.save({}, {
        type: device_type,
        document: $routeParams.id,
        working_document: doc.id
      }, function(res){

        console.log(res, $scope.document.devices);
        var is_already_in_place = false;
        if($scope.document.devices[device_type]) {
          for (var d in $scope.document.devices[device_type]) {
            console.log("compare ", d, doc)
            if($scope.document.devices[device_type][d].slug == doc.slug){
              is_already_in_place = true;
              break;
            }
          };
          !is_already_in_place && $scope.document.devices[device_type].push(doc)
        } else
          $scope.document.devices[device_type] = [doc];
      })

      return "";
    }

    $scope.getLocation = function(val) {
      var suggestions = WorkingDocumentFactory.query({
        limit:5,
        filters: JSON.stringify({
          type:'T'
        }),
        search: val
      });
      
      return suggestions.$promise.then(function (result) {
        console.log(result);
        var titles = [];
        angular.forEach(result.objects, function(item){
          titles.push(item);
        });
        console.log(titles);
        return titles;
      });
    };

    $scope.sync();
    console.log('%c documentProfileCtrl ', 'background: lime;');
  }])

  

  /*
    
    WorkingDocument List of type tool controller.
    ===

  */
  .controller('toolsCtrl', ['$scope', 'WorkingDocumentListFactory', function($scope, WorkingDocumentListFactory){
    $scope.setViewName('tools');

    $scope.orders = [
      {label:'black', value:'dark'},
      {label:'white', value:'light'}
    ];
    $scope.orderby = $scope.orders[1];

    $scope.sync = function() {
      WorkingDocumentListFactory.query({search: $scope.query, limit:$scope.limit, offset:$scope.offset, filters: $scope.extendFilters({type: 'T'})}, function(data){
        $scope.items = data.objects;
        $scope.paginate({
          total_count: data.meta.total_count
        });
      });
    };

    $scope.$on(CONTROLLER_PARAMS_UPDATED, function(e, options) {
      console.log('received...', $scope.offset, $scope.limit);
      $scope.sync();
    });

    $scope.sync();
    console.log('%c toolsCtrl ', 'background: lime;');
  }])
  .controller('toolCtrl', ['$scope', '$route', '$routeParams', 'WorkingDocumentFactory',function($scope, $route, $routeParams, WorkingDocumentFactory){
    $scope.status = CONTROLLER_STATUS_AVAILABLE;
    $scope.setViewName('tool');
    console.log('%c toolCtrl ', 'background: lime;', $routeParams.id, $routeParams);
    
    WorkingDocumentFactory.get({id: $routeParams.id}, function(data){
      $scope.item = data.object;
      console.log(data);
    });

  }])
  /*
    
    WorkingDocument List of type tool controller.
    ===

  */
  .controller('coursesCtrl', ['$scope', 'WorkingDocumentListFactory', function($scope, WorkingDocumentListFactory){
    $scope.setViewName('courses');

    $scope.sync = function() {
      WorkingDocumentListFactory.query({
        search: $scope.query,
        limit: $scope.limit,
        offset: $scope.offset,
        filters: $scope.extendFilters({
          type__in: ['course_secondary_school', 'course_master', 'course_phd', 'course']
        })}, function(data) {
        $scope.items = data.objects;
        $scope.paginate({
          total_count: data.meta.total_count
        });
      });
    };

    $scope.$on(CONTROLLER_PARAMS_UPDATED, function(e, options) {
      console.log('received...', $scope.offset, $scope.limit);
      $scope.sync();
    });

    $scope.sync();
    console.log('%c coursesCtrl ', 'background: lime;');
  }])
  .controller('courseCtrl', ['$scope', '$route', '$routeParams', 'WorkingDocumentFactory',function($scope, $route, $routeParams, WorkingDocumentFactory){
    $scope.status = CONTROLLER_STATUS_AVAILABLE;
    $scope.setViewName('courses');
    console.log('%c courseCtrl ', 'background: lime;', $routeParams.id, $routeParams);
    
    WorkingDocumentFactory.get({id: $routeParams.id}, function(data){
      $scope.item = data.object;
      console.log(data);
    });

  }])
  /*
    
    Filters and co.
    ===

  */
  .controller('filtersCtrl', ['$rootScope', '$scope', '$routeParams', '$location', function($rootScope, $scope, $routeParams, $location) {
    
  }])
  /*

    Handle header search and menu enlightment
    ===

  */
  .controller('headerCtrl', ['$rootScope', '$scope', '$location', function($rootScope, $scope, $location){
    // $scope.$on('$locationChangeSuccess')
    $rootScope.query = "";

    $scope.search = function(){
      $rootScope.query = $scope.query;
      $location.search('search', $rootScope.query);
    }
  }])
  /*

    Show the list of all types of working document !
    ===

  */
  .controller('indexCtrl', ['$rootScope', '$routeParams', '$scope', 'WorkingDocumentFactory', function($rootScope, $routeParams, $scope, WorkingDocumentFactory) {
    $scope.sequences = {};
    $scope.tasks = {};
    $scope.tools = {};
    $scope.others = {};

    try{
      $rootScope.filters = angular.extend({}, JSON.parse($routeParams.filters || "{}"));
    } catch(e){
      console.log('%c >> filter has been ignored, exception message: "' + e.message +'"','background: gold; color: #cc1600; line-height:5em');
      $rootScope.filters = {};
    }

    try{
      $rootScope.query = $routeParams.search;
    } catch(e){
      console.log('%c >> query param has been ignored, exception message: "' + e.message +'"','background: gold; color: #cc1600; line-height:5em');
      $rootScope.query = "";
    }

    console.log('%c load filters ', 'background: #151515; color: white', $rootScope.filters);
    console.log('%c load search query ', 'background: #151515; color: white', $rootScope.query);

    WorkingDocumentFactory.query({search: $rootScope.query, filters:$scope.extendFilters({type: 'B'})}, function(data){
      $scope.sequences = data;
      console.log(data);
    });

    WorkingDocumentFactory.query({search: $rootScope.query, filters: $scope.extendFilters({type: 'I'})}, function(data){
      $scope.tasks = data;
      console.log(data);
    });

    WorkingDocumentFactory.query({search: $rootScope.query, filters: $scope.extendFilters({type: 'T'})}, function(data){
      $scope.tools = data;
      console.log(data);
    });

    WorkingDocumentFactory.query({search: $rootScope.query, filters: $scope.extendFilters({type: '?'})}, function(data){
      $scope.others = data;
      console.log(data);
    });
  }])
  /*

    Edit the abstrac and the tags of a working document 
    ===

  */
  .controller('workingdocumentEditCtrl', ['$scope', '$routeParams', 'WorkingDocumentFactory', 'WorkingDocumentTagsFactory', 'URLFactory', function($scope, $routeParams, WorkingDocumentFactory, WorkingDocumentTagsFactory, URLFactory) {
    $scope.workingdocument = {};
    $scope.csv_tags = '';
    $scope.status = CONTROLLER_STATUS_WORKING; // first loading data

    WorkingDocumentFactory.query({id: $routeParams.id}, function(data){
      $scope.workingdocument = data.object;
      $scope.csv_tags = $scope.workingdocument.tags.map(function(i){return i.name}).join(', ')
      $scope.status = CONTROLLER_STATUS_AVAILABLE
    });

    $scope.addTodo = function(){
      if($scope.status != CONTROLLER_STATUS_AVAILABLE)
        return;
      $scope.status = CONTROLLER_STATUS_WORKING;

      // attach stuff
      WorkingDocumentTagsFactory.save({id: $routeParams.id}, {
        type: 'Ke',
        tags: $scope.csv_tags
      }, function(data){

        WorkingDocumentFactory.save({id: $routeParams.id},{abstract: $scope.workingdocument.abstract_raw}, function(data){
          console.log('Service%c success','color:green', 'status:',data.status)
          console.log(data)
          $scope.workingdocument = data.object;
          $scope.csv_tags = $scope.workingdocument.tags.map(function(i){return i.name}).join(', ')
          $scope.status = CONTROLLER_STATUS_AVAILABLE;
        })
      });
    }
  }])
  /*

    Create a working document form a bookmark, directly    
    ===

  */
  .controller('workingdocumentCreateCtrl', ['$scope', '$location', 'WorkingDocumentListFactory', 'URLFactory', function($scope, $location, WorkingDocumentListFactory, URLFactory) {
    
    var permalink = 'ciao'
    $scope.button = {
      text: 'add',
      disabled: false
    };

    $scope.status = {
      icon: 'fa-check grey',
      disabled: false
    };

    $scope.addTodo = function(){
      // check permalink, then save
      $scope.button.disabled = true;
      $scope.button.text = 'checking...'
      $scope.status.icon = 'fa-spinner';
      $scope.status.disabled = true
      // blablablab
      // check permalink, then save
      // http://www.pitchinteractive.com/beta/index.php
      URLFactory.query({url: $scope.permalink}, function(data) {
        $scope.status.icon = 'fa-check';
        $scope.button.text = 'saving...';

        if(data.object && data.object.title)
          WorkingDocumentListFactory.save({
            title:data.object.title,
            permalink:$scope.permalink,
            rating: 0,
            type:'?'
          }, function(data){
            console.log('data', data);
            $location.path('/w/'+data.object.id+'/edit')
          });
        else {
          alert('ouch, do it again. Url is not valid ?');
          $scope.status.disabled = false;
        }
      });

      /*WorkingDocumentListFactory.create({}, function(data){
        console.log('data', data);
      })*/
      //$location.path('corpusCtrl')
    }
  }]);