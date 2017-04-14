(function() {
    'use strict';

    angular
        .module('app')
        .factory('CommonSettingService', CommonSettingService);

    function CommonSettingService($http, $rootScope) {
        var service = {};
        service.getInitCommonSetting = getInitCommonSetting;
        service.setPricePerMin = setPricePerMin;
        service.setTemperature = setTemperature;
        service.setSpeed = setSpeed;
        return service;
    
        function getInitCommonSetting() {
            return $http.post('/get_init', {
            }).then(handleSuccess, handleError('Error getInitCommonService'));
            //　返回ｊｓｏｎ如下：
            // ｛　mode　: mode, lowTemp : lowTemp, highTemp : highTemp, defaultTemp : defaultTemp,
            //    lowSpeed : lowSpeed, midSpeed : midSpeed, highSpeed : highSpeed. pricePerMin : pricePerMin };
        }

        function setPricePerMin(price) {
            return $http.post($rootScope.getUrl + 'set_price', {
                pricePerMin : price
            }).then(handleSuccess, handleError('Error tetPricePerMin'));
        }

        function setTemperature(mode, lowTemp, highTemp, defaultTemp) {
            return $http.post($rootScope.getUrl + 'set_temperature', {
                mode : mode,
                lowTemp : lowTemp,
                highTemp : highTemp,
                defaultTemp : defaultTemp
            }).then(handleSuccess, handleError('Error setTemperature'));
        }

        function setSpeed(lowSpeed, midSpeed, highSpeed) {
            return $http.post($rootScope.getUrl + 'set_speed', {
                lowSpeed : lowSpeed,
                midSpeed : midSpeed,
                highSpeed : highSpeed
            }).then(handleSuccess, handleError('Error setSpeed'));
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
