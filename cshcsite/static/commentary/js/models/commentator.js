/*
The model representing a single match commentator.
*/

window.CSHC = window.CSHC || {}
window.CSHC.Models = window.CSHC.Models || {}

CSHC.Models.Commentator = Backbone.Model.extend({

    urlRoot: function() {
        return '/commentary/' + this.get('match') + '/commentator/';
    },

    defaults: function() {
        return {
            commentator: null,
            commentator_name: '',
            match: null
        };
    },

    initialize: function() {
        console.log('Commentator.initialize()');
        this.on("change", function() {
            console.log('Commentator Model Changed');
        });
        this.on("invalid", function(model, error) {
            console.log('Invalid commentator: ' + error);
        });
        this.on("error", function(model, xhr, opyions) {
            console.log('Commentator save failed: ' + xhr);
        });
    },

    validate: function(attrs) {
        if(!attrs.commentator){
            return 'The commentator must be specified';
        }
        if(!attrs.match){
            return 'The commentator must be associated with a match';
        }
    },

    toJSON: function(options) {
      return _.clone(this.attributes);
    },

});