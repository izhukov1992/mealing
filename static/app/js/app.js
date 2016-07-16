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
            reporter: function ($cookies, Reporter) {
              return Reporter.get({'id': $cookies.get('profile')}).$promise.then(function (response) {
                return response;
              });
            },
            reporters: function(Reporter) {
              return Reporter.query().$promise.then(function (response) {
                return response;
              });
            }
          }
        })
        .state('manager', {
          url: '/manager',
          templateUrl: 'static/app/templates/manager.html',
          controller: 'ManagerController',
          controllerAs: 'vm',
          resolve: {
            users: function(User) {
              return User.query().$promise.then(function (response) {
                return response;
              });
            },
            reporters: function(Reporter) {
              return Reporter.query().$promise.then(function (response) {
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
    .run(function($http, $rootScope, $cookies, $state) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';

      $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
        if (toState.name == 'auth') {
          if ($cookies.get('profile')) {
            event.preventDefault();
            $state.go('dashboard');
          }
        }
        else {
          if (!$cookies.get('profile')) {
            event.preventDefault();
            $state.go('auth');
          }
        }
      });
    });
  
})();