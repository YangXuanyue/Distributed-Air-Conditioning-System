(function () {
    'use strict';

    angular
        .module('app')
        .factory('ReportService', ReportService);

    ReportService.$inject = ['$http', '$rootScope'];

    function ReportService($http, $rootScope) {
        var service = {};

        service.getDailyReport = getDailyReport;
        service.getMonthlyReport = getMonthlyReport;
        return service;

        function getDailyReport() {
            return $http.post('/get_daily_report', {
            }).then(handleSuccess, handleError);
        }

        function getMonthlyReport() {
            return $http.post('/get_monthly_report', {
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
