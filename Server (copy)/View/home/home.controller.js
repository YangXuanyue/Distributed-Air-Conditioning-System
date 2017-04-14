(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['UserService','$rootScope', '$cookieStore', '$interval', 'AuthenticationService','RoomService'
    ];

    function HomeController(UserService, $rootScope, $cookieStore, $interval, AuthenticationService, RoomService) {
        var vm = this;
        vm.user = $rootScope.globals.currentUser;
        vm.logout = logout;

        (function init() {
            buildStates();
            initState();
            var timer = $interval(roomMaintain(), 5000);
        })();

        function buildStates() {
            var RoomState = {};
            buildRoomState();

            vm.RoomState = RoomState;

            function buildRoomState() {
                RoomState.rooms = [];
            }
        }

        function initState() {
            RoomService.getRooms()
                .then(function (response) {
                    var state = response.data;
                    setRooms(state);
                });

            function setRooms(room) {
                vm.RoomState.rooms = room;
            }
        }

        function logout() {
            AuthenticationService.ClearCredentials();
            location.reload();
        }

        function roomMaintain() {
            RoomService.getRooms()
                .then(function (response) {
                    var state = response.data;
                    setRooms(state);
                });

            function setRooms(room) {
                vm.RoomState.rooms = room;
            }
        }
    }

})();

