// Controller for driver
app.controller("driverCtrl", ($scope, $http) => {
    $scope.loading = true;
    $scope.ready = false;

    $http.get(api('drivers')).then(
        (res) => {
            console.log(res);
            $scope.loading = false;
        },
        (err) => {
            console.error('error', err);
            $scope.loading = false;
        }
    );
    $scope.mockData = {
        Type: 'Arrival',
        Source: 'SQ123',
        Destination: 'HOTA',
        Time: '13:37',
        Containers: ['12345', '67890', '13337'],
    };

    $scope.done = false;

    $scope.passTask = function () {
        $scope.done = true;
    };
    $scope.completeTask = function () {
        $scope.done = true;
    };
    $scope.refreshTasks = function () {
        $scope.loading = true;
        // api call
        $scope.done = false;
        $scope.loading = false;
    };
});

