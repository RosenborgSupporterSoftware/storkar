define(
    "app",
[
    'backbone',
    'router',
    'layoutmanager'
],
function(Backbone, Router, Layout) {

    var App = {};

    App._cacheTemplates = [
        'misc/frontpage.html',
        'player/frontpage.html',
        'player/list.html',
        'player/listitem.html',
        'player/details.html',
        'player/editor.html',
        'team/frontpage.html',
        'team/list.html',
        'team/listitem.html',
        'team/details.html',
        'team/editor.html',
        'league/frontpage.html',
        'league/list.html',
        'league/listitem.html',
        'league/details.html',
        'league/editor.html',
        'match/frontpage.html',
        'match/list.html',
        'match/listitem.html',
        'match/details.html',
        'match/editor.html'
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

