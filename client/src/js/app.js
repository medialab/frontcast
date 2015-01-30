'use strict';

angular.module('frontcast', [
  'ngRoute'
])
  .config(function ($routeProvider, $httpProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'src/views/index.html',
        controller: 'indexCtrl'
      })

      .otherwise({
        redirectTo: '/'
      });
  });