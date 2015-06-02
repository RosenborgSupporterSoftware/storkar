#!/usr/bin/python
# -*- coding: utf-8 -*-

# vim:sw=4

import os
import codecs
import json

from AppResponse import AppResponse

from rbkweb.Match import Match
from rbkweb.Data import Data
from rbkweb.Chart import Chart

# - match-list view [add bet, set result], view bbcode
# - match view [add match]
# - bet standing
#
# - antall tips-graf

# see https://developers.google.com/chart/image/docs/making_charts
# and https://developers.google.com/chart/image/docs/chart_params

class MatchView(AppResponse):

    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.dependency(js='jquery')
        self.__idx = int(client.arg('idx'))
        self.data = Data()


    def get_round(self, idx):
        return idx


    def html(self):
        self.data.load()

        html = []
        html += self.html_heading()
        html += self.html_body_open()

        gameidx = self.__idx

        html += self.html_header(u'Kamp %d' % self.get_round(gameidx), sections=[{'link':'MatchBetting.py','title':'Kamp-indeks'}])
        html += self.html_content_open()

        matches = self.data.get_matches_section()

        html += [
            u'<div align=center>',
        ]

        html += [
            u'<table width=480 border="0" cellspacing="0" cellpadding="0"><tr>'
        ]

        if self.__idx > 1:
            html += [
                u'<td align="left"><a href="MatchView.py?idx=%d"><i class="fa fa-arrow-left"></i></a> <a href="MatchView.py?idx=%d">%s</a></td>' % (self.__idx-1, self.__idx-1, matches[self.__idx-1]['game'])
            ]
        else:
            html += [
                u'<td align="left"></td>'
            ]
        if self.__idx < (len(matches)-1) and 'bets' in matches[self.__idx + 1] \
              and len(matches[self.__idx+1]['bets']):
            html += [
                u'<td align="right"><a href="MatchView.py?idx=%d">%s</a> <a href="MatchView.py?idx=%d"><i class="fa fa-arrow-right"></i></a></td>' % (self.__idx+1, matches[self.__idx+1]['game'], self.__idx+1)
            ]
        else:
            html += [
                u'<td align="right"></td>'
            ]
        html += [
            u'</tr></table><br/><p>'
        ]

        # FIXME: create subfunction
        confidences = {}
        bethistory = []
        hithistory = []
        for game in range(1,gameidx+1):
            matchdata = self.data.get_matches_section()[game]
            match = Match(matchdata, self.data)
            stats = match.get_stats()
            bethistory += [match.get_bet_count()]
            hithistory += [match.get_hit_count()]
            goalees = match.get_goalees()
            tagged = {}
            for goalee in goalees:
                shortname = goalee[2]
                confidence = goalee[1]
                if not shortname in confidences:
                    confidences[shortname] = []
                confidences[shortname].append(confidence)
                tagged[shortname] = 1
            for goalee in confidences:
                if not goalee in tagged:
                    confidences[goalee].append(0.0)


        # start
        match = self.data.get_matches_section()[gameidx]
        matchobj = Match(match, self.data)

        result_matrix = matchobj.get_score_matrix('result')
        halftime_matrix = matchobj.get_score_matrix('halftime')

        goals_for = Data.get_score_histogram(result_matrix, 0, 1)
        goals_against = Data.get_score_histogram(result_matrix, 1, 0)
        goals_advantage = Data.get_score_histogram(result_matrix, 1, 1)

        maxcount = max(goals_for + goals_against + goals_advantage)
        while maxcount % 4 != 0: maxcount += 1

        if matchobj.is_home_game():
            goals_advantage.reverse()
            goals_for, goals_against = goals_against, goals_for

        mid = (len(goals_advantage)-1)/2

        pie_imgurl = Chart.get_results_pie_imgurl(goals_advantage, mid, 200, 120)

        (hometeam, awayteam) = match['game'].split(u' - ', 2)
        logos = self.data.get_logos_section()
        assert logos
        assert hometeam in logos
        assert awayteam in logos

        stats = matchobj.get_stats()

        teams = self.data.get_teams_section()

        leftalign = "middle"
        rightalign = "top"
        if matchobj.is_home_game():
            leftalign, rightalign = rightalign, leftalign

        hometeamname = hometeam
        if 'name' in teams[hometeam]:
            hometeamname = teams[hometeam]['name']
        awayteamname = awayteam
        if 'name' in teams[awayteam]:
            awayteamname = teams[awayteam]['name']

        html += [u'<div align="center">']
        html += [u'<table cellspacing=30>']
        html += [u'<tr height=110>']
        html += [u'<td align=center valign=%s>' % leftalign]
        html += [u'<img src="%s" title="%s"/>' % (logos[hometeam], hometeamname)]
        html += [u'</td>']
        html += [u'<td valign=middle><font size=+4>mot</font></td>']

        html += [u'<td align=center valign=%s>' % rightalign]
        html += [u'<img src="%s" title="%s"/>' % (logos[awayteam], awayteamname)]
        html += [u'</td>']
        html += [u'</tr>']
        html += [u'</table>']
        html += [u'<p>']

        html += [u'<table cellpadding="1" border="0" cellspacing="0" bgcolor="black">']
        html += [u'<tr><td>']
        html += [u'<table cellpadding="0" border="0" cellspacing="0" bgcolor="black">']
        html += [u'<tr><td>']
        html += [u'<table cellpadding="2" border="0" bordercolor="black" cellspacing="1">']
        html += [u'<tr height="28">']

        rows = 6
        cols = 6
        if awayteam == u'Brann': rows = 11
        if hometeam == u'Orkla' or hometeam == u'Kolstad': cols = 11

        html += [u'<td background="%s" align="center" width="26"></td>' % self.data.get_imageurl("img/xxx.png")]
        for col in range(0, cols):
            html += [u'<td background="%s" align="center" width="26">%s</td>' % (self.data.get_imageurl("img/xxx.png"), col)]
        html += [u'</tr>']

        char = 'b'
        flip = 1
        if matchobj.is_home_game():
            char = 'h'
            flip = -1

        for y in range(1, rows+1):
            html += [u'<tr height="28">']
            html += [u'<td background="%s" align="center" width="26">%d</td>' % (self.data.get_imageurl("img/xxx.png"), (y-1))]
            for x in range(1, cols+1):
                d = x - y
                score = u'%d-%d' % ((y-1), (x-1))
                bg = u'img/%s00.png' % char
                if d == 1: bg = u'img/%s10.png' % char
                if d > 1: bg = u'img/%s20.png' % char
                if d == -1: bg = u'img/%s01.png' % char
                if d < -1: bg = u'img/%s02.png' % char
                bg = self.data.get_imageurl(bg)
                if not score in result_matrix:
                    html += [u'<td background="%s" align="center" width="26"></td>' % bg]
                else:
                    html += [u'<td background="%s" align="center" width="26">%d</td>' % (bg, result_matrix[score])]
            html += [u'</tr>']
        html += [u'</table>']
        html += [u'</td></tr>']
        html += [u'</table>']
        html += [u'</td></tr>']
        html += [u'</table>']
        html += [u'</div>']

        #if not 'bets' in match or len(match['bets']) == 0:
        #else:

        if stats.get('bets', 0) > 0:
            if len(goals_for) > 10: goals_for = goals_for[0:9]
            if len(goals_against) > 10: goals_against = goals_against[0:9]
            while len(goals_for) < 6: goals_for.append(0)
            while len(goals_against) < 6: goals_against.append(0)
    
    
            width = 20 + 12 * len(goals_for)
            goals_for_imgurl = Chart.get_goals_imgurl(goals_for, 0, width, 100, maxcount)
    
            width = 20 + 12 * len(goals_against)
            goals_against_imgurl = Chart.get_goals_imgurl(goals_against, 0, width, 100, maxcount)
    
            width = 20 + 12 * len(goals_advantage)
            goals_advantage_imgurl = Chart.get_goals_imgurl(goals_advantage, mid, width, 100, maxcount, True)
    
            html += [u'<p></p>']
            html += [u'<div align=center>']
            html += [u'<table cellspacing=0 cellpadding=0>']
            html += [u'<tr height=30>']
            html += [u'</tr>']

            if len(goals_advantage) > 16:
                html += [u'<tr>']
                
                html += [u'<td width="50%%" align="center"><img src="%s"/></td>' % goals_for_imgurl]
                html += [u'<td width="50%%" align="center"><img src="%s"/></td>' % goals_against_imgurl]
                html += [u'</tr><tr>']
                html += [u'<td align="center">Scorede m&aring;l</td>']
                html += [u'<td align="center">Innslupne m&aring;l</td>']
                html += [u'</tr><tr>']
                html += [u'<td align="center" colspan="2"><img src="%s"/></td>' % goals_advantage_imgurl]
                html += [u'</tr><tr>']
                html += [u'<td align="center" colspan="2">M&aring;lforskjell</td>']
                html += [u'</tr>']
            else:
                html += [u'<tr>']
                
                html += [u'<td width="33%%" align="center"><img src="%s"/></td>' % goals_for_imgurl]
                html += [u'<td width="33%%" align="center"><img src="%s"/></td>' % goals_against_imgurl]
                html += [u'<td width="33%%" align="center"><img src="%s"/></td>' % goals_advantage_imgurl]
                html += [u'</tr><tr>']
                html += [u'<td align="center">Scorede m&aring;l</td>']
                html += [u'<td align="center">Innslupne m&aring;l</td>']
                html += [u'<td align="center">M&aring;lforskjell</td>']
                html += [u'</tr>']
            html += [u'<tr height=30>']
            html += [u'</tr>']

            html += [u'</table>']
            html += [u'</div>']


            # player confidence
            players = self.data.get_players_section()
            dummy = players['default']
            dummy_image = dummy['image']

            goalees = matchobj.get_goalees()

            goalcount = stats['goals_for']
            score = (float(goalcount) / float(stats['bets'])) if stats['bets'] > 0 else 0
            intscore = int(u"%.0f" % score)

            if intscore > 1:
                # fix for multiple goals
                array = []
                for goalee in goalees[0:intscore-1]:
                    for i in range(1,intscore):
                        array += [(goalee[0]/i, goalee[1]/i, goalee[2])]
                array = sorted(array, reverse=True)
                for i in range(intscore,len(array)):
                    for j in range(0,i):
                        if not array[j]: continue
                        if not array[i]: continue
                        if array[i][2] == array[j][2]:
                            array[i] = None
                goalees[0:intscore-1] = array

            betgoalees = []
            html += [u'<div align="center"><table width="400">']
            index = 0
            for goalee in goalees:
                if not goalee: continue
                goals = goalee[0]
                confidence = goalee[1]
                shortname = goalee[2]
                # TODO: go from alias to keyname
                assert shortname in players, "unknown player '%s'" % shortname
                fullname = players[shortname]['name']

                imgurl = dummy_image
                if 'image' in players[shortname]:
                    imgurl = players[shortname]['image']
                imgurl = self.data.get_imageurl(imgurl)

                confidencedata = []
                if shortname in confidences:
                    confidencedata = confidences[shortname]
                while len(confidencedata) < 9: confidencedata.insert(0, 0.0)
                if len(confidencedata) > 9: confidencedata = confidencedata[-9:]
                graphurl = Chart.get_confidence_imgurl(confidencedata, 100, 25)

                html += [u'<tr><td><img src="%s"/></td><td align="center">%d</td><td align="center">%.0f%%</td><td>%s</td><td align="right"><img src="%s"/></td></tr>' % (imgurl, goals, confidence, fullname, graphurl)]

                if index < intscore:
                    betgoalees += [fullname]
                index += 1
                if index == intscore:
                    html += [u'<tr height="3" bgcolor="black"><td colspan="5"></td></tr>']
            html += [u'</table></div><p>']


            # pie chart
            pie_imgurl = Chart.get_results_pie_imgurl(goals_advantage, mid, 400, 200)
            html += [u'<div align="center">',
                     u'<table width=400>',
                     u'<tr>RBKweb.no\'s kollektive visdom tilsier:</tr>',
                     u'<tr height=200><td align=center valign="middle" background="%s">' % pie_imgurl,
                     u'<b><font size=+1>%s - %s<br>%s (%s)</font></b><br><br>' % (hometeamname, awayteamname, stats['result'], stats['halftime']),
                     u'<b>' + '<br>'.join(betgoalees) + '</b>',
                     u'</td></tr></table>',
                     u'</div><br><br>']

            # stats table
            html += [u'<div align="center">']
            html += [u'<table border="1" bordercolor="black" cellspacing="0" cellpadding="5">']
            html += [u'<thead><tr><td></td><td></td><td>tips</td></tr></thead>']

            homegoals = stats['goals_for']
            awaygoals = stats['goals_against']
            if not matchobj.is_home_game():
                homegoals, awaygoals = awaygoals, homegoals
            html += [u'<tr><td>Akkumulert resultat:</td><td align="center">%d-%d</td><td align="center">%d</td></tr>' % (homegoals, awaygoals, stats['bets'])]
            html += [u'<tr><td>Snittresultat:</td><td align="center">%s</td><td align="center">%d</td></tr>' % (stats['result_accurate'], stats['bets'])]
            html += [u'<tr><td>Snittresultat, pause:</td><td align="center">%s</td><td align="center">%d</td></tr>' % (stats['halftime_accurate'], stats['pause_bets'])]
            html += [u'</table>']


            # bet history
            if len(bethistory) > 1:
                if not 'result' in match: # strip off ongoing data
                    bethistory = bethistory[0:-1]
                    hithistory = hithistory[0:-1]

                #width = 38 + 27 * len(bethistory)
                width = 400
                betcountgraph = Chart.get_betcount_imgurl(bethistory, hithistory, width, 120)

                html += [u'<br><br>']
                html += [u'Historisk antall tips og treff<br>']
                html += [u'<img src="%s"/><br>' % betcountgraph]

        html += [u'<table width="400"><tr><td width="100%" align="right">']
        html += [u'<a target="_blank" href="MatchBBCode.py?idx=%d" title="BBCode"><i class="fa fa-code"></i></a>' % self.__idx]
        html += [u'</td></tr></table>']

        html += [u'</div>']


        # standard stuff
        html += self.html_content_close()
        html += self.html_footer()
        html += self.html_body_close()
        return html


def run(client):
    return MatchView(client)

