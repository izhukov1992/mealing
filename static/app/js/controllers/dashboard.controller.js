(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('DashboardController', DashboardController);

    function DashboardController($scope, $cookies, Reporter, Meal, meals, profile) {
      var vm = this;
      vm.add = {};
      vm.edit = {};
      vm.meals = meals;
      vm.limit = profile.limit;
      vm.SetCalorieLimit = SetCalorieLimit;
      vm.EatOut = EatOut;
      vm.EditMeal = EditMeal;
      vm.SaveMeal = SaveMeal;
      vm.RemoveMeal = RemoveMeal;
      
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
          'description': vm.add.description,
          'calories': vm.add.calories,
          'date': vm.add.date,
          'time': vm.add.time
        });
        meal.$save()
        .then(function(meal) {
          console.log("mealed");
          vm.meals.push(meal);
        });
      }
      
      function EditMeal(instance) {
        var index = vm.meals.indexOf(instance);
        angular.copy(instance, vm.edit);
        vm.edit.index = index;
      }
      
      function SaveMeal() {
        var meal = new Meal({
          'id': vm.edit.id,
          'description': vm.edit.description,
          'calories': vm.edit.calories,
          'date': vm.edit.date,
          'time': vm.edit.time
        });
        meal.$update()
        .then(function() {
          console.log("meal " + vm.edit.id + " updated");
          var index = vm.edit.index;
          delete vm.edit.index;
          angular.copy(vm.edit, vm.meals[index]);
        });
      }
      
      function RemoveMeal(instance) {
        var meal = new Meal({
          'id': instance.id
        });
        meal.$remove()
        .then(function() {
          console.log("meal " + instance.id + " removed");
          vm.meals.splice(vm.meals.indexOf(instance), 1);
        });
      }
    }

})();