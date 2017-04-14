(function () {
    'use strict';

    angular
        .module('app')
        .factory('UserService', UserService);

    UserService.$inject = ['$http', '$rootScope'];

    function UserService($http, $rootScope) {
        var service = {};

        service.Create = Create;

        return service;

        function Create(user) {
            return $http.post('/create_admin', {
                userName: user.username,
                password: user.password
            }).then(handleSuccess, handleError);
        }

        // private functions

        function handleSuccess(res) {
            return { success: true, data: res };
        }

        function handleError(error) {
            return function() {
                return { success: false, message: error };
            };
        }
    }

})();
