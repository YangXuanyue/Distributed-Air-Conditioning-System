(function () {
    'use strict';

    angular
        .module('app')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['UserService', '$location', '$rootScope', 'FlashService'];
    function RegisterController(UserService, $location, $rootScope, FlashService) {
        var vm = this;

        vm.register = register;

        function register() {
            vm.dataLoading = true;
            UserService.Create(vm.user)
                .then(function (response) {
                    console.log(response);
                    if (response.data!=='false') {
                        FlashService.Success('注册成功!', true);
                        $location.path('/login');
                    } else {
                        FlashService.Error('用户名已经被注册！',false);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();
