define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager'
],
function($, _, Backbone, Layout)
{
    var Misc = {};

    Misc.FrontPage = Backbone.Layout.extend({
        template: "misc/frontpage.html",

        collection: null,

        initialize: function(options) {
            console.log("main.frontpage.initialize()");
            Backbone.Layout.prototype.initialize.call(this, options);
            $("#listview").html("");
            this.render();
        },

        close: function() {
            this.remove();
            this.unbind();
        },

        beforeRender: function() {
            // set up info/links for the closest previous and upcoming matches
            // with countdown/countup time for each
            return true;
        }
    });

    return Misc;
});
