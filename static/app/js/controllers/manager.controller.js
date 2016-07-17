(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('ManagerController', ManagerController);

    function ManagerController($scope, DTOptionsBuilder, DTColumnDefBuilder, User, users, Reporter, reporters) {
      var vm = this;
      vm.add = {};
      vm.edit = {};
      vm.roles = [{'id': 0, 'value': 'Role...'},{'id': 1, 'value': 'User'},{'id': 2, 'value': 'Manager'},{'id': 3, 'value': 'Admin'}]
      vm.users = users;
      vm.reporters = reporters;
      vm.JoinBuddy = JoinBuddy;
      vm.EditUser = EditUser;
      vm.SaveUser = SaveUser;
      vm.RemoveUser = RemoveUser;
      vm.UpdateUsers = UpdateUsers;
      
      vm.dtOptions = DTOptionsBuilder.newOptions()
        .withPaginationType('full_numbers')
        .withDisplayLength(50)
        .withOption('order', [[1, 'asc'],[0, 'desc']]); 
      vm.dtColumnDefs = [
        DTColumnDefBuilder.newColumnDef(0).notVisible(),
        DTColumnDefBuilder.newColumnDef(4).notSortable(),
        DTColumnDefBuilder.newColumnDef(5).notSortable(),
      ];

      vm.add.role = 0;

      function JoinBuddy() {
        var user = new User({
          'username': vm.add.username,
          'email': vm.add.email,
          'password': vm.add.password,
          'role': vm.add.role
        });
        user
        .$save()
        .then(function(user) {
          console.log("user created");
          vm.UpdateUsers();
        });
      }
      
      function EditUser(instance) {
        angular.copy(instance, vm.edit);
        delete vm.edit.user.password;
      }
      
      function SaveUser() {
        var user = new User({
          'id': vm.edit.user.id,
          'username': vm.edit.user.username,
          'email': vm.edit.user.email,
          'password': vm.edit.user.password,
          'role': vm.edit.role
        });
        user
        .$update()
        .then(function() {
          console.log("user " + vm.edit.user.id + " updated");
          vm.UpdateUsers();
        });
      }
      
      function RemoveUser(instance) {
        var user = new User({
          'id': instance.user.id
        });
        user
        .$remove()
        .then(function() {
          console.log("user " + instance.user.id + " removed");
          vm.UpdateUsers();
        });
      }
      
      function UpdateUsers() {
        Reporter
        .query()
        .$promise
        .then(function (response) {
          vm.reporters = response;
        });
      }
      
    }

})();