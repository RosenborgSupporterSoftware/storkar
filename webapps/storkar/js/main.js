define(
    "main",
[
    'backbone',
    'app',
    'router'
],
function(Backbone, App, AppRouter)
{
    var promise = App.initialize();

    $.when(promise).then(function() {
        var app_router = new AppRouter();
        App.router = app_router;
        Backbone.history.start({pushState: false, root: '/'});
    });
});
