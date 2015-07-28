define(
    "storkar",
[
    'backbone'
],
function(Backbone)
{
    Storkar = {};

    Storkar.Layout = Backbone.Layout.extend({
        initialize: function(options) {
            if (this.detailActions) {
                this.hideActions("#detailactions");
                this.bindActions("#detailactions", this.detailActions);
            }
            if (this.listActions) {
                this.hideActions("#listactions");
                this.bindActions("#listactions", this.listActions);
            }
        },

        close: function() {
            if (this.detailActions)
                this.unbindActions("#detailactions", this.detailActions);
            if (this.listActions)
                this.unbindActions("#listactions", this.listActions);
            this.remove();
            this.unbind();
        },

        bindActions: function(tagcontext, actions) {
            var $ctx = $(tagcontext);
            for (var action in actions) {
                //console.log("registering handler for action " + action);
                var methodname = actions[action];
                var $a = $ctx.find("#" + action + "-action");
                $a.bind('click',
                        {self:this, action:action, method:methodname},
                        this.dispatch);
                $a.css("display", "inline");
            }
            //$ctx.css("display","inline");
        },

        unbindActions: function(tagcontext, actions) {
            var $ctx = $(tagcontext);
            for (var action in actions) {
                //console.log("unregistering handler for action " + action);
                $ctx.find("#" + action + "-action").unbind('click', this.dispatch);
            }
        },

        dispatch: function(event) {
            var self = event.data.self;
            var methodname = event.data.method;
            var action = event.data.action;
            var method = self[methodname];
            $.proxy(method, self)();
        },

        hideActions: function(tagcontext) {
            var $ctx = $(tagcontext);
            $ctx.find("a").css("display","none");
        },

        showAlert: function(msg) {
            $("#alert").html(msg);
            window.setTimeout(this.clearAlert, 5000);
        },

        clearAlert: function() {
            $("#alert").html("");
        }

    });

    Storkar.ListLayout = Storkar.Layout.extend({

        selection: null,

        initialize: function(options) {
            Storkar.Layout.prototype.initialize.call(this, options);
        },

        close: function(options) {
            Storkar.Layout.prototype.close.call(this, options);
        },

        events: {
            "click .item": "listItemClick"
        },

        // implement in subclass
        //select: function(uuid) {
        //},

        setSelection: function(uuid) {
            if (this.selection && this.selection == uuid) return;
            if (this.selection) {
                this.$("#" + this.selection).removeClass("selected");
            }
            this.selection = uuid;
            if (uuid) {
                var target = this.$("#" + uuid);
                target.addClass("selected");
            }
            //console.log("set item " + this.selection + " selected.");
        },

        listItemClick: function(event) {
            var target = $(event.target).parent();
            if (target) {
                this.setSelection(target.attr("id"));
            }
            if (this.select) {
                this.select(this.selection);
            }
        }

    });

    return Storkar;
});
