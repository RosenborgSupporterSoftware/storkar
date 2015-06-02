#!/usr/bin/python
# -*- coding: utf-8 -*-

from base.http.ClientInfo import ClientInfo
from AppResponse import AppResponse
from Data import Data
import json
import os


class MatchBetEditor(AppResponse):


    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.dependency(js='jquery')
        self.dependency(js='/apps/rbkweb/MatchBetEditor.js')
        self.dependency(css='fontawesome')

        self.__idx = int(client.arg("idx"))
        self.data = Data()


    def get_round(self, idx):
        return idx


    def html(self):
        self.data.load()

        matches = self.data.get_matches_section()
        players = self.data.get_players_section()
        matchdata = matches[self.__idx]

        title = "%d: %s" % (self.get_round(self.__idx), matchdata['game'])

        html = []
        html += self.html_heading(title)
        html += self.html_body_open()
        html += self.html_header(title, sections=[{'link':'MatchBetting.py','title':'Kamp-indeks'}])
        html += self.html_content_open()

        html += [
            u'<div align="center" style="white-space:nowrap;">',
        ]

        html += [
            u'<table width="480" border="0" cellspacing="0" cellpadding="0"><tr>'
        ]

        if self.__idx > 1:
            html += [
                u'<td align="left"><a href="MatchBetEditor.py?idx=%d"><i class="fa fa-arrow-left"></i></a> <a href="MatchBetEditor.py?idx=%d">%s</a></td>' % (self.__idx-1, self.__idx-1, matches[self.__idx-1]['game'])
            ]
        else:
            html += [
                u'<td align="left"></td>'
            ]
        if self.__idx < (len(matches)-1):
            html += [
                u'<td align="right"><a href="MatchBetEditor.py?idx=%d">%s</a> <a href="MatchBetEditor.py?idx=%d"><i class="fa fa-arrow-right"></i></a></td>' % (self.__idx+1, matches[self.__idx+1]['game'], self.__idx+1)
            ]
        else:
            html += [
                u'<td align="right"></td>'
            ]
        html += [
            u'</tr></table><br/><p>'
        ]
 

        html += [
            u'<table width="480" border="1" bordercolor="black" cellspacing="0" cellpadding="5px">'
        ]

        idx = 0
        html += [
            u'<tr id="row%d">' % idx,
            u'<td align="right">%d</td>' % idx,
            u'<td colspan=4>',
            u'<input id="bet_top" type="text" name="bet_top" value="" size="53"/>',
            u'</td><td>',
            u'<a title="Submit bet" href="javascript:rbkweb.bets.editor.add_bet2(%d);"><i class="fa fa-download"></i></a>&nbsp;&nbsp;' % self.__idx,
            u'<a title="Set result" style="color:red;" href="javascript:rbkweb.bets.editor.set_result2(%d);"><i class="fa fa-gavel"></i></a>' % self.__idx,
            u'</td>',
            u'</tr>'
        ]

        if not 'bets' in matchdata:
            matchdata['bets'] = []

        for bet in matchdata['bets']:
            previous = self.data.get_bets_for_user(bet['user'], self.__idx)

            idx += 1
            halftime = ""
            if 'halftime' in bet:
                halftime = bet['halftime']

            color = u'white'
            if len(previous) == 0:
                color = u'orange'

            html += [
                u'<tr id="row%d">' % idx,
                u'<td align="right">%d</td>' % idx,
                u'<td bgcolor="%s">%s</td>' % (color, bet['user']),
                u'<td align="center">%s</td>' % bet['result'],
                u'<td align="center">%s</td>' % halftime
            ]
            if 'goals' in bet:
                html += [u'<td style="padding:0; spacing=0; margin:0;" valign="bottom">']
                for goalee in bet['goals']:
                    img = players['default']['image']
                    goalee = self.data.get_playerid(goalee)
                    name = goalee
                    if goalee in players:
                        name = players[goalee]['name']
                        if 'image' in players[goalee]:
                            img = players[goalee]['image']

                    html += [
                        u'<img style="padding:0;" src="%s" title="%s" alt="%s"/> ' % (img, name, goalee)
                    ]

                html += [u'</td>']
            else:
                html += [u'<td></td>']

            html += [
                u'<td align="center">',
                u'<a id="edit%d" href="javascript:rbkweb.bets.editor.edit_bet(%d);" title="Edit"><i class="fa fa-edit"></i></a>&nbsp;&nbsp;' % (idx, idx),
                u'<a id="del%d" title="Delete" style="color:red;" href="javascript:rbkweb.bets.editor.delete_bet(%d,%d);"><i class="fa fa-times"></i></a></td>' % (idx, self.__idx, idx)
            ]
            html += [
                u'</tr>'
            ]

        html += [
            u'<tr id="row%d">' % idx,
            u'<td>%d</td>' % (idx + 1),
            u'<td colspan=4>',
            u'<input id="bet" type="text" name="bet" value="" size="53"/>',
            u'</td><td>',
            u'<a id="submit" title="Submit bet" href="javascript:rbkweb.bets.editor.add_bet(%d);"><i class="fa fa-upload"></i></a>&nbsp;&nbsp;' % self.__idx,
            u'<a id="submitres" title="Set result" style="color:red;" href="javascript:rbkweb.bets.editor.set_result(%d);"><i class="fa fa-gavel"></i></a>' % self.__idx,
            u'</td>',
            u'</tr>',
            u'<tr id="row%d">' % (idx+1),
            u'<td></td>',
            u'<td colspan=4>',
            u'<textarea id="multibet" rows="4" cols="51" name="multibet"></textarea>',
            u'</td><td>',
            u'<a id="submit" title="Submit bet" href="javascript:rbkweb.bets.editor.add_multibet(%d);"><i class="fa fa-upload"></i></a>&nbsp;&nbsp;' % self.__idx,
            u'</td>',
            u'</tr>',
            u'</table>']

        html += [
            u'<table width="480">',
            u'<tr>',
            u'<td width="10%">',
            u'</td>',
            u'<td width="80%" align="center">',
            u'<a href="MatchView.py?idx=%d" id="stats" title="Stats Page"><i class="fa fa-bar-chart-o"></i></a>' % self.__idx,
            u'<a href="PlayerSettings.py" id="config" title="Configure Players" style="color:grey;"><i class="fa fa-gear"></i></a>',
            u'</td>',
            u'<td width="10%" align="right">',
            u'<a target="_blank" href="MatchBetBBCode.py?idx=%d" title="BBCode"><i class="fa fa-code"></i></a>' % self.__idx,
            u'</td>',
            u'</tr>',
            u'</table>'
        ]

        html += [
            u'</div>'
        ]

        html += self.html_content_close()
        html += self.html_footer()
        html += self.html_body_close()
        return html


def run(client):
    return MatchBetEditor(client)


if __name__ == "__main__":
    environ = dict(os.environ)
    environ['wsgi.url_scheme'] = 'http'
    page = run(ClientInfo(environ))
    print '\n'.join(page.html())
