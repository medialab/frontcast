'use strict';

/* Controllers */
var CONTROLLER_STATUS_AVAILABLE = 'available',
    CONTROLLER_STATUS_WORKING = 'busy'

angular.module('walt.controllers', []).
  controller('corpusListCtrl', ['$scope', 'CorpusListFactory', function($scope, CorpusListFactory) {
    CorpusListFactory.query(function(data){
      $scope.howmany = data.meta.total_count;
      $scope.corpora = data.objects;
      
    });
  }])
  .controller('corpusCtrl', ['$scope','$routeParams','CorpusFactory', 'DocumentListFactory', function($scope, $routeParams, CorpusFactory, DocumentListFactory) {
    CorpusFactory.query({id: $routeParams.id}, function(data){
      $scope.corpus = data.object;
      
    });
    DocumentListFactory.query({id: $routeParams.id}, function(data){
      $scope.howmany = data.meta.total_count;
      $scope.documents = data.objects;
    });
  }])
  /*

    Edit the abstrac and the tags of a working document 
    ===

  */
  .controller('workingdocumentEditCtrl', ['$scope', '$routeParams', 'WorkingDocumentFactory', 'WorkingDocumentTagsFactory', 'URLFactory', function($scope, $routeParams, WorkingDocumentFactory, WorkingDocumentTagsFactory, URLFactory) {
    $scope.workingdocument = {};
    $scope.csv_tags = '';
    $scope.status = CONTROLLER_STATUS_WORKING; // first loading data

    WorkingDocumentFactory.query({id: $routeParams.id}, function(data){
      $scope.workingdocument = data.object;
      $scope.csv_tags = $scope.workingdocument.tags.map(function(i){return i.name}).join(', ')
      $scope.status = CONTROLLER_STATUS_AVAILABLE
    });

    $scope.addTodo = function(){
      if($scope.status != CONTROLLER_STATUS_AVAILABLE)
        return;
      $scope.status = CONTROLLER_STATUS_WORKING;

      // attach stuff
      WorkingDocumentTagsFactory.save({id: $routeParams.id}, {
        type: 'Ke',
        tags: $scope.csv_tags
      }, function(data){

        WorkingDocumentFactory.save({id: $routeParams.id},{abstract: $scope.workingdocument.abstract_raw}, function(data){
          console.log('Service%c success','color:green', 'status:',data.status)
          console.log(data)
          $scope.workingdocument = data.object;
          $scope.csv_tags = $scope.workingdocument.tags.map(function(i){return i.name}).join(', ')
          $scope.status = CONTROLLER_STATUS_AVAILABLE;
        })
      });
    }
  }])
  /*

    Create a working document form a bookmark, directly    
    ===

  */
  .controller('workingdocumentCreateCtrl', ['$scope', '$location', 'WorkingDocumentListFactory', 'URLFactory', function($scope, $location, WorkingDocumentListFactory, URLFactory) {
    
    var permalink = 'ciao'
    $scope.button = {
      text: 'add',
      disabled: false
    };

    $scope.status = {
      icon: 'fa-check grey',
      disabled: false
    };

    $scope.addTodo = function(){
      // check permalink, then save
      $scope.button.disabled = true;
      $scope.button.text = 'checking...'
      $scope.status.icon = 'fa-spinner';
      $scope.status.disabled = true
      // blablablab
      // check permalink, then save
      // http://www.pitchinteractive.com/beta/index.php
      URLFactory.query({url: $scope.permalink}, function(data) {
        $scope.status.icon = 'fa-check';
        $scope.button.text = 'saving...';

        if(data.object && data.object.title)
          WorkingDocumentListFactory.save({
            title:data.object.title,
            permalink:$scope.permalink,
            rating: 0,
            type:'?'
          }, function(data){
            console.log('data', data);
            $location.path('/w/'+data.object.id+'/edit')
          });
        else {
          alert('ouch, do it again. Url is not valid ?');
          $scope.status.disabled = false;
        }
      });

      /*WorkingDocumentListFactory.create({}, function(data){
        console.log('data', data);
      })*/
      //$location.path('corpusCtrl')
    }
  }]);