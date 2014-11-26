/*
The collection representing several match comments.
*/

window.CSHC = window.CSHC || {}
window.CSHC.Models = window.CSHC.Models || {}
window.CSHC.Collections = window.CSHC.Collections || {}

CSHC.Collections.MatchComments = Backbone.Collection.extend({

    model: CSHC.Models.Comment,

    url: function(){
        if (this.last_fetch == null){
            return '/commentary/' + this.match + '/';
        }
        else {
            return '/commentary/' + this.match + '/since/' + this.last_fetch.getTime() + '/';
        }
    },

    initialize: function(models, options) {
        options = options || {};
        if (options.match){
            this.match = options.match;
        }
        this.last_fetch = new Date();
        console.log('MatchComments.initialize()');
        this.on("add", function() {
            console.log('Comment added to collection');
        });
        this.on("remove", function() {
            console.log('Comment removed from collection');
        });
    },

    // parse: function(resp, options) {
    //     return resp.results;
    // },

    our_score: function(id) {
        return _.filter(this.models, function(comment){
            return comment.get('id') <= id && comment.get('comment_type') == 0;
        }).length;
    },

    opp_score: function(id) {
        return _.filter(this.models, function(comment){
            return comment.get('id') <= id && comment.get('comment_type') == 1;
        }).length;
    },

    update_last_fetch: function(){
        this.last_fetch = new Date();
        this.trigger('updated');
    },

    // Comments are sorted by descending timestamp order.
    comparator: function(a, b){
        return new Date(a.timestamp) < new Date(b.timestamp) ? -1 : 1;
    },
});