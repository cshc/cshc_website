/*
The view of multiple match comments.
*/

window.CSHC = window.CSHC || {}
window.CSHC.Views = window.CSHC.Views || {}

CSHC.Views.MatchCommentsView = Backbone.View.extend({
    el: $( '#match-comments' ),

    statsTemplate: _.template( $('#comment-stats-template').html() ),

    initialize: function() {
        this.$list_div = this.$('#live-comment-list');
        this.$stats_div = this.$('#comment-stats');
        this.collection = new CSHC.Collections.MatchComments([], {'match': match_id});
        this.collection.fetch({
                success: function(collection){
                    console.log('Fetched comments');
                    collection.update_last_fetch();
                },
                error: function(collection){
                    console.log('Failed to get comments');
                }
            });
        this.render();

        this.listenTo( this.collection, 'add', this.renderComment );
        this.listenTo( this.collection, 'reset', this.render );
        this.listenTo( this.collection, 'updated', this.renderStats );
    },

    render: function() {
        console.log("Rendering comment list");
        this.collection.each(function( item ) {
            this.renderComment( item );
        }, this );
    },

    renderComment: function( item ) {
        console.log("Rendering comment[" + item.id + "]");
        var commentView = new CSHC.Views.CommentView({
            model: item
        });
        this.$list_div.append( commentView.render().el );
    },

    renderStats: function(){
        console.log("Rendering comment stats");
        stats_ctx = {last_update: this.collection.last_fetch.getHours() + ":" + this.collection.last_fetch.getMinutes()};
        this.$stats_div.html(this.statsTemplate(stats_ctx));
    },
});