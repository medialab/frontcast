'use strict';

/* Directives */


angular.module('walt.directives', [])
  .directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }])
  /*
    handle columns resize
  */
  .directive('resizable', ['$window', function($window) {
    return function($scope) {
      $scope.initializeWindowSize = function() {
        $scope.availableHeight = $window.innerHeight;
      };
      $scope.initializeWindowSize();
      return angular.element($window).bind('resize', function() {
        $scope.initializeWindowSize();
        return $scope.$apply();
      });
    };  
  }])
  /*
    jquery fixed scroll on header (when object is created)
  */
  .directive('scrollToFixed', function() {
    return{
      restrict: 'A',
      scope: {
        marginTop: '='
      },
      link: function (scope, element, attrs) {
        //alert('eeeee' + );
        $(element).scrollToFixed({
          marginTop: scope.marginTop || 0
        });
      }
    };
  })
  
  .directive('fancySelect', function() {
    var linkFn = function(scope, element, attrs) {
      //alert(scope['orders'])
      $(element).append('<option value="cc">sss</option>').fancySelect();
    };
    return {
      restrict: 'A',
      transclude: true,
      link: linkFn
    };
  })
  /*
    Usage <div ghost-scroll >
    var y = $(document).scrollTop(),
          scrollheight =main.outerHeight();

      if(y < 12) // header shadow invisible
        header.hasClass('drop-shadow') && header.removeClass('drop-shadow');
      else 
        header.addClass('drop-shadow');

      if( y > scrollheight - h - 12) // footer shadow invisible
        footer.hasClass('drop-shadow') && footer.removeClass('drop-shadow');
      else 
        footer.addClass('drop-shadow');
  */
  .directive('ghostScroll', ['$window', function($window) {
    return function($scope, element, attrs) {
      angular.element($window).bind("scroll", function() {
        var y = this.pageYOffset, // console.log(this.pageYOffset)
            h = element.outerHeight;
            
        if(y < 12){
          // angular.element('header')
          
        }
             /*if (this.pageYOffset >= 100) {
                 scope.boolChangeClass = true;
             } else {
                 scope.boolChangeClass = false;
             }
            scope.$apply();*/
      });
    };
  }])
  .directive("angularRatings", function() {
    return {
      restrict: 'E',
      scope: {
        model: '=ngModel',
        notifyId: '=notifyId'
      },
      replace: true,
      transclude: true,
      template: '<div><ol class="angular-ratings">' + '<li ng-class="{active:model>0,over:over>0}">1</li>' + '<li ng-class="{active:model>1,over:over>1}">2</li>' + '<li ng-class="{active:model>2,over:over>2}">3</li>' + '<li ng-class="{active:model>3,over:over>3}">4</li>' + '<li ng-class="{active:model>4,over:over>4}">5</li>' + '</ol></div>',
      controller: [
        '$scope', '$attrs', '$http', function($scope, $attrs, $http) {
          $scope.over = 0;
          $scope.setRating = function(rating) {
            $scope.model = rating;
            $scope.$apply();
            if ($attrs.notifyUrl !== void 0 && $scope.notifyId) {
              return $http.post($attrs.notifyUrl, {
                id: $scope.notifyId,
                rating: rating
              }).error(function(data) {
                if (typeof data === 'string') {
                  alert(data);
                }
                return $scope.model = 0;
              });
            }
          };
          return $scope.setOver = function(n) {
            $scope.over = n;
            return $scope.$apply();
          };
        }
      ],
      link: function(scope, iElem, iAttrs) {
        if (iAttrs.notifyUrl !== void 0) {
          return angular.forEach(iElem.children(), function(ol) {
            return angular.forEach(ol.children, function(li) {
              li.addEventListener('mouseover', function() {
                return scope.setOver(parseInt(li.innerHTML));
              });
              li.addEventListener('mouseout', function() {
                return scope.setOver(0);
              });
              return li.addEventListener('click', function() {
                return scope.setRating(parseInt(li.innerHTML));
              });
            });
          });
        }
      }
    };
  })
  .directive('d3Bars', ['d3Service', '$compile',  function(d3Service, $compile) {
    return  {
      restrict: 'EA',
      scope: {
        data: '=data'
      },
      link: function(scope, element, attrs) {
        d3Service.d3().then(function(d3) {

          // our d3 code will go here
          var svg = d3.select(element[0]).append('svg')
            .style('width', '100%')
            .style('margin-top', '6px');
              

          var margin = parseInt(attrs.margin) || 20,
              barHeight = parseInt(attrs.barHeight) || 20,
              barPadding = 0;

          // Browser onresize event
          

          // Watch for resize event
           scope.$watch('data', function(){
            scope.render(d3.values(scope.data))
           });

          // watch for data changes. just remove?
          scope.render = function(data) {
            svg.selectAll('*').remove();
            if (!data) return;
            // setup variables
            var width = d3.select(element[0]).node().offsetWidth,
                height = 36,
                color = d3.scale.category20(),
                col = 12,//width/data.length - data.length*2,
                xScale = d3.scale.linear()
                  .domain([0, d3.max(data, function(d) {
                    return d.count;
                  })])
                  .range([2, height]);

            // set the height based on the calculations above
            svg.attr('height', height);

            //create the rectangles for the bar chart
            svg.selectAll('rect')
              .data(data).enter()
                .append('rect')
                .attr('width', col)
                .attr('x', function(d,i){
                  return i*(col + 2)
                })
                .attr('y', function(d) {
                  return height - xScale(d.count);
                })
                .attr('fill', '#fff')
                
                //.transition()
                //.duration(1000)
                .attr('height', function(d) {
                  return xScale(d.count);
                })

                .attr("tooltip-append-to-body", true)
               .attr("title", function(d){
                   return d.name;
               });

            
          }; // end of renderer

          scope.render(d3.values(scope.data));
          $compile(element)
        });
      }};
  }]);