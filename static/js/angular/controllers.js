'use strict'
/*
  Angular.js controllers



*/
'use strict';

/* Controllers */

angular.module('walt.controllers', []).
  controller('MyCtrl1', [function() {

  }])
  .controller('AssignmentCtrl', function($scope, $http) {
    $scope.deliver = function( id ){

      if( confirm('are you sure you wish to deliver this task?') ){

        $http({
          url: '/api/u/assignment/' + id + '/deliver/',
          method: "GET",
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
          }
        })
      }
    }
  })
  .controller('DocumentListCtrl', function($scope, $http){
    $scope.total_count = 0;
    $scope.documents = [];

    $scope.update = function( data ){
      $http({
        url: '/api/u/document/' + data.id,
        method: "POST",
        data: $.param(data),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
      })
    }

    $http.get('/api/document').success(function(data) {
      console.log( data );
      if( data.status != "ok")
        maze.toast( data.error );
      else{
        $scope.total_count = data.meta.total_count;
        $scope.documents = data.objects
      }
    });

    $scope.get_vimeo_id = function( vimeo_url ){
      return vimeo_url.replace(/[^\d]/g,'')
    }
  })
  .controller('ReferenceListCtrl', function($scope, $http){

  });

function AssignmentListCtrl($scope, $http) {
  $scope.total_count = 0;
  $scope.assignments = [];

  $http.get('/api/assignment').success(function(data) {
    console.log( data );
    if( data.status != "ok")
      maze.toast( data.error );
    else{
      $scope.total_count = data.meta.total_count;
      $scope.assignments = data.objects
    }
  });

};
