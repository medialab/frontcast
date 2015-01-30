'use strict';
// require a STATIC_URL global variable set
var STATIC_URL = STATIC_URL || '';

angular.module('frontcast', [
  'ngRoute'
])
  .config(function ($routeProvider, $httpProvider) {
    $routeProvider
      .when('/', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })

      // view list, create, view, edit a "document"
      .when('/d', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })
      .when('/d/new', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })
      .when('/d/:id', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })
      .when('/d/:id/edit', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })
      .when('/d/:id/props', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })

      // view list, create, view, edit a "working document"
      .when('/w', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })
      .when('/w/new', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })
      .when('/w/:id', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })
      .when('/w/:id/edit', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })
      .when('/w/:id/edit', {
        templateUrl: STATIC_URL + 'src/views/index.html',
        controller: 'indexCtrl'
      })

      .otherwise({
        redirectTo: '/'
      });
  });