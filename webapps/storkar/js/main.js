require.config({
    paths: {
        jquery: 'libs/jquery/jquery',
        underscore: 'libs/lodash/lodash',
        lodash: 'libs/lodash/lodash',
        backbone: 'libs/backbone/backbone',
        layoutmanager: 'libs/layoutmanager/backbone.layoutmanager'
    }
});

define([
    'jquery',
    'underscore',
    'backbone',
    'app',
    'router'
],
function($, _, Backbone, App, AppRouter)
{
    var promise = App.initialize();

    $.when(promise).then(function() {
        var app_router = new AppRouter();
        App.router = app_router;
        Backbone.history.start({pushState: false, root: '/'});
    });
});
