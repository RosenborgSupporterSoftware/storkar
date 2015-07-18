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
        url: "/rest/player",

        initialize: function(options) {
            Backbone.Model.prototype.initialize.call(this, options);
        },

        defaults: {
            'uuid': '',
            'name': '',
            'shortname': '',
            'headshot-20x30-url': '',
            'aliases': [],
            'active': true
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

        aliases: function() {
            return this.attributes['aliases'];
        },

        headshot_20x30_url: function() {
            return this.attributes['headshot-20x30-url'];
        },

        active: function() {
            return this.attributes['active'];
        }

    });

    Player.Collection = Backbone.Collection.extend({
        url: "/rest/player",

        model: Player.Model,

        initialize: function(options) {
            Backbone.Collection.prototype.initialize.call(this, options);
        }

    });

    Player.ListItem = Backbone.Layout.extend({
        template: "player/item.html",

        tagName: "tr",

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

        el: '#content',
        subel: '#listcontent',

        collection: null,

        initialize: function(options) {
            var thiz = this;
            Backbone.Layout.prototype.initialize.call(this, options);
            this.collection = new Player.Collection();
            this.listenTo(this.collection, 'change', thiz.render);
            this.collection.fetch().done(function() {
                thiz.collection.each(function(item) {
                    thiz.insertView("tbody#listcontent",
                                    new Player.ListItem({uuid: item.uuid(),
                                    collection: thiz.collection}));
                }, this);
                thiz.render(); // trigger('render'); //render();
            });
        },

        beforeRender: function() {
            var thiz = this;
            return true;
        }

    });

    return Player;
});
