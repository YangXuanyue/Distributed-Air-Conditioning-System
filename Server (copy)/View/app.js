    'use strict';

    var app = angular.module('app', ['ui.router', 'ngCookies']);
    
    app.config(function($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/login');
        $stateProvider
            .state('login', {
                url:'/login',
                templateUrl: 'login/login.view.html',
                controller: 'LoginController as vm'
            })
            .state('home', {
                url:'/home',
                templateUrl: 'home/home.view.html',
                controller: 'HomeController as vm'
            }) 
            .state('setting', {
                url:'/setting',
                templateUrl: 'setting/setting.view.html',
                controller: 'SettingController as vm'
            })           
            .state('register', {
                url:'/register',
                templateUrl: 'register/register.view.html',
                controller: 'RegisterController as vm'
            });
    });

    app.run(function($rootScope, $location, $cookieStore, $http, UserService, AuthenticationService) {
        // keep user logged in after page refresh
        $rootScope.globals = $cookieStore.get('globals') || {};

        $rootScope.getUrl = '127.0.0.1:8080';


        var user = $rootScope.globals.currentUser;
        if (user) {
            AuthenticationService.Login(user.userName,user.password)
                .then(function(res) {
                    AuthenticationService.SetCredentials(user.username,password);
                    $location.path('/home');
                });  
        }
       
        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in and trying to access a restricted page
            var restrictedPage = $.inArray($location.path(), ['/login', '/register','/forgetpass']) === -1;
            var loggedIn = $rootScope.globals.currentUser;
            // if (restrictedPage && !loggedIn) {
            //     $location.path('/login');
            // }
        });
    });


