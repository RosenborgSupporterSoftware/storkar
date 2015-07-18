require.config({
    paths: {
        jquery: 'libs/jquery/jquery',
        underscore: 'libs/lodash/lodash',
        lodash: 'libs/lodash/lodash',
        backbone: 'libs/backbone/backbone',
        layoutmanager: 'libs/layoutmanager/backbone.layoutmanager'
    }
});

require(['app'], function(App) {
    App.initialize();
});
