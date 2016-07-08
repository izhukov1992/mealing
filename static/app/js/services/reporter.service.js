(function() {
  'use strict';

  angular
    .module('mealing')
    .factory('Reporter', Reporter);

    function Reporter($resource) {
      return $resource(
        '/api/v1/reporter/:id/',
        {id: '@id'},
        {'update': {method:'PUT'}}
      );
    }

})();