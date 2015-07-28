require.config({
    baseUrl: '/js/',
    paths: {
        jquery: 'libs/jquery/jquery',
        underscore: 'libs/lodash/lodash',
        lodash: 'libs/lodash/lodash',
        backbone: 'libs/backbone/backbone',
        layoutmanager: 'libs/layoutmanager/backbone.layoutmanager'
    },
    deps: [
        'jquery',
        'underscore'
    ]
});
