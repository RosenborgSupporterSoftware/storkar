define([
    'jquery',
    'underscore',
    'backbone',
    'modules/misc',
    'modules/player',
    'modules/team',
    'modules/league',
    'modules/match'
],
function($, _, Backbone, Misc, Player, Team, League, Match) {
    var Router = Backbone.Router.extend({

        initialize: function(options) {
            Backbone.Router.prototype.initialize.call(this, options);
            this.on('route', this.routeInfo);
        },

        routes: {
            'dashboard': 'dashboard',
            'players': 'listPlayers',
            'player/:uuid/edit': 'editPlayer',
            'player/:uuid': 'viewPlayer',
            'teams': 'listTeams',
            'team/:uuid/edit': 'editTeam',
            'team/:uuid': 'viewTeam',
            'leagues': 'listLeagues',
            'league/:uuid/edit': 'editLeague',
            'league/:uuid': 'viewLeague',
            'matches': 'listMatches',
            'match/:uuid/edit': 'editMatch',
            'match/:uuid': 'viewMatch',
            '*actions': 'defaultAction'
        },

        listview: null,
        listviewname: "",
        detailview: null,
        detailviewname: "",

        sections: ["main", "players", "teams", "leagues", "matches"],

        updateSection: function(section) {
            //console.log("selecting section " + section);
            for (var i = 0; i < this.sections.length; ++i) {
                $("#menu"+this.sections[i]).removeClass("current");
            }
            $("#menu"+section).addClass("current");
        },

        updateListView: function(view, name, options) {
            //console.log("router.updateListView(" + name + ")");
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
            else if (this.listview instanceof Storkar.ListLayout) {
                if (options.uuid) {
                    this.listview.setSelection(options.uuid);
                } else {
                    this.listview.setSelection(null);
                }
            }
        },

        updateDetailView: function(view, name, options) {
            //console.log("router.updateDetailView(" + name + ")");
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

        dashboard: function() {
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
            this.updateListView(Player.List, "players", {uuid:uuid});
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
            this.updateListView(Player.List, "players", {uuid:uuid});
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
            this.updateListView(Team.List, "teams", {uuid:uuid});
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
            this.updateListView(Team.List, "teams", {uuid:uuid});
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
            this.updateListView(League.List, "leagues", {});
            this.updateDetailView(League.FrontPage, "leagues", {});
        },

        viewLeagueAsync: function(uuid) {
            this.updateListView(League.List, "leagues", {uuid:uuid});
            var App = require('app');
            this.updateDetailView(League.Details, "leagueview-" + uuid,
                                  {uuid:uuid, collection:App.leagues});
        },

        viewLeague: function(uuid) {
            this.updateSection("leagues");
            var thiz = this;
            var App = require('app');
            if (!App.leagues) {
                App.leagues = new League.Collection();
                App.leagues.fetch().done(function() {
                    App.leagues.sort();
                    thiz.viewLeagueAsync(uuid);
                });
            } else {
                thiz.viewLeagueAsync(uuid);
            }
        },

        editLeagueAsync: function(uuid) {
            this.updateListView(League.List, "leagues", {uuid:uuid});
            var App = require('app');
            this.updateDetailView(League.Editor, "leagueeditor-" + uuid,
                                  {uuid:uuid, collection:App.leagues});
        },

        editLeague: function(uuid) {
            this.updateSection("leagues");
            var thiz = this;
            var App = require('app');
            if (!App.leagues) {
                App.leagues = new League.Collection();
                App.leagues.fetch().done(function() {
                    App.leagues.sort();
                    thiz.editLeagueAsync(uuid);
                });
            } else {
                thiz.editLeagueAsync(uuid);
            }
        },

        listMatches: function() {
            this.updateSection("matches");
            this.updateListView(Match.List, "matches", {});
            this.updateDetailView(Match.FrontPage, "matches", {});
        },

        viewMatchAsync: function(uuid) {
            this.updateListView(Match.List, "matches", {uuid:uuid});
            var App = require('app');
            this.updateDetailView(Match.Details, "matchview-" + uuid,
                                  {uuid:uuid, collection:App.matches});
        },

        viewMatch: function(uuid) {
            this.updateSection("matches");
            var thiz = this;
            var App = require('app');
            if (!App.matches) {
                App.matches = new Match.Collection();
                App.matches.fetch().done(function() {
                    App.matches.sort();
                    thiz.viewMatchAsync(uuid);
                });
            } else {
                thiz.viewMatchAsync(uuid);
            }
        },

        editMatchAsync: function(uuid) {
            this.updateListView(Match.List, "matches", {uuid:uuid});
            var App = require('app');
            this.updateDetailView(Match.Editor, "matcheditor-" + uuid,
                                  {uuid:uuid, collection:App.matches});
        },

        editMatch: function(uuid) {
            this.updateSection("matches");
            var thiz = this;
            var App = require('app');
            if (!App.matches) {
                App.matches = new Match.Collection();
                App.matches.fetch().done(function() {
                    App.matches.sort();
                    thiz.editMatchAsync(uuid);
                });
            } else {
                thiz.editMatchAsync(uuid);
            }
        },

        defaultAction: function(actions) {
            console.log("default action: " + actions + ".");
            this.navigate('#dashboard', {trigger: true});
        }
    });

    return Router;
});
