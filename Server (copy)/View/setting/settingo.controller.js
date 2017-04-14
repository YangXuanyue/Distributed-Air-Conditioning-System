(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['UserService','$rootScope', '$cookieStore', '$interval', 'AuthenticationService', 'CommonSettingService'
    ];

    function HomeController(UserService, $rootScope, $cookieStore, $interval, AuthenticationService, CommonSettingService) {
        var vm = this;
        vm.user = $rootScope.globals.currentUser;
        vm.common_setting = {};
        vm.logout = logout;

        (function init() {
            initState();
            var timer = $interval(danmuMaintain(), 5000);
        })();

        function initState() {
            DanmuService.GetRooms()
                .then(function (response) {
                    var vm.common_setting = response;
                });
        }

        function logout() {
            AuthenticationService.ClearCredentials();
            location.reload();
        }

        function 
    }

})();

