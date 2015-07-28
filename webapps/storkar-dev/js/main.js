require.config({
    baseUrl: '/js/',
    paths: {
        jquery: 'libs/jquery/jquery',
        underscore: 'libs/lodash/lodash',
        lodash: 'libs/lodash/lodash',
        backbone: 'libs/backbone/backbone',
        layoutmanager: 'libs/layoutmanager/backbone.layoutmanager'
    }
});

define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'app',
    'router',
    'modules/team'
],
function($, _, Backbone, Layout, App, Router, Team)
{
    var promise = App.initialize();
    App.teams = new Team.Collection();
    var teamsfetched = App.teams.fetch();

    $.when(promise, teamsfetched).then(function() {
        var router = new Router();
        App.router = router;
        Backbone.history.start({pushState: false, root: '/'});
    });
});
