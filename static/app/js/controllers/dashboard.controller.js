(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('DashboardController', DashboardController);

    function DashboardController($scope, $cookies, Meals, Reporter, Meal) {
      var vm = this;
      vm.instance = null;
      vm.Meals = Meals;
      vm.SetCalorieLimit = SetCalorieLimit;
      vm.EatOut = EatOut;
      
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
      
      function EatOut() {
        var auth = new Meal({
          'description': vm.instance.description,
          'calories': vm.instance.calories,
          'date': vm.instance.date,
          'time': vm.instance.time
        });
        auth.$save()
        .then(function() {
          console.log("mealed");
        });
      }
    }

})();