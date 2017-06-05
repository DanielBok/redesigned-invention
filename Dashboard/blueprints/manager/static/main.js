let app = angular.module('managerApp', ['ngTable']);

app.config(($interpolateProvider) => {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});
