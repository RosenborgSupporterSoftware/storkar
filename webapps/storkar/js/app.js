define([
    'jquery',
    'underscore',
    'backbone',
    'router',
    'layoutmanager'
],

function($, _, Backbone, Router, Layout) {

    var App = {};

    App._cacheTemplates = [
        'player/list.html',
        'player/item.html'
    ];

    App.cacheTemplates = function() {
        _.each(App._cacheTemplates, function(path) {
            $.get('/js/templates/' + path, function(contents) {
                Layout.cache('/js/templates/' + path,
                             _.template(contents));
            }, "text");
        });
    };

    App.initialize = function() {
        App.router = Router;
        App.layout = Layout;
        App.cacheTemplates();

        Router.initialize();

        Layout.configure({
            manage: true,

            prefix: "/js/templates/"
        });
    };

    return App;
});

