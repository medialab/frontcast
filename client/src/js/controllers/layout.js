'use strict';

/**
 * @ngdoc function
 * @name frontcast.controller:layoutCtrl
 * @description
 * # LayoutCtrl
 * Controller of the frontcast layout.
 * Note that you don't want to modify values from inside a child controller.
 * Use the dedicated function to modify layoutCtrl scope vars.
 */
angular.module('frontcast')
  .controller('layoutCtrl', function($scope, $log, $routeParams) {
    $log.debug('layoutCtrl loaded');
   

    $scope.orderByChoices = [
      {
        label:'label',
        value:'soortvalue'
      }
    ];
    
    $scope.orderBy = $scope.orderByChoices[0];
    $scope.filters = {};
    $scope.filtersItems = {}; // the corresponding itesms, with full information available (id, slug, name etc...)
    $scope.facets = {};
    
    $scope.limit = 50;
    $scope.page = 1;

    $scope.total = 0;// the number of toatl item in view
    $scope.filtered = 0;// the number of available items in view (to be used with filters)


    // to be called from below
    $scope.setOrderbyChoices = function(choices, orderBy) {
      $log.info('    setOrderbyChoices', choices);
      $scope.orderByChoices = choices;
      $scope.orderBy = orderBy;
    };

    $scope.setOrderBy = function(choice) {
      $log.info('    setOrderby', choice);
      $scope.orderBy = choice;
      $scope.page = 1;
      $scope.$broadcast('API_PARAMS_CHANGED');
    }

    $scope.setPage = function() {
      $log.info('    setPage', $scope.page);
      $scope.$broadcast('API_PARAMS_CHANGED');
    }

    $scope.setFacets = function(facets) {
      $scope.facets = facets
    }

    $scope.setTotal = function(total) {
      $scope.total = total;
    }

    // set number of filtered items
    $scope.setFiltered = function(filtered) {
      $scope.filtered = filtered;
    }

    /*
      # function setFilter

      Filter functions: set and remove.
      Since we may change order, filters, offset or limits,
      we broadcast the event to layoutCtrl children controllers.
    */
    $scope.setFilter = function(key, filter, item) {
      $log.info('    setFilter', key, filter, item);
      $scope.filters[key] = filter;
      $scope.filtersItems[key] = angular.extend({
        filter: filter
      }, item);
      $scope.$broadcast('API_PARAMS_CHANGED');
    };

    /*
      # function removeFilter
      Filter functions: remove.
      Cfr. setFilter()
    */
    $scope.removeFilter = function(key, filter) {
      if($scope.filters[key] == filter) {
        delete $scope.filters[key];
        delete $scope.filtersItems[key];
      };
      $scope.$broadcast('API_PARAMS_CHANGED');
    };

    /*
      # function getParams

      return a dict object that can be used to call the api.
      Normally the sync function should have this function to re-assemble the parameters
      it handles: filters, order_by, search, limit and offset.
      Usage with DocumentFacory:

    */
    $scope.getParams = function(params) {
      var params = angular.extend({
        offset: $scope.limit * ($scope.page - 1),
        limit: $scope.limit,
        filters: JSON.stringify(angular.copy($scope.filters)),
        order_by: JSON.stringify($scope.orderBy.value.split('|'))
      }, params);
      return params;
    };

    /*
      Clone source in target by changing only the *different* fields
    */
    $scope.diffclone = function(target, source) {
      if(!target) {
        target = source;
      } else {
        for(var i in source) {
          if(typeof target[i]=='object') {
            $scope.diffclone(target[i], source[i]);
          } else if(!target[i] || target[i] != source[i]) {//console.log('updtargetted', i);
            target[i] = source[i];
          }
        }
      }
    };
  });