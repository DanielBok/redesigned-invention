let app = angular.module('managerApp', []);

app.config(($interpolateProvider) => {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});
