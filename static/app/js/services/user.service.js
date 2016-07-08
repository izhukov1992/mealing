(function() {
  'use strict';

  angular
    .module('mealing')
    .factory('User', User);

    function User($resource) {
      return $resource(
        '/api/v1/user/:id/',
        {id: '@id'},
        {'update': {method:'PUT'}}
      );
    }

})();