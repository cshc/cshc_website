/*
Encapsulates the match commentary RESTful API
*/

// app.factory('commentsFactory', ['$resource', function($resource) {
//   return $resource('/commentary/:matchId/:commentId', {matchId: context.match_id, commentId: '@id'})
// }]);

app.factory('commentsFactory', function($resource) {
  return $resource("/commentary/comments/" + context.match_id + "/:id/");
});

app.factory('commentatorsFactory', function($resource){
  return $resource("/commentary/commentators/" + context.match_id + "/:id/");
});
