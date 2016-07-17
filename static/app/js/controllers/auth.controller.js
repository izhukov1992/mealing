(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('AuthController', AuthController);

    function AuthController($scope, $cookies, $state, Auth, User) {
      var vm = this;
      vm.signup = {};
      vm.signin = {};
      vm.SignUp = SignUp;
      vm.SignIn = SignIn;
      
      function SignUp() {
        var auth = new User({
          'username': vm.signup.username,
          'password': vm.signup.password,
          'password_confirm': vm.signup.password_confirm
        });
        auth.$save()
        .then(function(data) {
          console.log("signed up");
          console.log("signed in");
          $cookies.put('profile', data.id);
          $cookies.put('role', data.role);
          $cookies.put('staff', data.user.is_staff);
          $state.go('dashboard');
        }, function(data) {
          vm.signup.errors = data.data;
        });
      }
      
      function SignIn() {
        var auth = new Auth({
          'username': vm.signin.username,
          'password': vm.signin.password
        });
        auth.$save()
        .then(function(data) {
          console.log("signed in");
          $cookies.put('profile', data.id);
          $cookies.put('role', data.role);
          $cookies.put('staff', data.user.is_staff);
          $state.go('dashboard');
        }, function(data) {
          vm.signin.errors = data.data;
        });
      }
    }

})();