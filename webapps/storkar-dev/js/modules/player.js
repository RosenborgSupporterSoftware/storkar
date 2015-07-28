define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'storkar'
],
function($, _, Backbone, Layout, Storkar)
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
            'fullname': '',
            'shortname': '',
            'aliases': [],
            'headshot-20x30-url': '',
            'headshot-40x60-url': '',
            'headshot-80x120-url': '',
            'headshot-160x240-url': '',
            'teamid': '',
            'active': true,
            'country': 'NO',
            'links': []
        },

        uuid: function() {
            return this.attributes['uuid'];
        },

        name: function() {
            return this.attributes['name'];
        },

        fullname: function() {
            return this.attributes['fullname'];
        },

        shortname: function() {
            return this.attributes['shortname'];
        },

        aliases: function() {
            return this.attributes['aliases'];
        },

        number: function() {
            return this.attributes['number'];
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

        headshot_160x240_url: function() {
            return this.attributes['headshot-160x240-url'];
        },

        teamid: function() {
            return this.attributes['teamid'];
        },

        active: function() {
            return this.attributes['active'];
        },

        country: function() {
            return this.attributes['country'];
        },

        links: function() {
            return this.attributes['links'] || [];
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

        className: "item",

        model: null,

        initialize: function(options) {
            Backbone.Layout.prototype.initialize.call(this, options);
            this.model = options.collection.findWhere({uuid: options.uuid});
            $(this.el).attr("id", this.model.uuid());
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    Player.List = Storkar.ListLayout.extend({
        template: "player/list.html",

        collection: null,

        initialize: function(options) {
            Storkar.ListLayout.prototype.initialize.call(this, options);
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
            this.listenTo(this.collection, 'update', thiz.render);
        },

        close: function() {
            Storkar.ListLayout.prototype.close.call(this);
        },

        beforeRender: function() {
            var App = require('app');
            var thiz = this;
            App.players.each(function(item) {
                thiz.insertView("ul.items",
                                new Player.ListItem({
                                    uuid: item.uuid(),
                                    collection: App.players
                                }));
            }, thiz);
            return true;
        },

        listActions: {
            "new":    "newPlayer",
            "reload": "reloadList"
            // "filter": "filterList"
        },

        select: function(uuid) {
            //console.log("select item " + uuid);
            var App = require('app');
            App.router.navigate("#player/" + uuid, {trigger: true});
        },

        newPlayer: function() {
            var App = require('app');
            App.router.navigate("#player/new/edit", {trigger: true});
        },

        reloadList: function() {
            this.showAlert("Reload not implemented yet.");
        },

        filterList: function() {
            this.showAlert("Filter not implemented yet.");
        }

    });

    Player.Details = Storkar.Layout.extend({
        template: "player/details.html",

        model: null,

        initialize: function(options) {
            Storkar.Layout.prototype.initialize.call(this, options);
            this.model = options.collection.findWhere({uuid: options.uuid});
            this.render();
        },

        close: function() {
            Storkar.Layout.prototype.close.call(this);
        },

        beforeRender: function() {
            return true;
        },

        detailActions: {
            "delete": "deletePlayer",
            "edit": "editPlayer"
        },

        editPlayer: function() {
            var App = require('app');
            var url = "#player/" + this.model.uuid() + "/edit";
            //console.log("URL: " + url);
            App.router.navigate("#player/" + this.model.uuid() + "/edit", {trigger: true});
        },

        deletePlayer: function() {
            this.showAlert("Delete not enabled/implemented yet.");
            var App = require('app');
            App.router.navigate("#players", {trigger: true});
        },

        serialize: function() {
            var info = { teamname: "" };
            var App = require('app');
            if (this.model.teamid() !== "" && App.teams !== null) {
                var team = App.teams.findWhere({ uuid: this.model.teamid() });
                if (team) info.teamname = team.name();
            }
            return { model: this.model, info: info };
        }

    });

    Player.Editor = Storkar.Layout.extend({
        template: "player/editor.html",

        model: null,

        initialize: function(options) {
            var thiz = this;
            Storkar.Layout.prototype.initialize.call(this, options);
            this.model = options.collection.findWhere({uuid: options.uuid});
            if (this.model) {
                this.render();
            } else {
                this.model = new Player.Model();
                this.model.set('uuid', options.uuid);
                this.model.fetch().done(function() {
                    var App = require('app');
                    App.router.navigate("#player/" + thiz.model.uuid() + "/edit",
                                        {trigger: false, replace: true});
                    App.router.detailviewname = "playereditor-" + thiz.model.uuid();
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

        events: {
            "focusout #newlink": "newLinkFocus",
            "keypress #newlink": "newLinkEnter",
        },

        newLinkEnter: function(event) {
            if (event.which !== 13) return;
            if (this.$(event.target).val() !== "") {
                this.addLinkInputField();
            }
        },

        newLinkFocus: function(event) {
            if (this.$(event.target).val() !== "") {
                this.addLinkInputField();
            }
        },

        addLinkInputField: function() {
            var n = 1;
            while (this.$("#link" + n).length) { n = n + 1; }
            var $lastlink = this.$("#newlink");
            $lastlink.closest("table").append("<tr><td>" + (n+1) + "</td><td><input id=\"newlink\" type=\"text\" size=\"60\"></input></td></tr>");
            $lastlink.attr("id", "link"+n);
            this.$("#newlink").focus();
        },

        detailActions: {
            "save": "saveModel",
            "reset": "resetEditor",
            "delete": "deleteModel",
            "return": "returnBack"
        },

        saveModel: function() {
            var attrs = {};
            attrs['uuid'] = this.model.uuid();
            var fullname = $('#fullname').val();
            if (fullname != this.model.fullname())
                attrs['fullname'] = fullname;
            var name = $('#name').val();
            if (name != this.model.name())
                attrs['name'] = name;
            var shortname = $('#shortname').val();
            if (shortname != this.model.shortname())
                attrs['shortname'] = shortname;
            var aliases = this.model.aliases();
            var aliasesstr = $('#aliases').val();
            if (aliasesstr) aliases = aliasesstr.split(',');

            if (aliases != this.model.aliases()) // FIXME: does not work
                attrs['aliases'] = aliases;
            var numberstr = $('#number').val();
            var number = this.model.number();
            if (numberstr) number = parseInt(numberstr, 10);
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
            var headshot240 = $('#headshot240').val();
            if (headshot240 != this.model.headshot_160x240_url())
                attrs['headshot-160x240-url'] = headshot240;
            var teamid = $('#team').val();
            // FIXME: don't send before we're using uuid here
            //if (teamid !== this.model.teamid())
            //    attrs['teamid'] = teamid;
            var active = $('#active').is(':checked');
            if (active != this.model.active())
                attrs['active'] = active;

            var links = [];
            for (var i = 1; ; i = i + 1) {
                var $linkinput = this.$('#link'+i);
                if ($linkinput.length) {
                    var linktext = $linkinput.val();
                    if (linktext !== "") {
                        links.push(linktext);
                    }
                }
                else {
                    break;
                }
            }
            var linktext = $('#newlink').val();
            if (linktext !== "") {
                links.push(linktext);
            }
            if (links != this.model.links()) { // FIXME: does not work
                attrs['links'] = links;
            }
            this.model.save(attrs, {patch: true});
            this.render();

            var App = require('app');
            if (!App.players.findWhere({uuid: this.model.uuid()})) {
                App.players.add(this.model);
            }
        },

        resetEditor: function() {
            this.render();
        },

        deleteModel: function() {
            this.showAlert("Delete not enabled/implemented yet.");
            var App = require('app');
            App.router.navigate("#players", {trigger: true});
        },

        returnBack: function() {
            window.history.back();
        },

        serialize: function() {
            var info = { teamname: "" };
            var App = require('app');
            if (this.model.teamid() !== "" && App.teams !== null) {
                var team = App.teams.findWhere({ uuid: this.model.teamid() });
                if (team) info.teamname = team.name();
            }
            return { model: this.model, info: info };
        }

    });


    return Player;
});
