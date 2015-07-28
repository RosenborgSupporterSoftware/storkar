require.config({
    baseUrl: '/js/',
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
    'layoutmanager',
    'app',
    'router'
],
function($, _, Backbone, Layout, App, Router)
{
    var promise = App.initialize();

    $.when(promise).then(function() {
        var router = new Router();
        App.router = router;
        Backbone.history.start({pushState: false, root: '/'});
    });
});
