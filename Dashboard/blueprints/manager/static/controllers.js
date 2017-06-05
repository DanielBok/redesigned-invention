// Controller for allocation
app.controller("allocCtrl", ($scope, $http) => {
    $scope.loading = true;
    let jq = $.noConflict();

    $http.get(api('schedule')).then(
        (res) => {
            console.log(res);
            $scope.schedule = res.data.flights;
            // setTimeout(() => jq('select').material_select(), 500);
            $scope.loading = false;
        },
        (err) => {
            console.error('error', err);
        }
    );

    $scope.print = function () {
        window.print();
    };

    $scope.query = {text: ""};
    $scope.$watch('query.text', () => {
        setTimeout(() => jq('select').material_select(), 150);
    });

    $scope.search_ = function (row) {
        // baseline condition, there's nothing
        if ($scope.query.text.trim() === "")
            return true;

        let text = $scope.query.text.toLowerCase(); // query

        // check if any field contains query. If so, return row
        for (let key in row)
            if (row.hasOwnProperty(key)) {
                let value = "";
                switch (key) {
                    case "TIME":
                        value = (new Date(row[key])).toISOString().replace('T', ' ').substr(0, 19);
                        break;
                    case "CONTAINERS":
                        continue;
                    default:
                        value = row[key].toLowerCase();
                }
                if (value.includes(text))
                    return true;
            }
        return false;
    }
});

// Controller for available
app.controller("availCtrl", ($scope, $http) => {
    $scope.loading = true;
    $scope.status = {
        editing: false,
        sending: false,
        send_done: false
    };

    let jq = $.noConflict();

    $http.get(api('workers')).then(
        res => {
            $scope.loading = false;
            $scope.drivers = res.data.workers;
            $scope.num_drivers = res.data.num_workers;
            console.log(res.data);
        },
        err => {
            console.error(err)
        }
    );

    $scope.range = function (n) {
        let arr = new Array(n);
        return [...arr.keys()];
    };

    $scope.toggleEdit = function () {
        $scope.status.send_done = false;
        if ($scope.status.editing) { // was editing, now complete.

            // json payload to server
            let payload = {
                workers: {
                    on: $scope.drivers.on,
                    off: $scope.drivers.off
                }
            };

            $scope.status.sending = true;
            $http.post(api('workers'), payload).then(
                res => {
                    $scope.status = {
                        editing: false,
                        sending: false,
                        send_done: true
                    };
                },
                err => {
                    console.error(err);
                }
            );
        } else {
            $scope.status.editing = true;
        }
    };
    $scope.swap = function (index, flag) {
        if (flag === 0) {
            // Item was moved from on -> off
            let worker = $scope.drivers.on[index];
            $scope.drivers.on.splice(index, 1);
            $scope.drivers.off.push(worker);
        } else {
            // Item was moved from off -> on
            let worker = $scope.drivers.off[index];
            $scope.drivers.off.splice(index, 1);
            $scope.drivers.on.push(worker);
        }
        // console.log(index, worker);
    };

});

// Controller for flight schedules
app.controller('fsCtrl', ($scope, $http, $location, NgTableParams) => {
    $scope.fs = {
        data: [],
        loading: true,
        type: ['Arrival', 'Departure']
    };

    $scope.terminals = [{
        name: 'Terminal 2',
        value: 'T2'
    },
        {
            name: 'Terminal 3',
            value: 'T3'
        }
    ];

    $scope.t = $scope.terminals[0];

    $scope.terminal2 = true;
    $scope.toggleTerminal = function (v) {
        $scope.terminal2 = !$scope.terminal2;
        $scope.t = $scope.terminals[v];
    };

    $http.get(api('flights')).then(
        (res) => {
            console.log(res);
            $scope.schedule = res.data.schedule;
            $scope.currentTerminal = true;
            $scope.fs.loading = false;
        },
        (err) => {
            console.error('error\n', err);
        }
    );
});


// Controller for taskboard
app.controller('tbCtrl', ($scope, $http) => {
    $scope.loading = true;
    let jq = $.noConflict();

    $http.get(api('drivers')).then(
        (res) => {
            console.log(res);
            $scope.drivers = res.data.drivers;
            $scope.loading = false;
        },
        (err) => {
            console.error('error', err);
            $scope.loading = false;
        }
    );

    $http.get(api('tasks')).then(
        (res) => {
            // console.log(res);
            $scope.tasks = res.data.tasks;
            setTimeout(() => jq('select').material_select(), 500);
            $scope.loading = false;
        },
        (err) => {
            console.error('error', err);
            $scope.loading = false;
        }
    );

});

// Magic controller for testing purposes
app.controller('managerMasterCtrl', ($scope, $http) => {
    $scope.loading = true;
    $scope.drivers = [];
    $scope.disabled_ = [];

    $http.get(api('drivers', {type: 'all'})).then(
        res => {
            console.log(res);
            $scope.drivers = res.data.drivers;
            $scope.drivers.forEach(() => $scope.disabled_.push(false));
            $scope.loading = false;
        },
        err => {
            console.error('error', err);
            $scope.loading = false;
        }
    );

    $scope.isReadyOrWorking = (text) => {
        text = text.toLowerCase();
        return text.startsWith("on") || text.startsWith("ready");
    };

    $scope.update_driver = (i) => {
        let driver = $scope.drivers[i];
        $scope.disabled_[i] = true;
        driver.activity = $scope.isReadyOrWorking(driver.status) ? 'stop' : 'start';

        $http.post(api('drivers'), driver).then(
            res => {
                $scope.disabled_[i] = false;
                $scope.drivers[i] = res.data.driver;
            },
            err => {
                console.error(err);
            }
        );
    }

});
