(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('SignUpController', SignUpController);

    function SignUpController($scope, Reporter) {
      var vm = this;
      vm.SignUp = SignUp;
      
      function SignUp() {
        var auth = new Reporter({
          'user': {
            'username': vm.username,
            'password': vm.password
          },
          'limit': vm.limit
        });
        auth.$save()
        .then(function() {
          console.log("signed up");
        });
      }
    }

})();