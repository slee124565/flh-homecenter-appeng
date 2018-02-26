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
	    })
	    .state({
	        name: 'logout',
	        url: '/logout',
	        templateUrl: 'views/logout.html',
	        controller: 'LogoutCtrl as logout',
	    });

//	    $urlRouterProvider.otherwise('/logout');

	});
