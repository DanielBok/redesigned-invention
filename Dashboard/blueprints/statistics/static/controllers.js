app.controller("statsCtrl", ($scope, $http) => {
    $scope.loading = true;

    $scope.data = {
        driver: "",
        all: null
    };

    $scope.drivers = [];
    $scope.chart = {
        containers: null,
        date: null,
        options: {},
        series: $scope.data.driver
    };

    let chartChange = driver => {
        $scope.chart.series = driver;
        let data = $scope.data.all[driver];

        let time = data.ready_time.map(e => e.substr(0, 7));

        let x = [];
        let y = [];
        for(let i=0; i < time.length; i++) {
            let index = x.indexOf(time[i]);
            if (index === -1) {
                x.push(time[i]);
                y.push(data.containers[i]);
            } else {
                y[index] += data.containers[i];
            }
        }

        $scope.chart.date = x;
        $scope.chart.containers = y;
    };

    let url = `${location.protocol}//${location.host}/stats/dpdata`;
    let jq = $.noConflict();
    $http.get(url).then(
        (res) => {
            console.log(res);
            $scope.data.all = res.data;

            $scope.drivers = res.data.drivers;

            let drivers = {};
            res.data.drivers.forEach(e => drivers[e] = null);

            setTimeout(() => {
                jq('#autocomplete-driver').autocomplete({
                    data: drivers,
                    limit: 20,
                    onAutocomplete: function (driver) {
                        chartChange(driver);
                    }
                });
            }, 500);

            let r = Math.floor(Math.random() * $scope.drivers.length);
            $scope.data.driver = $scope.drivers[r];
            chartChange($scope.data.driver);

            $scope.loading = false;
        },
        (err) => {
            console.error('error', err);
            $scope.loading = false;
        }
    );

    $scope.driverChange = function () {
        if ($scope.drivers.indexOf($scope.data.driver) !== -1) {
            chartChange($scope.data.driver);
        }
    };

});
