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
app.controller('tbCtrl', ($scope, $http , $interval) => {
    $scope.loading = true;
    let jq = $.noConflict();
    $scope.editing = false;
    $scope.free = null;

    $scope.loadTaskBoard = () => {
        $http.get(api('tasks', {type: 'all'})).then(
            (res) => {
                console.log("Tasks ", res);
                $scope.tasks = res.data.tasks;
                setTimeout(() => jq('select').material_select(), 500);
            },
            (err) => {
                console.error('error', err);
            }
        );

        $http.get(api('drivers')).then(
            (res) => {
                console.log("Drivers ", res);
                $scope.drivers = res.data.drivers;
            },
            (err) => {
                console.error('error', err);
            }
        );
        $scope.changeDriver = (newDriver) => {
            $scope.test = newDriver;
        };
        $scope.loading = false
    };

    $scope.deallocate = (task) => {
        console.log("deallocate driver: ", task.driver)
        $scope.updateDeallocatedDriver = task.driver
        $scope.free = task.driver;
        task.driver = null;
    };

    $scope.allocate = (task) => {
        console.log("allocate driver to: ", task.task_id)
        $scope.updateAllocatedTask = task.task_id
        task.driver = $scope.free;
        $scope.free = null;
    };

    $scope.toggleEdit = () => {
        $scope.editing = !$scope.editing;
    };

    $scope.submit = () => {
        let payload = {
            name: $scope.updateDeallocatedDriver,
            activity: "update",
            target: $scope.updateAllocatedTask
        };
        $scope.toggleEdit();
        $http.post(api('drivers'), payload).then(
            (res) => {
                console.log(res);
            },
            (err) => {
                console.error('error', err);
            }
        );
    };

    $scope.cancel = () => {
        $scope.toggleEdit();
    };

    //$scope.loadTaskBoard();

    $interval(function() {
    	if (!$scope.editing){
    		$scope.loadTaskBoard();
    	}
     }, 5000);

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
