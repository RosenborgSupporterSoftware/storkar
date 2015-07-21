define([
    'jquery',
    'underscore',
    'backbone',
    'modules/misc',
    'modules/player',
    'modules/team'
],
function($, _, Backbone, Misc, Player, Team) {
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
            'teams': 'listTeams',
            'team/:uuid': 'viewTeam',
            'team/:uuid/edit': 'editTeam',
            'leagues': 'listLeagues',
            'matches': 'listLeagueMatches',
            '*actions': 'defaultAction'
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
            this.updateDetailView(Player.Editor, "playereditor-" + uuid,
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
            this.updateListView(Team.List, "teams", {});
            this.updateDetailView(Team.FrontPage, "teams", {});
        },

        viewTeamAsync: function(uuid) {
            this.updateListView(Team.List, "teams", {});
            var App = require('app');
            this.updateDetailView(Team.Details, "teamview-" + uuid,
                                  {uuid:uuid, collection:App.teams});
        },

        viewTeam: function(uuid) {
            this.updateSection("teams");
            var thiz = this;
            var App = require('app');
            if (!App.teams) {
                App.teams = new Team.Collection();
                App.teams.fetch().done(function() {
                    App.teams.sort();
                    thiz.viewTeamAsync(uuid);
                });
            } else {
                thiz.viewTeamAsync(uuid);
            }
        },

        editTeamAsync: function(uuid) {
            this.updateListView(Team.List, "teams", {});
            var App = require('app');
            this.updateDetailView(Team.Editor, "teameditor-" + uuid,
                                  {uuid:uuid, collection:App.teams});
        },

        editTeam: function(uuid) {
            this.updateSection("teams");
            var thiz = this;
            var App = require('app');
            if (!App.teams) {
                App.teams = new Team.Collection();
                App.teams.fetch().done(function() {
                    App.teams.sort();
                    thiz.editTeamAsync(uuid);
                });
            } else {
                thiz.editTeamAsync(uuid);
            }
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
