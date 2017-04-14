(function () {
    'use strict';

    angular
        .module('app')
        .factory('AuthenticationService', AuthenticationService);

    AuthenticationService.$inject = ['$http', '$cookieStore', '$rootScope', '$timeout', 'UserService'];
    function AuthenticationService($http, $cookieStore, $rootScope, $timeout, UserService) {
        var service = {};

        service.Login = Login;
        service.SetCredentials = SetCredentials;
        service.ClearCredentials = ClearCredentials;

        return service;

        function Login(username, password) {
            return $http.post($rootScope.getUrl+'valid', {
                    userName: username,
                    password: password
                    },{
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded'}
                    }).then(handleSuccess, handleError);
        }
        
        function SetCredentials(username, password) {
            $rootScope.globals = {
                currentUser: {
                    userName: username,
                    password: password
                }
            };
            $cookieStore.put('globals', $rootScope.globals);
        }

        function ClearCredentials() {
            $rootScope.globals = {};
            $cookieStore.remove('globals');
        }

        function handleSuccess(res) {
            console.log("enter handleSuccess");
            console.log(res);
            if (res.data === 'true') {
                return {success: true}
            } else {
                return {success: false, message: '用户名或密码错误'}
            }
        }

        function handleError(res) {
            console.log("enter handleError");
            return { success: false, message: '用户名或密码错误'};
        }
    }

})();