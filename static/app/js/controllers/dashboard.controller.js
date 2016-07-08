(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('DashboardController', DashboardController);

    function DashboardController($scope, $cookies, Reporter) {
      var vm = this;
      vm.SetCalorieLimit = SetCalorieLimit;
      
      function SetCalorieLimit() {
        var auth = new Reporter({
          'id': $cookies.get('profile'),
          'limit': vm.limit
        });
        auth.$update()
        .then(function() {
          console.log("calorie limit updated");
        });
      }
    }

})();