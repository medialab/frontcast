'use strict';

/**
 * @ngdoc function
 * @name frontcast.controller:layoutCtrl
 * @description
 * # LayoutCtrl
 * Controller of the frontcast layout.
 */
angular.module('frontcast')
  .controller('layoutCtrl', function($scope, $log, $routeParams) {
    $log.debug('layoutCtrl loaded');
    $scope.ciao = "ciao"

    $scope.orderbyChoices = [
      {
        label:'label',
        value:'soortvalue'
      }
    ];
    $scope.orderby = $scope.orderbyChoices[0];



    // to be called from below
    $scope.setOrderby = function(choices, orderby) {
      $log.info('setOrderby', orderby);
      $scope.orderbyChoices = choices;
      $scope.orderby = orderby;
    };

  });