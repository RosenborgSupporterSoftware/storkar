define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'storkar'
],
function($, _, Backbone, Layout, Storkar)
{
    var League = {};

    League.Model = Backbone.Model.extend({
        url: function() {
            return "/rest/league/" + this.uuid();
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
            'active': true,
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

        active: function() {
            return this.attributes['active'];
        },

        links: function() {
            return this.attributes['links'];
        }
    });

    League.Collection = Backbone.Collection.extend({
        url: "/rest/league",

        model: League.Model,

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

    League.FrontPage = Storkar.Layout.extend({
        template: "league/frontpage.html",

        initialize: function(options) {
            Storkar.Layout.prototype.initialize.call(this, options);
            this.render();
        },

        close: function() {
            Storkar.Layout.prototype.close.call(this);
        },

        beforeRender: function() {
            return true;
        },

        detailActions: {
        }

    });

    League.ListItem = Backbone.Layout.extend({
        template: "league/listitem.html",

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

    League.List = Storkar.ListLayout.extend({
        template: "league/list.html",

        collection: null,

        initialize: function(options) {
            Storkar.ListLayout.prototype.initialize.call(this, options);
            var thiz = this;
            var App = require('app');
            if (!App.leagues) {
                App.leagues = new League.Collection();
                this.collection = App.leagues;
                this.collection.fetch().done(function() {
                    App.leagues.sort();
                    thiz.render();
                });
            } else {
                this.collection = App.leagues;
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
            App.leagues.each(function(item) {
                this.insertView("ul.items",
                                new League.ListItem({
                                    uuid: item.uuid(),
                                    collection: App.leagues
                                }));
            }, thiz);
            return true;
        },

        listActions: {
            "new": "newLeague",
            "reload": "reloadList"
        },

        select: function(uuid) {
            var App = require('app');
            App.router.navigate("#league/" + uuid, {trigger: true});
        },

        newLeague: function() {
            var App = require('app');
            App.router.navigate("#league/new/edit", {trigger: true});
        },

        reloadList: function() {
        }
    });

    League.Details = Storkar.Layout.extend({
        template: "league/details.html",

        model: null,

        initialize: function(options) {
            Storkar.Layout.prototype.initialize.call(this, options);
            var thiz = this;
            this.model = options.collection.findWhere({uuid: options.uuid});
            if (this.model) {
                this.render();
            } else {
                // try 
                this.model = new League.Model();
                this.model.set('uuid', options.uuid);
                this.model.fetch().done(function() {
                    var App = require('app');
                    App.router.navigate("#league/" + thiz.model.uuid() + "/edit",
                                        {trigger: false, replace: true});
                    App.router.detailviewname = "leagueeditor-" + thiz.model.uuid();
                    thiz.render();
                });
            }
        },

        close: function() {
            Storkar.Layout.prototype.close.call(this);
        },

        detailActions: {
            "edit": "editModel",
            "delete": "deleteModel"
        },

        editModel: function() {
            var App = require('app');
            App.router.navigate("#league/" + this.model.uuid() + "/edit",
                                { trigger: true });
        },

        deleteModel: function() {
            this.showAlert("Delete not enabled/implemented yet.");
            var App = require('app');
            App.router.navigate("#leagues", { trigger: true });
        },

        serialize: function() {
            return { model: this.model };
        }
    });

    League.Editor = Storkar.Layout.extend({
        template: "league/editor.html",

        model: null,

        initialize: function(options) {
            Storkar.Layout.prototype.initialize.call(this, options);
            var thiz = this;
            this.model = options.collection.findWhere({uuid: options.uuid});
            if (this.model) {
                this.render();
            } else {
                // try 
                this.model = new League.Model();
                this.model.set('uuid', options.uuid);
                this.model.fetch().done(function() {
                    var App = require('app');
                    App.router.navigate("#league/" + thiz.model.uuid() + "/edit",
                                        {trigger: false, replace: true});
                    App.router.detailviewname = "leagueeditor-" + thiz.model.uuid();
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
            var name = $("#name").val();
            if (name != this.model.name())
                attrs['name'] = name;
            var shortname = $("#shortname").val();
            if (shortname != this.model.shortname())
                attrs['shortname'] = shortname;
            var abbreviation = $("#abbreviation").val();
            if (abbreviation != this.model.abbreviation())
                attrs['abbreviation'] = abbreviation;

            this.model.save(attrs, {patch: true});
            this.render();

            var App = require('app');
            if (!App.leagues.findWhere({uuid: this.model.uuid()})) {
                App.leagues.add(this.model);
            }
        },

        resetEditor: function() {
            this.render();
        },

        abortEditor: function() {
            window.history.back();
            //var app = require('app');
            //app.router.navigate("#league/" + this.model.uuid(), {trigger: true});
        },

        deleteModel: function() {
            this.showAlert("Delete not enabled/implemented yet.");
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    return League;
});
