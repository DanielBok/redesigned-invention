let app = angular.module('statsApp', ['chart.js']);

app.config(($interpolateProvider) => {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});
