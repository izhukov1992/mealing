(function() {
  'use strict';

  angular
    .module('mealing')
    .factory('Meal', Meal);

    function Meal($resource) {
      return $resource(
        '/api/v1/meal/:id/',
        {id: '@id'},
        {'update': {method:'PUT'}}
      );
    }

})();