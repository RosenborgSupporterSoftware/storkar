define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager'
],
function($, _, Backbone, Layout)
{
    var Player = {};

    Player.Model = Backbone.Model.extend({
        url: function() {
            return "/rest/player/" + this.uuid();
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
            'aliases': [],
            'headshot-20x30-url': '',
            'headshot-40x60-url': '',
            'headshot-80x120-url': '',
            'teamid': '',
            'active': true
        },

        uuid: function() {
            return this.attributes['uuid'];
        },

        name: function() {
            return this.attributes['name'];
        },

        number: function() {
            return this.attributes['number'];
        },

        shortname: function() {
            return this.attributes['shortname'];
        },

        aliases: function() {
            return this.attributes['aliases'];
        },

        headshot_20x30_url: function() {
            return this.attributes['headshot-20x30-url'];
        },

        headshot_40x60_url: function() {
            return this.attributes['headshot-40x60-url'];
        },

        headshot_80x120_url: function() {
            return this.attributes['headshot-80x120-url'];
        },

        teamid: function() {
            return this.attributes['teamid'];
        },

        active: function() {
            return this.attributes['active'];
        }
    });

    Player.Collection = Backbone.Collection.extend({
        url: "/rest/player",

        model: Player.Model,

        comparator: function(m1, m2) {
            if (m1.attributes['number'] && m2.attributes['number']) {
                return m1.attributes['number'] - m2.attributes['number'];
            } else if (m1.attributes['number']) {
                return -1;
            } else if (m2.attributes['number']) {
                return 1;
            } else {
                return 0;
            }
        },

        initialize: function(options) {
            Backbone.Collection.prototype.initialize.call(this, options);
        }

    });

    Player.FrontPage = Backbone.Layout.extend({
        template: "player/frontpage.html",

        initialize: function(options) {
            Backbone.Layout.prototype.initialize.call(this, options);
            $(this.el).addClass("player");
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

    Player.ListItem = Backbone.Layout.extend({
        template: "player/listitem.html",

        tagName: "ul",

        model: null,

        initialize: function(options) {
            this.model = options.collection.findWhere({uuid: options.uuid});
            Backbone.Layout.prototype.initialize.call(this, options);
            $(this.el).addClass("player");
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    Player.List = Backbone.Layout.extend({
        template: "player/list.html",

        collection: null,

        initialize: function(options) {
            Backbone.Layout.prototype.initialize.call(this, options);
            var thiz = this;
            var App = require('app');
            if (!App.players) {
                App.players = new Player.Collection();
                this.collection = App.players;
                App.players.fetch().done(function() {
                    App.players.sort();
                    thiz.render();
                });
            } else {
                this.collection = App.players;
                this.render();
            }
            this.listenTo(this.collection, 'change', thiz.render);
        },

        close: function() {
            this.remove();
            this.unbind();
        },

        beforeRender: function() {
            var App = require('app');
            var thiz = this;
            App.players.each(function(item) {
                thiz.insertView("ul.players",
                                new Player.ListItem({
                                    uuid: item.uuid(),
                                    collection: App.players
                                }));
            }, thiz);
            return true;
        }

    });

    Player.Details = Backbone.Layout.extend({
        template: "player/details.html",

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
            "click #edit": "editPlayer"
        },

        editPlayer: function() {
            var App = require('app');
            App.router.navigate("player/" + this.model.uuid() + "/edit", {trigger: true});
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    Player.Editor = Backbone.Layout.extend({
        template: "player/editor.html",

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
            var attrs = {};
            var name = $('#name').val();
            if (name != this.model.name())
                attrs['name'] = name;
            var shortname = $('#shortname').val();
            if (shortname != this.model.shortname())
                attrs['shortname'] = shortname;
            var aliases = this.model.aliases();
            var aliasesstr = $('#aliases').val();
            if (aliasesstr) aliases = aliasesstr.split(',');
            if (aliases != this.model.aliases())
                attrs['aliases'] = aliases;
            var numberstr = $('#number').val();
            var number = this.model.number();
            if (numberstr) number = parseInt(numberstr);
            if (number != this.model.number())
                attrs['number'] = number;
            var headshot30 = $('#headshot30').val();
            if (headshot30 != this.model.headshot_20x30_url())
                attrs['headshot-20x30-url'] = headshot30;
            var headshot60 = $('#headshot60').val();
            if (headshot60 != this.model.headshot_40x60_url())
                attrs['headshot-40x60-url'] = headshot60;
            var headshot120 = $('#headshot120').val();
            if (headshot120 != this.model.headshot_80x120_url())
                attrs['headshot-80x120-url'] = headshot120;
            var teamid = $('#team').val();
            // FIXME: don't send before we're using uuid here
            //if (teamid !== this.model.teamid())
            //    attrs['teamid'] = teamid;
            var active = $('#active').val() === "true";
            if (active != this.model.active())
                attrs['active'] = active;

            this.model.save(attrs, {patch: true});
        },

        resetEditor: function() {
            this.render();
        },

        abortEditor: function() {
            var app = require('app');
            app.router.navigate('#player/' + this.model.uuid(), {trigger: true});
        },

        serialize: function() {
            return { model: this.model };
        }

    });


    return Player;
});
