/*
The main AngularJS controller for live match comments
*/

var REFRESH_INTERVAL_MS = 30000;

app.controller('CommentsController', function($scope, $timeout, LiveComment, Commentator, fileReader) {
  init();

  function init() {
    $scope.comments = [];
    $scope.last_update = new Date();
    $scope.context = context;
    $scope.user = { 'id': context.user_id, 'name': context.user_name };
    $scope.commentator = null;
    resetNewComment();
    refresh();
    $scope.access = get_access();
    $('.comment-option').tooltip()
  }

  function resetNewComment(){
    $scope.error = null;
    $scope.new_comment = new LiveComment();
    $scope.new_comment.comment_type = 2;
    $scope.new_comment.author = $scope.user.id;
    $scope.new_comment.author_name = $scope.user.name;
    $scope.new_comment.match = $scope.context.match_id;
    // Important: don't specify the photo attribute (i.e. don't set it to null)
    // Otherwise the Django Rest Framework view expects a photo file!
  }

  function get_access(){
    if(!$scope.user.id){
      return 'not_authenticated';
    }
    else if(!$scope.commentator){
      return 'no_commentator';
    }
    else if($scope.user.id != $scope.commentator.commentator){
      return 'other_commentator';
    }
    else{
      return 'commentating';
    }
  };

  $scope.commenter = function(comment){
    return comment.author_name.substr(0,comment.author_name.indexOf(' '));
  };

  $scope.showDelete = function(comment){
    // Users can always delete their own comment
    if(comment.author == $scope.user.id){
      return true;
    }
    return $scope.access == 'commentating' && $scope.context.commentary_is_active;
  };

  $scope.opp_score = function(index){
    return $scope.comments.slice(index).filter(function (comment) {
      return comment.comment_type == 1;
    }).length;
  };

  $scope.setType = function(comment_type){
    $scope.new_comment.comment_type = comment_type;
  }

  $scope.startScoring = function(){
    $scope.error = null;
    commentator = new Commentator();
    commentator.commentator = $scope.user.id;
    commentator.commentator_name = $scope.user.name;
    commentator.match = $scope.context.match_id;
    commentator.$save(
      function(response){
        console.log("Saved new commentator");
        $scope.commentator = response;
        $scope.access = get_access();
      },
      function(error){
        console.log("Failed to save new commentator: " + error);
        $scope.error = "Sorry - something went wrong. Maybe someone else just beat you to it?";
      });
  };

  $scope.stopScoring = function(){
    $scope.error = null;
    $scope.commentator.$delete({id:$scope.commentator.id},
      function(){
        console.log("Commentator deleted");
        $scope.new_comment.comment_type = 2;
        $scope.commentator = null;
        $scope.access = get_access();
      },
      function(error){
        console.log("Failed to delete commentator: " + error);
        $scope.error = "Sorry - something went wrong";
      });
  };

  $scope.postComment = function() {
    console.debug("Posting comment");
    $scope.error = null;
    $scope.new_comment.$save(
      function(response){
        console.log("Saved new comment");
        addComment(response);
        $scope.last_update = new Date();
      },
      function(error){
        console.log("Failed to post comment: " + error);
        $scope.error = "Sorry - something went wrong";
      });
    resetNewComment();
    $scope.imageSrc = null;
  };

  $scope.deleteComment = function(comment) {
    console.debug("Deleting comment: " + comment.id);
    $scope.error = null;
    comment.$delete({id:comment.id},
      function(response){
        console.log("Comment deleted");
        removeComment(response);
        $scope.last_update = new Date();
      },
      function(error){
        console.log("Failed to delete comment: " + error);
        $scope.error = "Sorry - something went wrong";
      });
  };

  // Function to replicate setInterval using $timeout service.
  $scope.scheduleRefresh = function(){
    $scope.refresh_promise = $timeout(function() {
      $scope.refresh_promise = null;
      $scope.refresh();
    }, REFRESH_INTERVAL_MS);
  };

  $scope.toggleRefresh = function(){
    // Cancel any scheduled refresh first
    if($scope.refresh_promise){
      $timeout.cancel($scope.refresh_promise);
      $scope.refresh_promise = null;
    }
    if(!$scope.auto_refresh){
      $scope.auto_refresh = true;
      $scope.scheduleRefresh();
    }
    else{
      $scope.auto_refresh = false;
    }
  };

  $scope.refresh = function(){
    refresh();
  };

  function refresh(){
    console.log("Refreshing comments...");
    $("#list-refresh-icon").addClass('icon-spin');
    $scope.error = null;
    var commentators = Commentator.query(
      function(){
        console.log("Retrieved match commentator");
        if (commentators.length > 0){
          $scope.commentator = commentators[0];
          $scope.access = get_access();
        }
        else{
          $scope.commentator = null;
          $scope.access = get_access();
        }
      },
      function(error){
        console.log("Failed to get commentators: " + error);
        $scope.error = "Sorry - something went wrong";
      });

    var comments_on_server = LiveComment.query(
      function() {
        console.log("Retrieved match comments");
        to_remove = comment_difference($scope.comments, comments_on_server);
        to_add = comment_difference(comments_on_server, $scope.comments);
        _.each(to_remove, function(comment, index, list){ removeComment(comment) });
        _.each(to_add, function(comment, index, list){ addComment(comment) });
        $("#list-refresh-icon").removeClass('icon-spin');
      },
      function(error){
        console.log("Failed to get comments: " + error);
        $scope.error = "Sorry - something went wrong";
      });

    if($scope.auto_refresh && !$scope.refresh_promise){
      $scope.scheduleRefresh();
    }
    $scope.last_update = new Date();
  }

  $scope.getFile = function() {
    $scope.progress = 0;
    fileReader.readAsDataUrl($scope.file, $scope)
    .then(function(result) {
      $scope.imageSrc = result;
      $scope.new_comment.photo = $scope.file;
    });
  };

  function comment_difference(array, rest) {
    return _.filter(array, function(value){
      return !_.find(rest, function(v) { return value.id == v.id;});
    });
  };

  function removeComment(comment) {
    for (var i = $scope.comments.length - 1; i >= 0; i--) {
      if ($scope.comments[i].id === comment.id) {
        $scope.comments.splice(i, 1);
        break;
      }
    }
  }

  function addComment(comment){
    for (var i = 0; i < $scope.comments.length; i++) {
      if($scope.comments[i].timestamp < comment.timestamp){
        $scope.comments.splice(i, 0, comment);
        return;
      }
    }
    $scope.comments.push(comment);
  }

});
