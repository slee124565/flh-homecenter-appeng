'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:LoginCtrl
 * @description
 * # LoginCtrl
 * Controller of the ngappApp
 */
angular.module('ngappApp')
  .controller('LoginCtrl', ['$window', '$location', '$firebaseAuth',
  function ($window, $location, $firebaseAuth) {

    var login = this;
    login.userSignOut = function() {
      $window.firebase.auth().signOut().then(function() {
        console.log('Sign out successful');
      }, function(error) {
        console.log(error);
      });
    };

    var url = $location.url();
    var queryString = url.split('?')[1];
    login.queryString = queryString;


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

    function configureAuthStateChangedHandler() {

      var auth = $firebaseAuth();

      // firebase user authentication state changed handler
      auth.$onAuthStateChanged(function(user) {
        console.log('auth.$onAuthStateChanged ...');
        if (user) {
          user.getIdToken().then(function(idToken) {
            console.log('user firebase login token', idToken);
            login.queryString += '&id_token=' + idToken;
            console.log('queryString', login.queryString);
//            $window.location.href = '/oc/oauth?' + login.queryString;
            $window.location.href = 'https://flh-homecenter.appspot.com/oc/oauth?' + login.queryString;
          });
        } else {
          console.log('no user object and idToken!');
        }
      });

    }

    function configureFirebaseLoginWidget() {
      var uiConfig = {
        'signInSuccessUrl': '/?' + login.queryString,
        'signInOptions': [
          // Leave the lines as is for the providers you want to offer your users.
          $window.firebase.auth.GoogleAuthProvider.PROVIDER_ID,
          $window.firebase.auth.EmailAuthProvider.PROVIDER_ID
        ],
        // Terms of service url
        'tosUrl': '<your-tos-url>',
      };

      var ui = new $window.firebaseui.auth.AuthUI($window.firebase.auth());
      ui.start('#firebaseui-auth-container', uiConfig);
    }

    firebaseInit();
    configureAuthStateChangedHandler();
    configureFirebaseLoginWidget();
  }]);
