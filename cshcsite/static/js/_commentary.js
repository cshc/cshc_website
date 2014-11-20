/* Backbone.js-based code for the match commentary feature in a match details page
*/

// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    window.CSHC = {
        Models: {},
        Collections: {},
        Views: {}
    };

    CSHC.Models.Comment = Backbone.Model.extend({

        urlRoot: function() {
            return '/matches/' + this.get('match') + '/comments/';
        },

        initialize: function() {
            console.log('a new comment');
            this.on("change", function() {
                console.log('Comment Model Changed');
            });
            this.on("invalid", function(model, error) {
                console.log('Invalid comment: ' + error);
            });
            this.on("error", function(model, xhr, opyions) {
                console.log('Save failed: ' + xhr);
            });
        },

        // Default attributes for the comment item.
        defaults: function() {
          return {
            author: null,
            match: null,
            comment_type: 0,
            comment: "",
            photo_url: "",
            state: "Pending",
            timestamp: null,
            last_modified: null
          };
        },

        validate: function(attrs) {
            if(attrs.author == null){
                return 'The comment author must be specified';
            }
        }

    });

    CSHC.Collections.CommentList = Backbone.Collection.extend({

        model: CSHC.Models.Comment,

        url: function(){
            if (this.last_fetch == null){
                return '/matches/' + this.match + '/comments/';
            }
            else {
                return '/matches/' + this.match + '/comments/since/' + this.last_fetch.getTime() + '/';
            }
        },

        initialize: function(models, options) {
            options || (options = {});
            if (options.match){
                this.match = options.match;
            }
            this.last_fetch = null;
            console.log('a new comment collection');
            this.on("add", function() {
                console.log('Comment added to collection');
            });
            this.on("remove", function() {
                console.log('Comment removed from collection');
            });
        },

        // Comments are sorted by descending timestamp order.
        comparator: function(a, b){
            return new Date(a.timestamp) < new Date(b.timestamp) ? -1 : 1;
        }
    });

    var comments = new CSHC.Collections.CommentList([], {'match': match_id});

    CSHC.Views.CommentView = Backbone.View.extend({

        tagName: 'li',
        className: '',
        id: function(){
            return 'match-comment-' + this.model.get('id');
        },

        template: _.template($('#comment-template').html()),

        initialize: function(){
            console.log('CommentView created');
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.remove);
        },

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    CSHC.Views.CommentListView = Backbone.View.extend({

        el: $("#match-comments"),

        statsTemplate: _.template($('#comment-list-template').html()),

        initialize: function(){
            console.log('CommentListView created');

            this.listenTo(comments, 'add', this.addOne);
            this.listenTo(comments, 'all', this.render);

            comments.fetch({
                success: function(collection){
                    console.log('Fetched comments');
                    collection.last_fetch = new Date();
                },
                error: function(collection){
                    console.log('Failed to get comments');
                }
            });
        },

        render: function() {
            this.$('#match-comment-stats').html(this.statsTemplate(this.collection));
            return this;
        },

        addOne: function(comment) {
            var view = new CSHC.Views.CommentView({model: comment});
            this.$("#match-comment-list").append(view.render().el);
        }
    });

    var commentList = new CSHC.Views.CommentListView({collection: comments});

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