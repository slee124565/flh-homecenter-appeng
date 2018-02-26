'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:LogoutCtrl
 * @description
 * # LogoutCtrl
 * Controller of the ngappApp
 */
angular.module('ngappApp')
  .controller('LogoutCtrl', ['$window', function ($window) {
//  var logout = this;

  function firebaseInit() {
    if (!$window.firebase.apps.length) {
      var firebaseConfig = {
        apiKey: 'AIzaSyBGm_Gwo7zUW3TjAKkVoODZ6g6n4Jx6z9w',
        authDomain: 'flh-pvstation.firebaseapp.com',
        databaseURL: 'https://flh-pvstation.firebaseio.com',
        storageBucket: 'flh-pvstation.appspot.com'
      };
      $window.firebase.initializeApp(firebaseConfig);
    }
  }

  function userLogout() {
      $window.firebase.auth().signOut().then(function() {
        console.log('Sign out successful');
      }, function(error) {
        console.log(error);
      });
  }

  firebaseInit();
  userLogout();
  }]);
