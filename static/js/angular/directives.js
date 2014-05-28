'use strict';

/* Directives */


angular.module('walt.directives', [])
  .directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }])
  /*
   * Checks every $digest for height changes
   */
  .directive( 'watch-bounds', [function() {
    return {
      link: function( scope, elem, attrs ) {
        scope.$watch(function() {
          scope.__height = elem.height();
        });
      }
    }
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
        initdata: '=overallData',
        data: '=data'
      },
      link: function(scope, element, attrs) {
        d3Service.d3().then(function(d3) {

          // our d3 code will go here
          var svg = d3.select(element[0]).append('svg')
            .style('width', '100%')
            .style('margin-top', '6px');
          

          //console.log('INITDATA');

          var margin = parseInt(attrs.margin) || 20,
              barHeight = parseInt(attrs.barHeight) || 20,
              barPadding = 0,
              maximum;
              

          
          scope.render = function(data) {
            var width = d3.select(element[0]).node().offsetWidth,
                height = 60,
                color = d3.scale.category20(),
                col = 12,// min max?width/data.length - data.length*2,
                
                max = d3.max(data, function(d) {
                  return d.count;
                }),

                overallmax = maximum || max,
                

                node_selection,
                enter_selection,
                exit_selection;

            

            var scale = d3.scale.linear()
                  .domain([0, max])
                  .range([0, 60]);
            
            //console.log("DATA MAX", max, data)

            svg.attr('height', height); // set the height based on the calculations above

            var selection = svg.selectAll('rect').data(data, function(d) {
              return d.slug; // unique shared identifier :D
            });

            selection.transition()
              .duration(500)
              .attr('y', function(d) {
                return height - scale(d.count);
              })
              .attr('height', function(d) {
                return scale(d.count);
              })
              .attr('width', col)
              .attr('title', function(d) {
                return d.count
              })
              .attr('fill', '#fff')


            

            selection.enter().append('rect')
              .attr('x', function(d,i){
                return i*(col + 2)
              })
              .transition()
              .duration(500)
              .attr('y', function(d) {
                return height - scale(d.count);
              })
              .attr('height', function(d) {
                return scale(d.count);
              })
              .attr('width', col)
              .attr('fill', '#fff')

            selection.exit()
              .transition()
              .duration(500)
              .attr('y', height - 2)
              .attr('height', 2)
              .attr('fill', '#aa3735')

            /*  
            g.append('text')
              .attr('x', function(d,i){
                return i*(col + 2)
              })
              .attr('y', height)
              .attr('display', function(d) {
                return d.count >= max? 'block': 'none'
              })
              .text(function(d){return 'h' + d.count})

            g.select("rect")
              .transition()
              .duration(750)
              
              .attr('y', function(d) {
                return height - scale(d.count);
              })
              .attr('height', function(d) {
                return scale(d.count);
              })
              .attr('fill', '#fff')

            /* on update: what to be updated?
            node_selection.each(function(d, i) {
              var el = d3.select(this); 
              console.log('node updating is the', max, data);
              el.selectAll("rect")
                  .transition()
                  .duration(300)
                  .attr('y', function(d) {
                    return height - scale(d.count);
                  })
                  .attr('height', function(d) {
                    return scale(d.count);
                  })
                  .attr('fill', '#fff')
                  .attr('title', function(d) {
                    return d.slug + ' ' + d.count + ' ' + max
                  })

              el.selectAll("text")
                .attr('y', 20)
                .attr('display', function(d) {
                  return d.count >= max? 'block': 'none'
                })
                .text(function(d){return d.count})
            });

            // entering
            enter_selection = node_selection.enter().append("g")
                
            

            //exiting
            exit_selection = node_selection.exit().each(function(d, i) {
              var el = d3.select(this);
              el.selectAll("rect")
                .transition()
                .duration(300)
                .attr('y', height - 2)
                .attr('height', 2)
                .attr('fill', '#aa3735')
                .attr('title', 0)

               el.selectAll("text")
                .attr('y', height)
                .attr('display', function(d) {
                  return d.count >= max? 'block': 'none'
                })
                .text(function(d){return d.count})
            });
            /*
            enter.append('text')
              .attr('x', function(d,i){
                return i*(col + 2)
              })
              .attr('y', function(d) {
                return height - scale(d.count);
              })
              .attr('display', function(d) {
                return d.count == max? 'block': 'none'
              })
              .text(function(d){return 'h' + d.count})

            // update
            selection.transition().duration(1000).
              .attr('y', function(d) {
                return height - scale(d.count);
              })
              .attr('height', function(d) {
                return scale(d.count);
              })

            selection.transition()
              .duration(1000)
              .attr('y', function(d) {
                return height - scale(d.count);
              })
              .attr('height', function(d) {
                return scale(d.count);
              })

            selection.exit()
            .transition()
              .duration(1000)
              .attr('height', 2)
              .attr('y', height - 2);
            */
            $compile(element)
          }; // end of render er

          // Watch for resize event
          

          scope.render(d3.values(scope.initdata));
          scope.$watch('data', function(){
            scope.render(d3.values(scope.data))
          });
          
        });
      }};
  }]);