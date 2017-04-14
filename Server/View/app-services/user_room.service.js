(function() {
    'use strict';

    angular
        .module('app')
        .factory('RoomService', RoomService);

    WcpaService.$inject = ['$http', '$rootScope'];

    function RoomService($http, $rootScope) {
        var service = {};
        service.speedUp = speedUp;
        service.speedDown = speedDown;
        service.tempUp = tempUp;
        service.tempDown = tempDown;
        service.getCurTemp = getCurTemp;
        service.getCurSpeed = getCurSpeed;
        service.turnOn = turnOn;
        service.turnOff = turnOff;

        function turnOn() {
            return $http.post($rootScope.getUrl + 'turnon', {
                roomId : roomId
            }).then(handleSuccess, handleError('Error turn on'));
        }
        
        function turnOff() {
            return $http.post($rootScope.getUrl + 'turnoff', {
                roomId : roomId
            }).then(handleSuccess, handleError('Error turn off'));

            // 需返回账单信息
        }
        function speedUp() {
            return $http.post($rootScope.getUrl + 'speedup', {
                roomId : roomId
            }).then(handleSuccess, handleError('Error speed up'));
        }

        function speedDown($http, $rootScope) {
            return $http.post($rootScope.getUrl + 'speeddown', {
                roomId : roomId
            }).then(handleSuccess, handleError('Error speed down'));
        }

        function tempUp($http, $rootScope) {
            return $http.post($rootScope.getUrl + 'tempup', {
                roomId : roomId
            }).then(handleSuccess, handleError('Error temp up'));
        }
        function tempDown($http, $rootScope) {
            return $http.post($rootScope.getUrl + 'tempdown', {
                roomId : roomId
            }).then(handleSuccess, handleError('Error temp down'));
        }

        function getCurState($http, $rootScope) {
            return $http.post($rootScope.getUrl + 'cur_state', {
                roomId : roomId
            }).then(handleSuccess, handleError('Error speed up'));

            // json 如下：
            // { curTemp :curTemp,
            //   curPrice : curPrice,
            //   curMode : curMode}
        }



        return service;
        
    }
})();
