
var app = angular.module('commentaryApp', ['ngAnimate', 'ngResource']);

// Need to handle Django's CSRF protection
// Ref: http://ozkatz.github.io/backbonejs-with-django-15.html
app.config(['$httpProvider',
    function($httpProvider) {
        var token = $('meta[name="csrf-token"]').attr('content');
        $httpProvider.defaults.headers.common['X-CSRFToken'] = token;
}])

app.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

