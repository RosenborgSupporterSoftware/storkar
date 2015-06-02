// vim:sw=4
window.rbkweb = window.rbkweb || {};
rbkweb.bets = rbkweb.bets || {};
rbkweb.bets.editor = rbkweb.bets.editor || {};

(function($) {
    "use strict";

    rbkweb.bets.editor.add_bet = function(idx) {
        var value = $('#bet').val();
        var data = { bet: value };
        $.ajax({url: "/apps/rbkweb/request/post/AddBet.py?idx=" + idx +
                     "&data=" + JSON.stringify(data),
                type: "GET"})
        .done(function(){
            window.location.reload(true);
        });
    };

    rbkweb.bets.editor.add_multibet = function(idx) {
        var value = $('#multibet').val();
        var data = { multibet: value };
        $.ajax({url: "/apps/rbkweb/request/post/AddBet.py?idx=" + idx +
                     "&data=" + JSON.stringify(data),
                type: "GET"})
        .done(function(){
            window.location.reload(true);
        });
    };

    rbkweb.bets.editor.add_bet2 = function(idx) {
        var value = $('#bet_top').val();
        var data = { bet: value };
        $.ajax({url: "/apps/rbkweb/request/post/AddBet.py?idx=" + idx +
                     "&data=" + JSON.stringify(data),
                type: "GET"})
        .done(function(){
            window.location.reload(true);
        });
    };

    rbkweb.bets.editor.edit_bet = function(row) {
        var sel = $('#row'+row+ ' td');
        var halftime = sel.eq(3).text();
        if (halftime == '') { halftime = '-'; }
        var text = sel.eq(1).text() + ',' + sel.eq(2).text() + ',' + halftime;
        var goalees = sel.eq(4);
        if (goalees.size()) {
            goalees.find('img').each(function(idx) {
                text += ',' + $(this).attr('alt');
            });
        }
        $('#bet').val(text);
        $('#bet').focus();
    };

    rbkweb.bets.editor.delete_bet = function(idx,row) {
        var sel = $('#row'+row+ ' td');
        var user = sel.eq(1).text();
        $.ajax({url: "/apps/rbkweb/request/post/DeleteBet.py?idx=" + idx +
                     "&row=" + row + "&user=" + user,
                type: "GET"})
        .done(function(){
            window.location.reload(true);
        });
    };

    rbkweb.bets.editor.set_result = function(idx) {
        var value = $('#bet').val();
        var data = { result: value };
        $.ajax({url: "/apps/rbkweb/request/post/AddResult.py?idx=" + idx +
                     "&data=" + JSON.stringify(data),
                type: "GET"})
        .done(function(){
            window.location.reload(true);
        });
    };

    rbkweb.bets.editor.set_result2 = function(idx) {
        var value = $('#bet_top').val();
        var data = { result: value };
        $.ajax({url: "/apps/rbkweb/request/post/AddResult.py?idx=" + idx +
                     "&data=" + JSON.stringify(data),
                type: "GET"})
        .done(function(){
            window.location.reload(true);
        });
    };

})(jQuery);
