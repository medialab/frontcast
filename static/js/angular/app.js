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
  'ngCookies',
  'ngAnimate',
  'walt.filters',
  'walt.services',
  'walt.directives',
  'walt.controllers',
  'd3'
]).
config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider, $cookies) {
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';

  $routeProvider.when('/w/:id/edit', {templateUrl: '/frontcast/static/js/angular/partials/workingdocument.edit.html', controller: 'workingdocumentEditCtrl'});
  
  $routeProvider.when('/w/bookmark', {templateUrl: '/frontcast/static/js/angular/partials/workingdocument.bookmark.html', controller: 'workingdocumentCreateCtrl'});
  // $routeProvider.when('/w/edit', {templateUrl: '/frontcast/static/js/angular/partials/workingdocument.edit.html', controller: 'workingdocumentCreateCtrl'});
  
  $routeProvider.when('/', {templateUrl: '/frontcast/static/js/angular/partials/index.html', controller: 'indexCtrl'});
  $routeProvider.otherwise({redirectTo: '/'});

  //$locationProvider.html5Mode(true);
}]);