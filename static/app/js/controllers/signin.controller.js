(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('SignInController', SignInController);

    function SignInController($scope, $cookies, Auth) {
      var vm = this;
      vm.SignIn = SignIn;
      
      function SignIn() {
        var auth = new Auth({
          'username': vm.username,
          'password': vm.password
        });
        auth.$save()
        .then(function(data) {
          console.log("signed in")
          $cookies.put('profile', data.id);
        });
      }
    }

})();