
var app = angular.module('commentaryApp', ['ngAnimate']);

// Should be automatically supplied by backend
var nextId = 1;

function defaultFor(arg, val) {
  return typeof arg !== 'undefined' ? arg : val;
}

function Comment(id, comment, we_scored, they_scored, photo) {
  this.id = id;
  this.comment = defaultFor(comment);
  this.we_scored = defaultFor(we_scored);
  this.they_scored = defaultFor(they_scored);
  this.photo = defaultFor(photo);
  this.update = !this.we_scored && !this.they_scored && !this.photo;
  this.timestamp = new Date();
}


Comment.prototype.toString = function() {
  return "\"" + this.comment + "\"";
};

app.service('commentsService', function() {
  this.getComments = function() {
    return comments;
  };

  this.insertComment = function(comment) {
    console.debug("Inserting comment " + comment.toString());
    comments.unshift(comment);
  };

  this.deleteComment = function(id) {
    for (var i = comments.length - 1; i >= 0; i--) {
      if (comments[i].id === id) {
        comments.splice(i, 1);
        break;
      }
    }
  };

  this.getComment = function(id) {
    for (var i = 0; i < comments.length; i++) {
      if (comments[i].id === id) {
        return comments[i];
      }
    }
    return null;
  };

  comments = [
    new Comment(nextId++, "Then I commented"),
    new Comment(nextId++, "We scored", true, false),
    new Comment(nextId++, "They scored", false, true),
  ];
});

app.controller('CommentsController', function($scope, commentsService, fileReader) {
  init();


  function init() {
    $scope.comments = commentsService.getComments();
    $scope.last_update = new Date();
    $scope.our_team = "Cambridge South M1";
    $scope.opp_team = "Ely City M2";
    $scope.new_comment_type = 'update';
    $scope.user = { 'id': 63, 'name': 'Graham McCulloch'};
    //$scope.scorer = { 'id': 95, 'name': 'Neil Sneade'};
    $scope.scorer = { 'id': 63, 'name': 'Graham McCulloch'};
    $scope.match_id = match_id;
  }

  $scope.our_score = function(index){
    return $scope.comments.slice(index).filter(function (comment) {
      return comment.we_scored;
    }).length;
  };

  $scope.opp_score = function(index){
    return $scope.comments.slice(index).filter(function (comment) {
      return comment.they_scored;
    }).length;
  };

  $scope.i_am_scorer = function(){
    return $scope.user && $scope.scorer && ($scope.user.id == $scope.scorer.id);
  };

  $scope.postComment = function() {
    console.debug("Posting comment");
    we_scored = $scope.new_comment_type == 'goal_scored';
    they_scored = $scope.new_comment_type == 'goal_conceded';
    var comment = new Comment(nextId++, $scope.new_comment, we_scored, they_scored, $scope.imageSrc);
    commentsService.insertComment(comment);
    $scope.new_comment = null;
    $scope.imageSrc = null;
    $scope.file = null;
    $scope.last_update = new Date();
    $scope.new_comment_type = 'update';
  };

  $scope.deleteComment = function(comment) {
    console.debug("Deleting comment: " + comment.id);
    commentsService.deleteComment(comment.id);
  };

  $scope.getFile = function() {
    $scope.progress = 0;
    fileReader.readAsDataUrl($scope.file, $scope)
      .then(function(result) {
        $scope.imageSrc = result;
      });
  };

});

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