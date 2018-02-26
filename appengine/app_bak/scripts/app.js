'use strict';

/**
 * @ngdoc overview
 * @name ngappApp
 * @description
 * # ngappApp
 *
 * Main module of the application.
 */
angular
  .module('ngappApp', [
    'ngResource',
    'ui.router',
    'firebase'
  ]).config(function($stateProvider, $urlRouterProvider){
	    $stateProvider
	    .state({
	        name: 'login',
	        url: '/login',
	        templateUrl: 'views/login.html',
	        controller: 'LoginCtrl as login',
	    });

	    $urlRouterProvider.otherwise('/login');

	});
