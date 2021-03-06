(function() {
    'use strict';

    angular
        .module('app')
        .factory('RoomService', RoomService);

    function RoomService($http, $rootScope) {
        var service = {};
        service.getRooms = getRooms;
        service.show_log = show_log;
        return service;

        function show_log() {
            $http.post('/show_log', {}).then(handleSuccess, handleError('Error getRooms'));
        }
        function getRooms() {
            return $http.post('/get_rooms', {
            }).then(handleSuccess, handleError('Error getRooms'));
            // rooms[4];
            // { room.curState :
            //   room.curTemp :
            //   room.aimTemp :
            //   room.curSpeed : 
            // }
        }

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
