'use strict';

/**
 * @ngdoc function
 * @name frontcast.controller:toolsCtrl
 * @description
 * # toolsCtrl
 * Controller of the frontcast layout.
 */
angular.module('frontcast')
  .controller('toolsCtrl', function($scope, $log, $routeParams, WorkingDocumentsFactory, WorkingDocumentsFacetsFactory) {
    $log.debug('toolsCtrl loaded.');
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
      $scope.$parent.filters.type = 'T';

      $log.info('toolsCtrl.sync', $scope.getParams());
      $scope.infiniteScrolling = 'DISABLED';
      WorkingDocumentsFactory.query($scope.getParams(), function(res) {
        $scope.items = res.objects;
        $scope.setFiltered(res.meta.total_count);
        $scope.infiniteScrolling = 'ENABLED';
      });
      WorkingDocumentsFacetsFactory.query($scope.getParams(), function(res) {
        $scope.setFacets(res.facets);
        $scope.setFiltered(res.meta.total_count);
        $scope.setTotal(res.meta.total_count); // without filtering applied
      });
    };


    $scope.infinite = function() {
      $log.info('toolsCtrl.infinite', $scope.infiniteScrolling, $scope.page);
      if($scope.infiniteScrolling == 'DISABLED')
        return;
      $scope.infiniteScrolling = 'DISABLED';
      $scope.addPage();
      $log.info('toolsCtrl.infinite', $scope.getParams());
      
      WorkingDocumentsFactory.query($scope.getParams(), function(res) {
        for (var i = 0; i < res.objects.length; i++) {
          $scope.items.push(res.objects[i]);
        }
        if(res.objects.length)
          $scope.infiniteScrolling = 'ENABLED';
      });
    }

    $scope.$parent.filters = {}; // reset filters on load
    $scope.$on('API_PARAMS_CHANGED', $scope.sync);
    $scope.sync();
  });