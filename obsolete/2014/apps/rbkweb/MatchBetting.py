# -*- coding: utf-8 -*-

import os
import codecs
import json

from AppResponse import AppResponse
from Data import Data


# TODO: use Data instance


class MainView(AppResponse):


    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.dependency(js='jquery2')
        self.dependency(css='fontawesome')
        self.dependency(js='/apps/rbkweb/MatchEditor.js')
        self.data = Data()


    def get_round(self, idx):
        return idx


    def html(self):
        self.data.load()

        html = []
        html += self.html_heading()
        html += self.html_body_open()
        html += self.html_header()
        html += self.html_content_open()

        teams = self.data.get_teams_section()

        html += [u'<div align=center>']
        html += [u'<table border=1 bordercolor=black cellspacing=0 cellpadding=5>']

        matches = self.data.get_matches_section()
        prevdate = matches[1]['date']
        ongoing = False
        for idx in range(1, len(matches)):
            match = matches[idx]
            havestats = 'bets' in match and len(match['bets'])
            haveresults = 'result' in match
            if havestats and not haveresults:
                ongoing = True
                matchname = match['game']
                hometeam, awayteam = matchname.split(' - ', 2)
                hometeamname = hometeam
                if hometeam in teams:
                    if 'name' in teams[hometeam]:
                        hometeamname = teams[hometeam]['name']
                awayteamname = awayteam
                if awayteam in teams:
                    if 'name' in teams[awayteam]:
                        awayteamname = teams[awayteam]['name']
                havestats = 'bets' in match and len(match['bets'])
                haveresults = 'result' in match

                matchname = u'%s - %s' % (hometeamname, awayteamname)
                matchdate = match['date']
                color = "beige"
                html += [u'<tr bgcolor="%s">' % color,
                         u'<td align="right">%d</td>' % self.get_round(idx)]
                html += [u'<td><a href="MatchView.py?idx=%d">%s</a></td>' % (idx, matchname)]
                html += [u'<td>%s</td>' % matchdate,
                         u'<td><a href="MatchBetEditor.py?idx=%d">bets</a></td>' % idx]
                html += [u'<td><a href="MatchView.py?idx=%d">stats</a></td>' % idx]
                html += [u'<td>results</td>']

                html += ['</tr>']

        if ongoing:
            html += [u'<tr height=2 bgcolor="%s"><td colspan=6></td></tr>' % 'white']

        for idx in range(1, len(matches)):
            match = matches[idx]
            matchname = match['game']
            hometeam, awayteam = matchname.split(' - ', 2)
            hometeamname = hometeam
            if hometeam in teams:
                if 'name' in teams[hometeam]:
                    hometeamname = teams[hometeam]['name']
            awayteamname = awayteam
            if awayteam in teams:
                if 'name' in teams[awayteam]:
                    awayteamname = teams[awayteam]['name']
            havestats = 'bets' in match and len(match['bets'])
            haveresults = 'result' in match

            matchname = u'%s - %s' % (hometeamname, awayteamname)
            matchdate = match['date']
            if matchdate.find(' ') != -1:
                matchdate = matchdate.split(' ',2)[0]

            color = "white"
            if not haveresults:
                color = "beige"
                if not havestats:
                    color = "lightgrey"

            if prevdate[:7] != matchdate[:7]: # new month
                html += [u'<tr height=2 bgcolor="%s"><td colspan=6></td></tr>' % color]

            html += [u'<tr bgcolor="%s">' % color,
                     u'<td align="right">%d</td>' % self.get_round(idx)]
            if havestats:
                html += [u'<td><a href="MatchView.py?idx=%d">%s</a></td>' % (idx, matchname)]
            else:
                html += [u'<td>%s</td>' % matchname]
            html += [u'<td>%s</td>' % matchdate,
                     u'<td><a href="MatchBetEditor.py?idx=%d">bets</a></td>' % idx]

            if havestats:
                html += [u'<td><a href="MatchView.py?idx=%d">stats</a></td>' % idx]
            else:
                html += [u'<td>stats</td>']

            if haveresults:
                html += [u'<td><a href="StandingsView.py?idx=%d">results</a></td>' % idx]
            else:
                html += [u'<td>results</td>']

            html += ['</tr>']
            prevdate = matchdate

        html += [u'<tr height=2 bgcolor="white"><td colspan=6></td></tr>']
        html += [u'<tr><td align="right">%d</td>' % (idx+1)]
        html += [u'<td colspan=4><input id="match" type="text" value="" size="50"></td>']
        html += [u'<td align="center"><a id="submit" title="Add Match" href="#"><i class="fa fa-plus-square"></i></a>']
        html += [u'<a id="config" style="color:grey;" title="Configure Teams" href="TeamSettings.py"><i class="fa fa-gear"></i></a></td></tr>']
        html += [u'</table>']
        html += [u'<script>']
        html += [u'$("#submit").click(function() {']
        html += [u'rbkweb.matches.editor.add_match();']
        html += [u'});']
        html += [u'</script>']
        html += [u'</div>']

        html += self.html_content_close()
        html += self.html_footer()
        html += self.html_body_close()
        return html


def run(client):
    return MainView(client)

