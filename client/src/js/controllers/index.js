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
    $scope.infiniteScrolling = 'DISABLED'; // do nothing now
    $scope.items = [];

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
      $scope.infiniteScrolling = 'DISABLED';
      DocumentsFactory.query($scope.getParams(), function(res) {
        $scope.items = res.objects;
        $scope.setFiltered(res.meta.total_count);
        $scope.infiniteScrolling = 'ENABLED';
      });
      DocumentsFacetsFactory.query($scope.getParams(), function(res) {
        $scope.setFacets(res.facets);
        $scope.setFiltered(res.meta.total_count);
        $scope.setTotal(res.meta.total_count); // without filtering applied
      });
    };


    $scope.infinite = function() {
      $log.info('indexCtrl.infinite', $scope.infiniteScrolling, $scope.page);
      if($scope.infiniteScrolling == 'DISABLED')
        return;
      $scope.infiniteScrolling = 'DISABLED';
      $scope.addPage();
      $log.info('indexCtrl.infinite', $scope.getParams());
      
      DocumentsFactory.query($scope.getParams(), function(res) {
        for (var i = 0; i < res.objects.length; i++) {
          $scope.items.push(res.objects[i]);
        }
        $scope.infiniteScrolling = 'ENABLED';
      });
    }

    $scope.$on('API_PARAMS_CHANGED', $scope.sync);
    
    $scope.sync();
  });