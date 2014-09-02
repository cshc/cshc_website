/* Backbone.js-based code for the match commentary feature in a match details page
*/


// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    var Comment = Backbone.Model.extend({

    });

    var CommentList = Backbone.Collection.extend({

        model: Comment,
    });

    var Comments = new CommentList;

    var CommentView = Backbone.View.extend({

    });

    var CommentListView = Backbone.View.extend({

    });

    var CommentList = new CommentListView;

    // Need to handle Django's CSRF protection
    // Ref: http://ozkatz.github.io/backbonejs-with-django-15.html
    var _sync = Backbone.sync;
    Backbone.sync = function(method, model, options){
        options.beforeSend = function(xhr){
            var token = $('meta[name="csrf-token"]').attr('content');
            xhr.setRequestHeader('X-CSRFToken', token);
        };
        return _sync(method, model, options);
    };
});