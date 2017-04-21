(function () {
    'use strict';

    angular
        .module('app')
        .controller('SettingController', SettingController);

    SettingController.$inject = ['UserService','$rootScope', '$cookieStore', '$interval', 'AuthenticationService', 'CommonSettingService', 
    ];

    function SettingController(UserService, $rootScope, $cookieStore, $interval, AuthenticationService, CommonSettingService) {
        var vm = this;
        vm.user = $rootScope.globals.currentUser;
        vm.logout = logout;
        initState();

        function setPrice() {
            CommonSettingService.setPricePerMin(vm.newPricePerMin)
                .then(function (response) {
                    if (response.success) {
                        vm.pricePerMin = vm.newPricePerMin;
                    }
                });
        }

        function setTemperature() {
            CommonSettingService.setTemperature(vm.newMode, vm.newLowTemp, vm.newHighTemp, vm.newDefaultTemp)
                .then(function(response)  {
                    if (response.success) {
                        vm.mode = vm.newMode;
                        vm.lowTemp = vm.newLowTemp;
                        vm.highTemp = vm.newHighTemp;
                        vm.defaultTemp = vm.newDefaultTemp;
                    }
                });
        }

        function setSpeed() {
            CommonSettingService.setSpeed(vm.newLowSpeed, vm.newMidSpeed, vm.newHighSpeed) 
                .then(function(response) {
                    if (response.success) {
                        vm.lowSpeed = vm.newLowSpeed;
                        vm.midSpeed = vm.newMidSpeed;
                        vm.highSpeed = vm.newHighSpeed;
                    }
                });
        }

        function initState() {
            CommonSettingService.getInitCommonSetting()
                .then(function(response) {
                    if (response.success) {
                        var data = response.data;
                        vm.mode = data.mode;
                        vm.lowTemp = data.lowTemp;
                        vm.highTemp = data.highTemp;
                        vm.defaultTemp = data.defaultTemp;
                        
                        vm.lowSpeed = data.lowSpeed;
                        vm.midSpeed = data.midSpeed;
                        vm.highSpeed = data.highSpeed;

                        vm.pricePerMin = data.pricePerMin;
                    }
                });
        }

        function logout() {
            AuthenticationService.ClearCredentials();
            location.reload();
        }
    }

})();

