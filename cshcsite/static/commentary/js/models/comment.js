/*
The model representing a single match comment.
*/

window.CSHC = window.CSHC || {}
window.CSHC.Models = window.CSHC.Models || {}

CSHC.Models.Comment = Backbone.Model.extend({

    urlRoot: function() {
        return '/commentary/' + this.get('match') + '/';
    },

    defaults: function() {
        return {
            author: null,
            author_name: '',
            match: null,
            comment_type: 2,
            comment: "",
            photo: "",
            state: "Pending",
            timestamp: null,
            last_modified: null
        };
    },

    initialize: function() {
        console.log('Comment.initialize()');
        this.on("change", function() {
            console.log('Comment Model Changed');
        });
        this.on("invalid", function(model, error) {
            console.log('Invalid comment: ' + error);
        });
        this.on("error", function(model, xhr, opyions) {
            console.log('Comment save failed: ' + xhr);
        });
    },

    validate: function(attrs) {
        if(!attrs.author){
            return 'The comment author must be specified';
        }
        if(!attrs.match){
            return 'The comment must be associated with a match';
        }
    },

    toJSON: function(options) {
      return _.clone(this.attributes);
    },

});