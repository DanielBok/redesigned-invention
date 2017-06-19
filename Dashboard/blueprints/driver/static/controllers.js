// Controller for driver
app.controller("driverCtrl", ($scope, $http) => {
    $scope.loading = true;
    $scope.ready = false;
    $scope.name = "";
    $scope.task = {
        containers: null,
        destination: null,
        source: null,
        ready_time: null,
        task_id: null
    };

    $http.get(api('drivers')).then(
        (res) => {
            console.log(res);
            $scope.loading = false;
            if (res.data.drivers[0].status!='Off Work') {
              $scope.ready = true;
              $scope.refreshTasks();
            } else{
              $scope.ready = false;
            };
            //console.log(res.data.drivers[0].status)
        },
        (err) => {
            console.error('error', err);
            $scope.loading = false;
        }
    );
    //$scope.done = false;


    $scope.setReady = function() {
        if ($scope.ready){
            let payload = {
                name: $scope.name,
                activity: "stop"
            };
            $http.post(api('drivers'), payload).then(
              (res) => {
                  console.log(res);
              },
              (err) => {
                  console.error('error', err);
              }
            );
            $scope.ready = false;

        } else {
            let payload = {
                name: $scope.name,
                activity: "start"
            };
            $http.post(api('drivers'), payload).then(
              (res) => {
                  console.log(res);
                  if (res.data.task == null) {
                      $scope.done = true;
                  } else {
                      $scope.task = res.data.task;
                      $scope.done = false;
                  };
              },
              (err) => {
                  console.error('error', err);
              }
            );
            $scope.ready = true;
        };
    };

    $scope.completeTask = function () {
        $scope.loading = true;
        let payload = {
            name: $scope.name,
            activity: 'complete'
        };
        $http.post(api('drivers'), payload).then(
          (res) => {
              console.log(res);
              if (res.data.task == null){
                  $scope.done = true;
              } else {
                  $scope.task = res.data.task;
                  $scope.done = false;
              };
          },
          (err) => {
              console.error('error', err);
          }
        );
        $scope.loading = false;
        Materialize.toast('Task completed!', 2000)
    };

    $scope.refreshTasks = function () {
        $scope.loading = true;
        let payload = {
            name: $scope.name,
            activity: 'get_task'
        };
        $http.post(api('drivers'), payload).then(
          (res) => {
              console.log(res);
              if (res.data.task == null){
                  $scope.done = true;
              } else {
                  $scope.task = res.data.task;
                  $scope.done = false;
              };
          },
          (err) => {
              console.error('error', err);
          }
        );
        $scope.loading = false;
        Materialize.toast('Content refreshed!', 2000)
    };
});
