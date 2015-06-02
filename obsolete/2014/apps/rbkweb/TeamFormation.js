window.rbkweb = window.rbkweb || {};
rbkweb.teamformation = rbkweb.teamformation || {};

(function ($) {

    rbkweb.teamformation.update = function() {
        $.ajax({url: "TeamFormationHTML.py?team=" + encodeURIComponent($("#input").val()),
                type: "GET"})
        .done(function(data){
            $("#formation").html(data);
        });

    };

})(jQuery);
