(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('DashboardController', DashboardController);

    function DashboardController($scope, $cookies, Reporter, Meal, meals, today, profile) {
      var vm = this;
      vm.add = {};
      vm.edit = {};
      vm.filter = {};
      vm.meals = meals;
      vm.today = today;
      vm.limit = profile.limit;
      vm.percentage = 0;
      vm.SetCalorieLimit = SetCalorieLimit;
      vm.EatOut = EatOut;
      vm.EditMeal = EditMeal;
      vm.SaveMeal = SaveMeal;
      vm.RemoveMeal = RemoveMeal;
      vm.FilterMeal = FilterMeal;
      vm.TodayMeal = TodayMeal;
      vm.CalculateMeal = CalculateMeal;
      vm.FormatDate = FormatDate;
      vm.FormatTime = FormatTime;
      
      vm.CalculateMeal();
      
      function SetCalorieLimit() {
        var reporter = new Reporter({
          'id': $cookies.get('profile'),
          'limit': vm.limit
        });
        reporter.$update()
        .then(function() {
          console.log("calorie limit updated");
          vm.TodayMeal();
        });
      }
      
      function EatOut() {
        var date = vm.FormatDate(vm.add.date);
        var time = vm.FormatTime(vm.add.time);
        var meal = new Meal({
          'description': vm.add.description,
          'calories': vm.add.calories,
          'date': date,
          'time': time
        });
        meal.$save()
        .then(function(meal) {
          console.log("mealed");
          vm.meals.push(meal);
          vm.TodayMeal();
        });
      }
      
      function EditMeal(instance) {
        angular.copy(instance, vm.edit);
        var time = vm.edit.time.split(":");
        vm.edit.time = new Date();
        vm.edit.time.setHours(time[0]);
        vm.edit.time.setMinutes(time[1]);
        vm.edit.time.setSeconds(time[2]);
        vm.edit.date = new Date(vm.edit.date);
      }
      
      function SaveMeal() {
        var date = vm.FormatDate(vm.edit.date);
        var time = vm.FormatTime(vm.edit.time);
        var meal = new Meal({
          'id': vm.edit.id,
          'description': vm.edit.description,
          'calories': vm.edit.calories,
          'date': date,
          'time': time
        });
        meal.$update()
        .then(function() {
          console.log("meal " + vm.edit.id + " updated");
          vm.FilterMeal();
          vm.TodayMeal();
        });
      }
      
      function RemoveMeal(instance) {
        var meal = new Meal({
          'id': instance.id
        });
        meal.$remove()
        .then(function() {
          console.log("meal " + instance.id + " removed");
          vm.FilterMeal();
          vm.TodayMeal();
        });
      }
      
      function FilterMeal() {
        var start_date = vm.FormatDate(vm.filter.start_date);
        var end_date = vm.FormatDate(vm.filter.end_date);
        Meal
        .query({
          'start_date': start_date,
          'end_date': end_date
        })
        .$promise
        .then(function (data) {
          vm.meals = data;
        });
      }
      
      function TodayMeal() {
        Meal
        .query({
          'only_today': true
        })
        .$promise
        .then(function (data) {
          vm.today = data;
          vm.CalculateMeal();
        });
      }
      
      function CalculateMeal() {
        vm.percentage = 0;
        if (vm.today.length === 1) {
          vm.percentage = vm.today[0].calories;
        }
        else if (vm.today.length > 1) {
          vm.percentage = vm.today.reduce(function (previous, current) {
            return previous.calories + current.calories;
          });
        }
        vm.percentage = vm.percentage / vm.limit * 100;
      }
      
      function FormatDate(source_date) {
        var date;
        if (Date.parse(source_date)) {
          date = new Date(source_date);
          date = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
        }
        return date
      }
      
      function FormatTime(source_date) {
        var time;
        if (Date.parse(source_date)) {
          time = new Date(source_date);
          time = time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds();
        }
        return time
      }
    }

})();