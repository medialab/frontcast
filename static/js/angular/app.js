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
  'd3',
  'toggle-switch',
  'ngSanitize',
  'xeditable',
  'ui.bootstrap',
  
  'monospaced.elastic'
]).
config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider, $cookies) {
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';

  $routeProvider.when('/w/:id/edit', {templateUrl: '/frontcast/static/js/angular/partials/workingdocument.edit.html', controller: 'workingdocumentEditCtrl'});
  
  $routeProvider.when('/w/bookmark', {templateUrl: '/frontcast/static/js/angular/partials/workingdocument.bookmark.html', controller: 'workingdocumentCreateCtrl'});
  // $routeProvider.when('/w/edit', {templateUrl: '/frontcast/static/js/angular/partials/workingdocument.edit.html', controller: 'workingdocumentCreateCtrl'});
  
  //$routeProvider.when('/', {templateUrl: '/frontcast/static/js/angular/partials/overview.html', controller: 'overviewCtrl'});
  
  // documents
  $routeProvider.when('/docs', {templateUrl: '/frontcast/static/js/angular/partials/document.list.html', controller: 'documentsCtrl', reloadOnSearch:false});
  $routeProvider.when('/doc/:id/profile', {templateUrl: '/frontcast/static/js/angular/partials/document.profile.html', controller: 'documentProfileCtrl'});
  $routeProvider.when('/doc/:id/profile/edit', {templateUrl: '/frontcast/static/js/angular/partials/document.profile.edit.html', controller: 'documentProfileCtrl'});

  // courses
  $routeProvider.when('/courses', {templateUrl: '/frontcast/static/js/angular/partials/course.list.html', controller: 'coursesCtrl', reloadOnSearch:false});
  $routeProvider.when('/course/:id', {templateUrl: '/frontcast/static/js/angular/partials/course.html', controller: 'courseCtrl'});
  
  // seances
  $routeProvider.when('/lessons', {templateUrl: '/frontcast/static/js/angular/partials/lesson.list.html', controller: 'lessonsCtrl', reloadOnSearch:false});
  $routeProvider.when('/lesson/:id', {templateUrl: '/frontcast/static/js/angular/partials/lesson.html', controller: 'lessonCtrl'});

  // tools
  $routeProvider.when('/tools', {templateUrl: '/frontcast/static/js/angular/partials/tool.list.html', controller: 'toolsCtrl', reloadOnSearch:false});
  $routeProvider.when('/tools/add', {templateUrl: '/frontcast/static/js/angular/partials/tool.add.html', controller: 'toolCtrl'});
  $routeProvider.when('/tools/:id/edit', {templateUrl: '/frontcast/static/js/angular/partials/tool.edit.html', controller: 'toolCtrl'});
  $routeProvider.when('/tool/:id', {templateUrl: '/frontcast/static/js/angular/partials/tool.html', controller: 'toolCtrl'});

  $routeProvider.otherwise({redirectTo: '/docs'});

  //$locationProvider.html5Mode(true);
}]);
