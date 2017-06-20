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
app.controller('fsCtrl', ($scope, $http) => {
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
app.controller('tbCtrl', ($scope, $http , $interval, $q) => {
    $scope.loading = true;
    $scope.disableAllocateButton = true;
    $scope.editing = false;

    $scope.loadTaskBoard = () => {

        console.log("loading taskboard");
        // Resolve all your promises simultaneously.
        // Previous resolution was asynchronous and led to concurrency errors
        $q.all([
            $http.get(api('tasks', {type: 'all'})),
        ]).then(data => {
            let tasks = data[0].data;
            $scope.tasks = tasks.tasks;
            console.log("tasks: ", $scope.tasks)
            $scope.checkTimings();

        }, err => {
            console.error("ERROR", err);
        });

        $scope.changeDriver = (newDriver) => {
            $scope.test = newDriver;
        };
        $scope.loading = false
    };

    $scope.deallocate = (task) => {
        console.log("deallocate driver: ", task.driver);
        $scope.updateDeallocatedDriver = task.driver;
        task.driver = null;
        $scope.disableAllocateButton = false;
    };

    $scope.allocate = (task) => {
        console.log("allocate driver to: ", task.task_id);
        $scope.updateAllocatedTask = task.task_id;
        $scope.disableAllocateButton = true;
        task.driver = $scope.updateDeallocatedDriver;
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
        $scope.loadTaskBoard();
    };

    $scope.cancel = () => {
        $scope.toggleEdit();
        $scope.loadTaskBoard();
    };

    $scope.checkTimings = () => {
        var time_now = new Date();
        let tz_offset = -time_now.getTimezoneOffset() / 60;
        tz_offset = tz_offset > 0 ? `+0${tz_offset}00` : `-0${tz_offset}00`;
        console.log('time now:', time_now);
        $scope.tasks.forEach( task => {
            var task_time = new Date(`${task.flight_time}${tz_offset}`);
            var remaining = Math.round((task_time - time_now)/60000);
            if (remaining < 0){
                task.flag = -1; // overdue task
            } else if (remaining < 20) {
                task.flag = 1; // urgent task
            } else {
              task.flag = 0; // normal task
            };
        })
    };

    $scope.loadTaskBoard(); // first load

    $interval(function() {
      // Call interval function only after first load
    	if (!$scope.editing && !$scope.loading){
    		$scope.loadTaskBoard();
        Materialize.toast('Taskboard refreshed!', 2000)
    	}
    }, 20000);

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
