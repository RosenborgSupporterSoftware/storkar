define([
    'jquery',
    'underscore',
    'backbone'
],
function($, _, Backbone)
{
    var Team = {};

    Team.Model = Backbone.Model.extend({
        url: function() {
            return "/rest/team/" + this.uuid();
        },

        isNew: function() {
            return false;
        },

        initialize: function(options) {
            Backbone.Model.prototype.initialize.call(this, options);
        },

        defaults: {
            'uuid': '',
            'name': '',
            'shortname': '',
            'abbreviation': '',
            'country': '',
            'logo-30-url': '',
            'logo-60-url': '',
            'logo-120-url': '',
            'links': []
        },

        uuid: function() {
            return this.attributes['uuid'];
        },

        name: function() {
            return this.attributes['name'];
        },

        shortname: function() {
            return this.attributes['shortname'];
        },

        abbreviation: function() {
            return this.attributes['abbreviation'];
        },

        country: function() {
            return this.attributes['country'];
        },

        logo_120_url: function() {
            return this.attributes['logo-120-url'];
        },

        logo_60_url: function() {
            return this.attributes['logo-60-url'];
        },

        logo_30_url: function() {
            return this.attributes['logo-30-url'];
        },

        links: function() {
            return this.attributes['links'];
        }

    });

    Team.Collection = Backbone.Collection.extend({
        url: "/rest/team",

        model: Team.Model,

        comparator: function(m1, m2) {
            if (m1.attributes['name'] && m2.attributes['name']) {
                return m1.attributes['name'].localeCompare(m2.attributes['name']);
            } else if (m1.attributes['name']) {
                return -1;
            } else if (m2.attributes['name']) {
                return 1;
            } else {
                return 0;
            }
        },

        initialize: function(options) {
            Backbone.Collection.prototype.initialize.call(this, options);
        }

    });

    Team.FrontPage = Backbone.Layout.extend({
        template: "team/frontpage.html",

        initialize: function(options) {
            Backbone.Layout.prototype.initialize.call(this, options);
            this.render();
        },

        close: function() {
            this.remove();
            this.unbind();
        },

        beforeRender: function() {
            return true;
        }

    });

    Team.ListItem = Backbone.Layout.extend({
        template: "team/listitem.html",

        tagName: "ul",

        model: null,

        initialize: function(options) {
            this.model = options.collection.findWhere({uuid: options.uuid});
            Backbone.Layout.prototype.initialize.call(this, options);
            $(this.el).addClass("item");
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    Team.List = Backbone.Layout.extend({
        template: "team/list.html",

        collection: null,

        initialize: function(options) {
            Backbone.Layout.prototype.initialize.call(this, options);
            var thiz = this;
            var App = require('app');
            if (!App.teams) {
                App.teams = new Team.Collection();
                this.collection = App.teams;
                this.collection.fetch().done(function() {
                    App.teams.sort();
                    thiz.render();
                });
            } else {
                this.collection = App.teams;
                this.render();
            }
            this.listenTo(this.collection, 'change', thiz.render);
        },

        close: function() {
            this.remove();
            this.unbind();
        },

        beforeRender: function() {
            var thiz = this;
            var App = require('app');
            App.teams.each(function(item) {
                this.insertView("ul.items",
                                new Team.ListItem({
                                    uuid: item.uuid(),
                                    collection: App.teams
                                }));
            }, thiz);
            return true;
        }
    });

    Team.Details = Backbone.Layout.extend({
        template: "team/details.html",

        model: null,

        initialize: function(options) {
            this.model = options.collection.findWhere({uuid: options.uuid});
            Backbone.Layout.prototype.initialize.call(this, options);
            this.render();
        },

        close: function() {
            this.remove();
            this.unbind();
        },

        beforeRender: function() {
            return true;
        },

        events: {
            "click #edit": "editTeam"
        },

        editTeam: function() {
            var App = require('app');
            App.router.navigate("#team/" + this.model.uuid() + "/edit", {trigger: true});
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    Team.Editor = Backbone.Layout.extend({
        template: "team/editor.html",

        model: null,

        initialize: function(options) {
            this.model = options.collection.findWhere({uuid: options.uuid});
            Backbone.Layout.prototype.initialize.call(this, options);
            this.render();
        },

        close: function() {
            this.remove();
            this.unbind();
        },

        beforeRender: function() {
            return true;
        },

        events: {
            "click #save": "save",
            "click #reset": "resetEditor",
            "click #abort": "abortEditor"
        },

        save: function() {
        },

        resetEditor: function() {
            this.render();
        },

        abortEditor: function() {
            var app = require('app');
            app.router.navigate("#team/" + this.model.uuid(), {trigger: true});
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    return Team;
});
