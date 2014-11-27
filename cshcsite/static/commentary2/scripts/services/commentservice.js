/*
Encapsulates the match commentary RESTful API
*/

// app.factory('commentsFactory', ['$resource', function($resource) {
//   return $resource('/commentary/:matchId/:commentId', {matchId: context.match_id, commentId: '@id'})
// }]);

app.factory('commentsFactory', function($resource) {
  return $resource("/commentary/comments/" + context.match_id + "/:id/",
    {id: "@_id"}, {
      save: {
        method: 'POST',
        transformRequest: function(data) {
          if (data === undefined)
            return data;

          var fd = new FormData();
          angular.forEach(data, function(value, key) {
            if (value instanceof FileList) {
              if (value.length == 1) {
                fd.append(key, value[0]);
              } else {
                angular.forEach(value, function(file, index) {
                  fd.append(key + '_' + index, file);
                });
              }
            } else {
              fd.append(key, value);
            }
          });

          return fd;
        },
        headers: {'Content-Type': undefined}
      }
    });
});

app.factory('commentatorsFactory', function($resource){
  return $resource("/commentary/commentators/" + context.match_id + "/:id/");
});
