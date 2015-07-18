define([
    'jquery',
    'underscore',
    'backbone',
    'modules/player'
],
function($, _, Backbone, Player) {
    var AppRouter = Backbone.Router.extend({

        initialize: function(options) {
            Backbone.Router.prototype.initialize.call(this, options);
            this.on('route', this.routeInfo);
        },

        routes: {
            'players': 'listPlayers',
            '*actions': 'defaultAction'
        },

        routeInfo: function(actions) {
            console.log('Routing for ', actions);
        },

        listPlayers: function() {
            var playerList = new Player.List();
        },

        defaultAction: function(actions) {
            this.listPlayers(); // FIXME: rewrite location
        }
    });

    var initialize = function() {
        var app_router = new AppRouter();

        // app_router.on('route', function(actions) {
        //     console.log('Routing for ', actions);
        // });

        Backbone.history.start({pushState: true});
        return app_router;
    };

    return { initialize: initialize };
});
