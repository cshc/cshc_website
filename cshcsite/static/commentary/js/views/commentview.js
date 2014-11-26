/*
The view of a single match comment.
*/

window.CSHC = window.CSHC || {}
window.CSHC.Views = window.CSHC.Views || {}

CSHC.Views.CommentView = Backbone.View.extend({

    tagName: 'div',
    className: 'media comment-item',
    template: _.template( $( '#match-comment-template' ).html()),

    events: {
        'click .delete': 'deleteComment'
    },

    deleteComment: function() {
        //Delete model
        this.model.destroy();

        //Delete view
        this.remove();
    },


    icon: function() {
        if(this.model.get('comment_type') == 0) {
            return 'icon-thumbs-up';
        }
        else if(this.model.get('comment_type') == 1) {
            return 'icon-thumbs-down';
        }
        else if(this.model.get('photo')) {
            return 'icon-camera';
        }
        else {
            return 'icon-edit';
        }
    },

    render: function() {
        context = this.model.toJSON();
        context.icon = this.icon();
        context.we_scored = context.comment_type == 0;
        context.they_scored = context.comment_type == 1;
        dt = new Date(Date.parse(context.timestamp));
        context.time = dt.getHours() + ":" + dt.getMinutes();

        // Scores are calculated based on the number of preceeding 'goal_scored'
        // and 'goal_conceded' comments.
        context.our_score = this.model.collection.our_score(context.id);
        context.opp_score = this.model.collection.opp_score(context.id);
        this.$el.html( this.template( context ) );

        return this;
    }
});