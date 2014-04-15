'use strict';

/* Controllers */
var CONTROLLER_STATUS_AVAILABLE = 'available',
    CONTROLLER_STATUS_WORKING = 'busy',
    CONTROLLER_PARAMS_UPDATED = "CONTROLLER_PARAMS_UPDATED";

angular.module('walt.controllers', [])
  /*
    
    The very main controller. Handle filters.
    ===

  */
  .controller('layoutCtrl', ['$scope', '$rootScope','$location', '$route', function($scope, $rootScope, $location, $route) {
    $scope.filters = {};
    $scope.query = "";
    $scope.limit = 25;
    $scope.offset = 0;
    $scope.default_limit = 25;
    $scope.default_offset = 0;

    $scope.loadFilters = function(options) {
      var candidates = $location.search().filters,
          limit = +$location.search().limit,
          offset = +$location.search().offset;

      if(candidates) {
        try{
          var filters = JSON.parse(candidates);
          $scope.filters = filters;
        } catch(e){
          console.log("%c! filters failed ", 'color:white; background-color:crimson', e.message);
          
        }
      } else
        $scope.filters = {};

      $scope.limit = isNaN(limit)? $scope.default_limit: limit;
      $scope.offset = isNaN(offset)? $scope.default_offset: offset;
      // limit and offset here
      console.log("%c filters ", 'color:white; background-color:green', $scope.limit, $scope.offset);
          
      $scope.$broadcast(CONTROLLER_PARAMS_UPDATED, options);
    };

    $rootScope.$on('$routeUpdate', function(e, r){
      console.log("%c! route updated ", 'color:white; background-color:crimson', e.message);
          
      $scope.loadFilters({controller: r.$$route.controller}); // push current controllername
    });

    

    // commont filter propertiues here
    $scope.setProperties = function(property, value) {
      $scope.filters[property] = [value];
      console.log('%c filters setProperties', 'background: crimson; color: white',property, value, $scope.filters);
      $location.search('filters', JSON.stringify($scope.filters))
    };

    $scope.setProperty = function(property, value) {
      $scope.filters[property] = value;
      console.log('%c filters setProperty', 'background: crimson; color: white',property, value, $scope.filters);
      $location.search('filters', JSON.stringify($scope.filters))
    };

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



  .controller('toolsCtrl', ['$scope', 'WorkingDocumentListFactory', function($scope, WorkingDocumentListFactory){
    $scope.name = 'tools';

    $scope.sync = function() {
      WorkingDocumentListFactory.query({search: $scope.query, limit:$scope.limit, offset:$scope.offset, filters: $scope.extendFilters({type: 'T'})}, function(data){
        $scope.items = data.objects;
        console.log(data);
      });
    };

    $scope.$on(CONTROLLER_PARAMS_UPDATED, function(e, options) {
      console.log('received...');
      $scope.sync();
    });

    $scope.sync();
    console.log('%c toolsCtrl ', 'background: lime;');
  }])



  .controller('toolCtrl', ['$scope', '$route', '$routeParams', function($scope, $route, $routeParams){
    $scope.status = CONTROLLER_STATUS_AVAILABLE;

    console.log('%c toolCtrl ', 'background: lime;', $routeParams.id, $routeParams);


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