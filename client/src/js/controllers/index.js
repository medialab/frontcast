'use strict';

/**
 * @ngdoc function
 * @name frontcast.controller:indexCtrl
 * @description
 * # indexCtrl
 * Controller of the frontcast layout.
 */
angular.module('frontcast')
  .controller('indexCtrl', function($scope, $log, $routeParams, DocumentsFactory) {
    $log.debug('indexCtrl loaded.');

    $scope.setOrderby([
      {
        label: 'title',
        value: '-title'
      },
      {
        label: 'rating',
        value: '-rating'
      }
    ],{
        label: 'last added',
        value: '-id'
      });


    /*
      Load documents
    */
    $scope.sync = function() {
      $log.info('indexCtrl.sync');
      DocumentsFactory.query({order_by:'["title"]'}, function(res) {
        $scope.items = res.objects;
      });
    };
    

    $scope.sync();
  });