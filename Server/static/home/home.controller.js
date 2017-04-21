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
        vm.analyze = analyze;
        $interval(function() {
            roomMaintain();
        }, 100);

        (function init() {
            buildStates();
            initState();
            // var timer = $interval(roomMaintain(), 100);
        })();


        function analyze() {
            RoomService.show_log()
                .then(function (response) {
                    var state = response.data;
                    console.log(state);
                });
        }

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
                    //console.log(state);
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
            console.log("maintain");
            RoomService.getRooms()
                .then(function (response) {
                    var state = response.data;
                    console.log(state);
                    setRooms(state.data);
                });

            function setRooms(room) {
                vm.RoomState.rooms = room;
                console.log(vm.RoomState.rooms);
            }
        }
    }

})();


