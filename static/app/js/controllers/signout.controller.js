(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('SignOutController', SignOutController);

    function SignOutController($scope, $cookies, $state, Auth) {
      var auth = new Auth();
      auth.$remove()
      .then(function() {
        console.log("signed out")
        $cookies.remove('profile');
        $cookies.remove('role');
        $cookies.remove('staff');
        $state.go('auth');
      });
    }

})();