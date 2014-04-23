'use strict';

/* Filters */

angular.module('walt.filters', [])
  /*
    A simple excerpt filter to handle abstract and contents. Use with plain text, not html. to be improved

  */
  .filter('excerpt', function() {
    return function(text) {
      var contents = String(text).split(/[\s\n]/);
      return contents.length > 9? contents.slice(0,10).join(" ") + ' [...]': String(text)
    };
  })
  .filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    }
  }]);