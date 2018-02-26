'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:LoginCtrl
 * @description
 * # LoginCtrl
 * Controller of the ngappApp
 */
angular.module('ngappApp')
  .controller('LoginCtrl', ['$window', '$firebaseAuth', '$http', function ($window, $firebaseAuth, $http) {

//  var login = this;

//  var backendHostUrl = '/v1/u';

  // Fetch Backend Authorization Code
  function fetchBackendAuthCodeByToken(idToken) {
    $http({
        url: '/oc/oauth',
        method: 'GET',
        params: {'auth_token': idToken}
    }).then(function successCallback(response) {
            // this callback will be called asynchronously
            // when the response is available
            console.log('aut_code success', response.data);
        }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            console.log('auth_code fail', response.statusText);
    });
  }

  // Firebase log-in
  function configureFirebaseLogin() {

    // [START onAuthStateChanged]
    var auth = $firebaseAuth();

    auth.$onAuthStateChanged(function(user) {
      if (user) {
//        var name = user.displayName;

        /* If the provider gives a display name, use the name for the
        personal welcome message. Otherwise, use the user's email. */
//        var welcomeName = name ? name : user.email;

        user.getToken().then(function(idToken) {

          /* Now that the user is authenicated, fetch the backend service authentication code. */
          fetchBackendAuthCodeByToken(idToken);
        });

      }
    // [END onAuthStateChanged]

    });

  }


  // [START configureFirebaseLoginWidget]
  // Firebase log-in widget
  function configureFirebaseLoginWidget() {
    var uiConfig = {
      'signInSuccessUrl': '/',
      'signInOptions': [
        // Leave the lines as is for the providers you want to offer your users.
        $window.firebase.auth.GoogleAuthProvider.PROVIDER_ID,
//        firebase.auth.FacebookAuthProvider.PROVIDER_ID,
//        firebase.auth.TwitterAuthProvider.PROVIDER_ID,
//        firebase.auth.GithubAuthProvider.PROVIDER_ID,
        $window.firebase.auth.EmailAuthProvider.PROVIDER_ID
      ],
      // Terms of service url
      'tosUrl': '<your-tos-url>',
    };

    var ui = new $window.firebaseui.auth.AuthUI($window.firebase.auth());
    ui.start('#firebaseui-auth-container', uiConfig);
  }
  // [END configureFirebaseLoginWidget]

  configureFirebaseLogin();
  configureFirebaseLoginWidget();

  }]);
