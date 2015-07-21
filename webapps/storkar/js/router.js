define([
    'jquery',
    'underscore',
    'backbone',
    'modules/misc',
    'modules/player'
],
function($, _, Backbone, Misc, Player) {
    var AppRouter = Backbone.Router.extend({

        initialize: function(options) {
            Backbone.Router.prototype.initialize.call(this, options);
            this.on('route', this.routeInfo);
        },

        routes: {
            'main': 'frontPage',
            'players': 'listPlayers',
            'player/:uuid': 'viewPlayer',
            'player/:uuid/edit': 'editPlayer',
            'teams': 'listTeams', // team/:uuid
            'leagues': 'listLeagues', // league/:uuid
            'matches': 'listLeagueMatches', // match/:uuid
            '*actions': 'defaultAction' // -> main
        },

        listview: null,
        listviewname: "",
        detailview: null,
        detailviewname: "",

        sections: ["main", "players", "teams", "leagues", "matches"],

        updateSection: function(section) {
            console.log("selecting section " + section);
            for (var i = 0; i < this.sections.length; ++i) {
                $("#menu"+this.sections[i]).removeClass("current");
            }
            $("#menu"+section).addClass("current");
        },

        updateListView: function(view, name, options) {
            console.log("router.updateListView(" + name + ")");
            if (name !== this.listviewname) {
                if (this.listview) {
                    if (this.listview.close) {
                        this.listview.close();
                    }
                    this.listview = null;
                    this.listviewname = null;
                }
                this.listviewname = name;
                if (view) {
                    this.listview = new view(options);
                    $("#listview").append(this.listview.$el);
                }
            }
        },

        updateDetailView: function(view, name, options) {
            console.log("router.updateDetailView(" + name + ")");
            if (name !== this.detailviewname) {
                if (this.detailview) {
                    if (this.detailview.close) {
                        this.detailview.close();
                    }
                    this.detailview = null;
                    this.detailviewname = null;
                }
                this.detailviewname = name;
                if (view) {
                    this.detailview = new view(options);
                    $("#detailview").html(this.detailview.$el);
                }
            }
        },

        routeInfo: function(actions) {
            console.log('Routing for ' + actions + '.');
        },

        frontPage: function() {
            this.updateSection("main");
            this.updateListView(null, "", {});
            this.updateDetailView(Misc.FrontPage, "dashboard", {});
        },

        listPlayers: function() {
            this.updateSection("players");
            this.updateListView(Player.List, "players", {});
            this.updateDetailView(Player.FrontPage, "players", {});
        },

        viewPlayerAsync: function(uuid) {
            this.updateListView(Player.List, "players", {});
            var App = require('app');
            this.updateDetailView(Player.Details, "playerview-" + uuid,
                                  {uuid:uuid, collection:App.players});
        },

        viewPlayer: function(uuid) {
            this.updateSection("players");
            var thiz = this;
            var App = require('app');
            if (!App.players) {
                App.players = new Player.Collection();
                App.players.fetch().done(function() {
                    App.players.sort();
                    thiz.viewPlayerAsync(uuid);
                });
            } else {
                thiz.viewPlayerAsync(uuid);
            }
        },

        editPlayerAsync: function(uuid) {
            this.updateListView(Player.List, "players", {});
            var App = require('app');
            this.updateDetailView(Player.Editor, "playeredit-" + uuid,
                                  {uuid:uuid, collection:App.players});
        },

        editPlayer: function(uuid) {
            this.updateSection("players");
            var thiz = this;
            var App = require('app');
            if (!App.players) {
                App.players = new Player.Collection();
                App.players.fetch().done(function() {
                    App.players.sort();
                    thiz.editPlayerAsync(uuid);
                });
            } else {
                thiz.editPlayerAsync(uuid);
            }
        },

        listTeams: function() {
            this.updateSection("teams");
        },

        listLeagues: function() {
            this.updateSection("leagues");
        },

        listLeagueMatches: function() {
            this.updateSection("matches");
        },

        defaultAction: function(actions) {
            console.log("default action: " + actions + ".");
            this.navigate('#/main', {trigger: true});
        }
    });

    return AppRouter;
});
