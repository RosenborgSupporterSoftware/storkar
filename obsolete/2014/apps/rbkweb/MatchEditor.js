// vim:sw=4
window.rbkweb = window.rbkweb || {};
rbkweb.matches = rbkweb.matches || {};
rbkweb.matches.editor = rbkweb.matches.editor || {};

(function($) {
    "use strict";

    rbkweb.matches.editor.add_match = function() {
        var value = $('#match').val();
        var data = { match: value };
        $.ajax({url: "/apps/rbkweb/request/post/AddMatch.py?" +
                     "data=" + JSON.stringify(data),
                type: "GET"})
        .done(function(){
            window.location.reload(true);
        });
    };

})(jQuery);
