define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'storkar'
],
function($, _, Backbone, Layout, Storkar)
{
    var Match = {};

    Match.Model = Backbone.Model.extend({
        url: function() {
            return "/rest/match/" + this.uuid();
        },

        isNew: function() {
            return false;
        },

        initialize: function(options) {
            Backbone.Model.prototype.initialize.call(this, options);
        },

        defaults: {
            'uuid': '',
            'leagueid': '',
            'datetime': '',
            'hometeamid': '',
            'awayteamid': '',
            // results, goalees
            'links': []
        },

        uuid: function() {
            return this.attributes['uuid'];
        },

        leagueid: function() {
            return this.attributes['leagueid'];
        },

        datetime: function() {
            return this.attributes['datetime'];
        },

        hometeamid: function() {
            return this.attributes['hometeamid'];
        },

        awayteamid: function() {
            return this.attributes['awayteamid'];
        },

        links: function() {
            return this.attributes['links'];
        }
    });

    Match.Collection = Backbone.Collection.extend({
        url: "/rest/match",

        model: Match.Model,

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

    Match.FrontPage = Storkar.Layout.extend({
        template: "match/frontpage.html",

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
        },

        detailActions: {
        }
    });

    Match.ListItem = Backbone.Layout.extend({
        template: "match/listitem.html",

        tagName: "ul",

        className: "item",

        model: null,

        initialize: function(options) {
            this.model = options.collection.findWhere({uuid: options.uuid});
            Backbone.Layout.prototype.initialize.call(this, options);
            $(this.el).attr("id", this.model.uuid());
        },

        serialize: function() {
            return { model: this.model };
        }
    });

    Match.List = Storkar.ListLayout.extend({
        template: "match/list.html",

        collection: null,

        initialize: function(options) {
            Storkar.ListLayout.prototype.initialize.call(this, options);
            var thiz = this;
            var App = require('app');
            if (!App.matches) {
                App.matches = new Match.Collection();
                this.collection = App.matches;
                this.collection.fetch().done(function() {
                    App.matches.sort();
                    thiz.render();
                });
            } else {
                this.collection = App.matches;
                this.render();
            }
            this.listenTo(this.collection, 'change', thiz.render);
            this.listenTo(this.collection, 'update', thiz.render);
        },

        close: function() {
            Storkar.ListLayout.prototype.close.call(this);
        },

        beforeRender: function() {
            var thiz = this;
            var App = require('app');
            App.matches.each(function(item) {
                this.insertView("ul.items",
                                new Match.ListItem({
                                    uuid: item.uuid(),
                                    collection: App.matches
                                }));
            }, thiz);
            return true;
        },

        listActions: {
            "new": "newMatch",
            "reload": "reloadList"
        },

        select: function(uuid) {
            var App = require('app');
            App.router.navigate("#match/" + uuid, {trigger: true});
        },

        newMatch: function() {
            var App = require('app');
            App.router.navigate("#match/new/edit", {trigger: true});
        },

        reloadList: function() {
            this.showAlert("not implemented");
        }
    });

    Match.Editor = Storkar.Layout.extend({
        template: "match/editor.html",

        model: null,

        initialize: function(options) {
            Storkar.Layout.prototype.initialize.call(this, options);
            var thiz = this;
            this.model = options.collection.findWhere({uuid: options.uuid});
            if (this.model) {
                this.render();
            } else {
                // try 
                this.model = new Match.Model();
                this.model.set('uuid', options.uuid);
                this.model.fetch().done(function() {
                    var App = require('app');
                    App.router.navigate("#match/" + thiz.model.uuid() + "/edit",
                                        {trigger: false, replace: true});
                    thiz.render();
                });
            }
        },

        close: function() {
            Storkar.Layout.prototype.close.call(this);
        },

        beforeRender: function() {
            return true;
        },

        detailActions: {
            "save": "saveModel",
            "reset": "resetEditor",
            "return": "abortEditor",
            "delete": "deleteModel"
        },

        saveModel: function() {
            var attrs = {};
            attrs['uuid'] = this.model.uuid();
            var leagueid = $("#leagueid").val();
            if (leagueid != this.model.leagueid())
                attrs['leagueid'] = leagueid;

            this.model.save(attrs, {patch: true});
            this.render();

            var App = require('app');
            if (!App.matches.findWhere({uuid: this.model.uuid()})) {
                App.matches.add(this.model);
            }
        },

        resetEditor: function() {
            this.render();
        },

        abortEditor: function() {
            window.history.back();
            //var app = require('app');
            //app.router.navigate("#match/" + this.model.uuid(), {trigger: true});
        },

        deleteModel: function() {
            this.showAlert("Delete not implemented");
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    return Match;
});
