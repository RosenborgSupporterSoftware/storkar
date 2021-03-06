define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'storkar'
],
function($, _, Backbone, Layout, Storkar)
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
            'fullname': '',
            'name': '',
            'shortname': '',
            'abbreviation': '',
            'country': '',
            'logo-30-url': '',
            'logo-60-url': '',
            'logo-120-url': '',
            'active': true,
            'links': []
        },

        uuid: function() {
            return this.attributes['uuid'];
        },

        fullname: function() {
            return this.attributes['fullname'];
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

        abbreviation: function() {
            return this.attributes['abbreviation'];
        },

        country: function() {
            return this.attributes['country'];
        },

        logo_30_url: function() {
            return this.attributes['logo-30-url'];
        },

        logo_60_url: function() {
            return this.attributes['logo-60-url'];
        },

        logo_120_url: function() {
            return this.attributes['logo-120-url'];
        },

        active: function() {
            return this.attributes['active'];
        },

        links: function() {
            return this.attributes['links'];
        }

    });

    Team.Collection = Backbone.Collection.extend({
        url: "/rest/team",

        model: Team.Model,

        comparator: function(m1, m2) {
            if (m1.attributes['country'] !== m2.attributes['country']) {
                if (m1.attributes['country'] == 'NO')
                    return -1;
                if (m2.attributes['country'] == 'NO')
                    return 1;
            }
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

    Team.List = Storkar.ListLayout.extend({
        template: "team/list.html",

        collection: null,

        initialize: function(options) {
            Storkar.ListLayout.prototype.initialize.call(this, options);
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
            this.listenTo(this.collection, 'update', thiz.render);
        },

        close: function() {
            Storkar.ListLayout.prototype.close.call(this);
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
        },

        listActions: {
            "new":    "newTeam",
            "reload": "reloadList"
        },

        select: function(uuid) {
            var App = require('app');
            App.router.navigate("#team/" + uuid, {trigger: true});
        },

        newTeam: function() {
            var App = require('app');
            App.router.navigate("#team/new/edit", {trigger: true});
        },

        reloadList: function() {
        }

    });

    Team.Details = Storkar.Layout.extend({
        template: "team/details.html",

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
            "edit": "editTeam",
            "delete": "deleteTeam"
        },

        editTeam: function() {
            var App = require('app');
            App.router.navigate("#team/" + this.model.uuid() + "/edit", {trigger: true});
        },

        deleteTeam: function() {
            this.showAlert("Delete not enabled/implemented yet.");
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    Team.Editor = Storkar.Layout.extend({
        template: "team/editor.html",

        model: null,

        initialize: function(options) {
            Storkar.Layout.prototype.initialize.call(this, options);
            this.model = options.collection.findWhere({uuid: options.uuid});
            if (this.model) {
                this.render();
            } else {
                this.model = new Team.Model();
                this.model.set('uuid', options.uuid);
                var thiz = this;
                this.model.fetch().done(function() {
                    var App = require('app');
                    App.router.navigate("#team/" + thiz.model.uuid() + "/edit",
                                        {trigger: false, replace: true});
                    App.router.detailviewname = "teameditor-" + thiz.model.uuid();
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
            "keydown #newlink": "newLinkTAB"
        },

        newLinkEnter: function(event) {
            if (event.which !== 13) return;
            console.log("newLinkEnter()");
            if (this.$(event.target).val() !== "") {
                this.addLinkInputField();
                this.$("#newlink").focus();
            }
        },

        setFocusElement: false,

        newLinkTAB: function(event) {
            if (event.keyCode !== 9) return;
            console.log("newLinkTAB()");
            if (this.$(event.target).val() !== "") {
                this.addLinkInputField();
                this.setFocusElement = "#newlink";
            }
        },

        newLinkFocus: function(event) {
            if (this.$(event.target).val() !== "") {
                console.log("newLinkFocusOut()");
                this.addLinkInputField();
                if (this.setFocusElement) {
                    this.$(this.setFocusElement).focus();
                    this.setFocusElement = false;
                }
            }
        },

        addLinkInputField: function() {
            var n = 1;
            while (this.$("#link" + n).length) { n = n + 1; }
            var $lastlink = this.$("#newlink");
            $lastlink.closest("table").append("<tr><td>" + (n+1) + "</td><td><input id=\"newlink\" type=\"text\" size=\"60\"></input></td></tr>");
            $lastlink.attr("id", "link"+n);
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

            var fullname = $("#fullname").val();
            if (fullname != this.model.fullname())
                attrs['fullname'] = fullname;

            var name = $("#name").val();
            if (name != this.model.name())
                attrs['name'] = name;
            var shortname = $("#shortname").val();
            if (shortname != this.model.shortname())
                attrs['shortname'] = shortname;
            var abbreviation = $("#abbreviation").val();
            if (abbreviation != this.model.abbreviation())
                attrs['abbreviation'] = abbreviation;
            var country = $("#country").val();
            if (country != this.model.country())
                attrs['country'] = country;

            var logo_30 = $("#logo30").val();
            if (logo_30 != this.model.logo_30_url())
                attrs['logo-30-url'] = logo_30;
            var logo_60 = $("#logo60").val();
            if (logo_60 != this.model.logo_60_url())
                attrs['logo-60-url'] = logo_60;
            var logo_120 = $("#logo120").val();
            if (logo_120 != this.model.logo_120_url())
                attrs['logo-120-url'] = logo_120;

            var active = $('#active').is(':checked');
            if (active != this.model.active())
                attrs['active'] = active;

            var links = [];
            var linktext = null;
            for (var i = 1; ; i = i + 1) {
                var $linkinput = this.$('#link'+i);
                if ($linkinput.length) {
                    linktext = $linkinput.val();
                    if (linktext !== "") {
                        links.push(linktext);
                    }
                }
                else {
                    break;
                }
            }
            linktext = $('#newlink').val();
            if (linktext !== "") {
                links.push(linktext);
            }
            if (links != this.model.links()) { // FIXME: does not work
                attrs['links'] = links;
            }

            this.model.save(attrs, {patch: true});
            this.render();

            var App = require('app');
            if (!App.teams.findWhere({uuid: this.model.uuid()})) {
                App.teams.add(this.model);
            }
        },

        resetEditor: function() {
            this.render();
        },

        abortEditor: function() {
            var app = require('app');
            app.router.navigate("#team/" + this.model.uuid(), {trigger: true});
        },

        deleteModel: function() {
            this.showAlert("Delete not enabled/implemented yet.");
            var App = require('app');
            App.router.navigate("#teams", {trigger: true});
        },

        serialize: function() {
            return { model: this.model };
        }

    });

    // Misc.TabList
    // Team.PlayerList
    // Team.MatchList
    // Team.Formation

    return Team;
});
