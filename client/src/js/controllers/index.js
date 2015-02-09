'use strict';

/**
 * @ngdoc function
 * @name frontcast.controller:indexCtrl
 * @description
 * # indexCtrl
 * Controller of the frontcast layout.
 */
angular.module('frontcast')
  .controller('indexCtrl', function($scope, $log, $routeParams, DocumentsFactory, DocumentsFacetsFactory) {
    $log.debug('indexCtrl loaded.');

    $scope.setOrderbyChoices([
      {
        label: 'title a-z',
        value: 'title'
      },
      {
        label: 'title z-a',
        value: '-title'
      },
      {
        label: 'top rated',
        value: '-rating'
      },
      {
        label: 'last added first',
        value: '-id'
      }
    ],{
        label: 'last added',
        value: '-id'
      });


    /*
      Load documents
    */
    $scope.sync = function() {
      $log.info('indexCtrl.sync', $scope.getParams());
      DocumentsFactory.query($scope.getParams(), function(res) {
        $scope.items = res.objects;
        $scope.setTotal(res.meta.total_count);
      });
      DocumentsFacetsFactory.query($scope.getParams(), function(res) {
        $scope.setFiltersItems(res.facets);
      });
    };

    $scope.$on('API_PARAMS_CHANGED', $scope.sync);
    
    $scope.sync();
  });