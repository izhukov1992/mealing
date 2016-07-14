(function() {
  'use strict';

  angular
    .module('mealing')
    .controller('ManagerController', ManagerController);

    function ManagerController($scope, $cookies, DTOptionsBuilder, DTColumnDefBuilder, Reporter, Meal) {
      var vm = this;
      
      vm.dtOptions = DTOptionsBuilder.newOptions()
        .withPaginationType('full_numbers')
        .withDisplayLength(50)
        .withOption('order', [[1, 'desc'],[0, 'desc']]); 
      vm.dtColumnDefs = [
        DTColumnDefBuilder.newColumnDef(0).notVisible(),
        DTColumnDefBuilder.newColumnDef(4).notSortable(),
        DTColumnDefBuilder.newColumnDef(5).notSortable(),
      ];
      
    }

})();