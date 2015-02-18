'use strict';

/**
 * @ngdoc function
 * @name frontcast.controller:documentCtrl
 * @description
 * # documentCtrl
 * Controller for a single document (view and edit). handle the related devices, too
 */
angular.module('frontcast')
  .controller('documentCtrl', function($scope, $log, $routeParams, DocumentFactory) {
    $log.debug('documentCtrl loaded.');

    DocumentFactory.get({id: $routeParams.id}, function(res) {
      $scope.doc = res.object;
    });
  });