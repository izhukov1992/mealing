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
      vm.Edit = Edit;
      vm.Remove = Remove;
      
      function SetCalorieLimit() {
        var reporter = new Reporter({
          'id': $cookies.get('profile'),
          'limit': vm.limit
        });
        reporter.$update()
        .then(function() {
          console.log("calorie limit updated");
        });
      }
      
      function EatOut() {
        var meal = new Meal({
          'description': vm.instance.description,
          'calories': vm.instance.calories,
          'date': vm.instance.date,
          'time': vm.instance.time
        });
        meal.$save()
        .then(function(meal) {
          console.log("mealed");
          vm.Meals.push(meal);
        });
      }
      
      function Edit(instance) {
      }
      
      function Remove(instance) {
        var meal = new Meal({
          'id': instance.id
        });
        meal.$remove()
        .then(function() {
          console.log("meal " + instance.id + " removed");
          vm.Meals.splice(vm.Meals.indexOf(instance), 1);
        });
      }
    }

})();