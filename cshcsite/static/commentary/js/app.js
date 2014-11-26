
$(function() {

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

    comments_view = new window.CSHC.Views.MatchCommentsView();
});