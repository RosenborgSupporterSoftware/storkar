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
        'player/frontpage.html',
        'player/list.html',
        'player/listitem.html',
        'player/details.html',
        'player/editor.html',
        'misc/frontpage.html'
    ];

    App.players = null;

    App.teams = null;

    App.cacheTemplates = function() {
        var promise = null;
        _.each(App._cacheTemplates, function(path) {
            var p = '/js/templates/' + path;
            promise = $.get(p, function(contents) {
                Layout.cache(p, _.template(contents));
            }, "text");
        });
        return promise;
    };

    App.initialize = function(options) {
        Layout.configure({
            manage: true,

            prefix: "/js/templates/",

            fetchTemplate: function(path) {
                var template = Layout.cache(path);
                if (!template) {
                    console.error("Template '" + path + "' not pre-cached! Edit app.js.");
                }
                return template;
            }
        });

        var promise = App.cacheTemplates();

        return promise;
    };

    return App;
});

