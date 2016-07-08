(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('SignUpController', SignUpController);

    function SignUpController($scope, User) {
      var vm = this;
      vm.SignUp = SignUp;
      
      function SignUp() {
        var auth = new User({
          'username': vm.username,
          'password': vm.password
        });
        auth.$save()
        .then(function() {
          console.log("signed up");
        });
      }
    }

})();