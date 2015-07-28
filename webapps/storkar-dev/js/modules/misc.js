define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'storkar'
],
function($, _, Backbone, Layout, Storkar)
{
    var Misc = {};

    Misc.FrontPage = Storkar.Layout.extend({
        template: "misc/frontpage.html",

        collection: null,

        initialize: function(options) {
            console.log("main.frontpage.initialize()");
            Storkar.Layout.prototype.initialize.call(this, options);
            $("#listview").html("");
            this.render();
        },

        close: function() {
            Storkar.Layout.prototype.close.call(this);
        },

        listActions: {
        },

        detailActions: {
        },

        beforeRender: function() {
            // set up info/links for the closest previous and upcoming matches
            // with countdown/countup time for each
            return true;
        }
    });

    return Misc;
});
