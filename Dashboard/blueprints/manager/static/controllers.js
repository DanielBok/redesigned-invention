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

            let time_now = new Date();
            let tz_offset = -time_now.getTimezoneOffset() / 60;
            tz_offset = tz_offset > 0 ? `+0${tz_offset}00` : `-0${tz_offset}00`;

            $scope.schedule = res.data.schedule;

            res.data.schedule.forEach(e => {
                e.scheduled_time = (new Date(`${e.scheduled_time}${tz_offset}`)).toGMTString();
                e.actual_time = (new Date(`${e.actual_time}${tz_offset}`)).toGMTString();
            });

            $scope.currentTerminal = true;
            $scope.fs.loading = false;
        },
        (err) => {
            console.error('error\n', err);
        }
    );
});

// Controller for taskboard
app.controller('tbCtrl', ($scope, $http, $interval, $q) => {
    $scope.loading = true;
    $scope.disableAllocateButton = true;
    $scope.editing = false;

    let make_tasks_aware_tz = tasks => {
        let time_now = new Date();
        let tz_offset = -time_now.getTimezoneOffset() / 60;
        tz_offset = tz_offset > 0 ? `+0${tz_offset}00` : `-0${tz_offset}00`;

        tasks.forEach(e => {
            e.flight_time = (new Date(`${e.flight_time}${tz_offset}`)).toGMTString();
            e.ready_time = (new Date(`${e.ready_time}${tz_offset}`)).toGMTString();
        })
    };

    $scope.loadTaskBoard = () => {

        $http.get(api('tasks', {type: 'all'})).then(res => {
            let tasks = res.data;
            $scope.tasks = tasks.tasks;

            make_tasks_aware_tz($scope.tasks);
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
        // console.log("deallocate driver: ", task.driver);
        $scope.updateDeallocatedDriver = task.driver;
        task.driver = null;
        $scope.disableAllocateButton = false;
    };

    $scope.allocate = (task) => {
        // console.log("allocate driver to: ", task.task_id);
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
                // console.log(res);
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
        let time_now = new Date();
        let tz_offset = -time_now.getTimezoneOffset() / 60;
        tz_offset = tz_offset > 0 ? `+0${tz_offset}00` : `-0${tz_offset}00`;

        $scope.tasks.forEach(task => {
            let task_time = new Date(`${task.flight_time}${tz_offset}`);
            let remaining = Math.round((task_time - time_now) / 60000);
            if (remaining < 0) {
                task.flag = -1; // overdue task
            } else if (remaining < 20) {
                task.flag = 1; // urgent task
            } else {
                task.flag = 0; // normal task
            }
        })
    };

    $scope.loadTaskBoard(); // first load

    $interval(function () {
        // Call interval function only after first load
        if (!$scope.editing && !$scope.loading) {
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
            // console.log(res);
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
