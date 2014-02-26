'use strict';

angular.module('d3', [])
  .factory('d3Service', ['$document', '$q', '$rootScope',
    function($document, $q, $rootScope) {
      var d = $q.defer();
      function onScriptLoad() {
        // Load client in the browser
        $rootScope.$apply(function() { d.resolve(window.d3); });
      }
      // Create a script tag with d3 as the source
      // and call our onScriptLoad callback when it
      // has been loaded
      var scriptTag = $document[0].createElement('script');
      scriptTag.type = 'text/javascript'; 
      scriptTag.async = true;
      scriptTag.src = 'http://d3js.org/d3.v3.min.js';
      scriptTag.onreadystatechange = function () {
        if (this.readyState == 'complete') onScriptLoad();
      }
      scriptTag.onload = onScriptLoad;

      var s = $document[0].getElementsByTagName('body')[0];
      s.appendChild(scriptTag);

      return {
        d3: function() { return d.promise; }
      };
    }
  ]);

// Declare app level module which depends on filters, and services
angular.module('walt', [
  'ngRoute',
  'walt.filters',
  'walt.services',
  'walt.directives',
  'walt.controllers',
  'd3'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/w/bookmark', {templateUrl: '/frontcast/static/js/angular/partials/workingdocument.bookmark.html', controller: 'workingdocumentCreateCtrl'});
  // $routeProvider.when('/w/edit', {templateUrl: '/frontcast/static/js/angular/partials/workingdocument.edit.html', controller: 'workingdocumentCreateCtrl'});
  
  $routeProvider.when('/corpus', {templateUrl: '/frontcast/static/js/angular/partials/corpus.list.html', controller: 'corpusListCtrl'});
  $routeProvider.when('/corpus/:id', {templateUrl: '/frontcast/static/js/angular/partials/corpus.html', controller: 'corpusCtrl'});
  $routeProvider.when('/document', {templateUrl: '/frontcast/static/js/angular/partials/document.list.html', controller: 'MyCtrl2'});
  $routeProvider.otherwise({redirectTo: '/corpus'});
}]);