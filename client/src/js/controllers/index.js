'use strict';

/**
 * @ngdoc function
 * @name frontcast.controller:indexCtrl
 * @description
 * # indexCtrl
 * Controller of the frontcast layout.
 */
angular.module('frontcast')
  .controller('indexCtrl', function($scope, $log, $routeParams) {
    $log.debug('indexCtrl loaded.');

    /*
      Load documents
    */
    $scope.sync = function() {
      
    }
  });