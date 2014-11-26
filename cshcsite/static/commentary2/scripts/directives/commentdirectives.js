/*
AngularJS directives relating to match commentary
*/

app.directive("ngFileSelect", function() {
  return {
    link: function($scope, el) {
      el.bind("change", function(e) {
        $scope.file = (e.srcElement || e.target).files[0];
        $scope.getFile();
      })
    }
  }
});

// Ref: http://stackoverflow.com/a/17472118
app.directive('bindKey', function() {
  return function(scope, element, attrs) {
    element.bind("keydown keypress", function(event) {
      if(event.which ===  Number(attrs.key) && !event.ctrlKey) {
        scope.$apply(function(){
          scope.$eval(attrs.bindKey, {'event': event});
        });

        event.preventDefault();
      }
    });
  };
});