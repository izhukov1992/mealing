(function() {
  'use strict';

  angular
    .module('mealing', [
      'ngResource',
      'ngCookies',
      'ui.bootstrap',
      'ui.bootstrap.datetimepicker',
      'ui.router',
      'datatables',
    ]).
    config(function($locationProvider, $resourceProvider, $urlRouterProvider, $stateProvider) {
      $locationProvider.hashPrefix('!');

      $resourceProvider.defaults.stripTrailingSlashes = false;

      $urlRouterProvider.otherwise('/');

      $stateProvider
        .state('dashboard', {
          url: '/',
          templateUrl: 'static/app/templates/dashboard.html',
          controller: 'DashboardController',
          controllerAs: 'vm',
          resolve: {
            meals: function (Meal) {
              return Meal.query().$promise.then(function (response) {
                return response;
              });
            },
            today: function (Meal) {
              return Meal.query({'only_today': true}).$promise.then(function (response) {
                return response;
              });
            },
            profile: function ($cookies, Reporter) {
              return Reporter.get({'id': $cookies.get('profile')}).$promise.then(function (response) {
                return response;
              });
            }
          }
        })
        .state('auth', {
          url: '/auth',
          templateUrl: 'static/app/templates/auth.html',
          controller: 'AuthController',
          controllerAs: 'vm'
        })
        .state('signout', {
          url: '/signout',
          controller: 'SignOutController'
        });
    })
    .run(function($rootScope, $http, $window, $state) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';

      // Ensure authentication
      //$rootScope.$on('$locationChangeSuccess', function() {
      //  if ($window.authRequired) {
      //    $state.go('login');
      //  }
      //});
    });
  
})();