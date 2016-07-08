(function() {
  'use strict';

  angular
    .module('mealing')
    .factory('Auth', Auth);

    function Auth($resource) {
      return $resource('/api/v1/auth/');
    }

})();