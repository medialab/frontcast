'use strict'
/*
  Angular.js controllers



*/
function DocumentListCtrl($scope, $http) {
  $scope.total_count = 0;
  $scope.documents = [];

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
}


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

}
