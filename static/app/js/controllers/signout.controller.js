(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('SignOutController', SignOutController);

    function SignOutController($scope, $state, Auth) {
      var auth = new Auth();
      auth.$remove()
      .then(function() {
        console.log("signed out")
        $state.go('signin');
      });
    }

})();