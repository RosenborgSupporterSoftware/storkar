# -*- coding: utf-8 -*-
# vim:sw=4

import json
import codecs
import os

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

class MatchBBCode(AppResponse):

    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.dependency(js='jquery')
        self.__idx = int(client.arg('idx'))
        self.data = Data()


    def get_round(self, idx):
        return idx


    def html(self):
        self.data.load()

        body = []
        body += self.html_heading()
        body += self.html_body_open()
        body += [u'<pre>']

        html = []
        gameidx = self.__idx


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

        (hometeam, awayteam) = match['game'].split(' - ', 2)
        logos = self.data.get_logos_section()
        assert logos
        assert hometeam in logos
        assert awayteam in logos

        teams = self.data.get_teams_section()

        hometeamname = hometeam
        if 'name' in teams[hometeam]:
            hometeamname = teams[hometeam]['name']

        awayteamname = awayteam
        if 'name' in teams[awayteam]:
            awayteamname = teams[awayteam]['name']

        stats = matchobj.get_stats()

        leftalign = u"middle"
        rightalign = u"top"
        if matchobj.is_home_game():
            leftalign, rightalign = rightalign, leftalign

        html += [u'<div align="center">\n']
        html += [u'<table cellspacing="30">']
        # html += [u'<tr><td colspan="3" align="center">[size=26]Runde %d[/size]</td>' % self.get_round(self.__idx)]
        # html += [u'</tr>']
        html += [u'<tr height="110">']
        html += [u'<td align="center" valign="%s">' % leftalign]
        html += [u'<img src="%s" title="%s"/>' % (logos[hometeam], hometeamname)]
        html += [u'</td>']
        html += [u'<td valign="middle">[size=26]mot[/size]</td>']

        html += [u'<td align="center" valign="%s">' % rightalign]
        html += [u'<img src="%s" title="%s"/>' % (logos[awayteam], awayteamname)]
        html += [u'</td>']
        html += [u'</tr>']
        html += [u'</table>']

        html += [u'<table cellpadding="1" border="0" cellspacing="0" bgcolor="black">']
        html += [u'<tr><td>']
        html += [u'<table cellpadding="0" border="0" cellspacing="0" bgcolor="black">']
        html += [u'<tr><td>']

        rows = 6
        cols = 6
        if awayteam == u'Brann': rows = 11
        if hometeam == u'Orkla' or hometeam == u'Kolstad': cols = 11

        html += [u'<table cellpadding="2" border="0" bordercolor="black" cellspacing="1">']
        html += [u'<tr height="28">']
        html += [u'<td background="%s" align="center" width="26"></td>' % self.data.get_imageurl("img/xxx.png")]
        for col in range(0, cols):
            html += [u'<td background="%s" align="center" width="26">[size=12]%d[/size]</td>' % (self.data.get_imageurl("img/xxx.png"), col) ]
        html += [u'</tr>']

        char = 'b'
        flip = 1
        if matchobj.is_home_game():
            char = 'h'
            flip = -1

        for y in range(1, rows+1):
            html += [u'<tr height="28">']
            html += [u'<td background="%s" align="center" width="26">[size=12]%d[/size]</td>' % (self.data.get_imageurl(u"img/xxx.png"), (y-1))]
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
                    html += [u'<td background="%s" align="center" width="26">[size=12]%d[/size]</td>' % (bg, result_matrix[score])]
            html += [u'</tr>']
        html += [u'</table>']
        html += [u'</td></tr>']
        html += [u'</table>']
        html += [u'</td></tr>']
        html += [u'</table>']
        if stats.get('bets', 0) == 0:
            html += [u'\n\n']
        html += [u'</div>\n']

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

            html += [u'<div align="center">']
            html += [u'<table cellspacing="0" cellpadding="0">']
            html += [u'<tr height="30"></tr>']

            if len(goals_advantage) > 16:
                html += [u'<tr>']

                html += [u'<td width="50%%" align="center"><img src="%s"/></td>' % goals_for_imgurl]
                html += [u'<td width="50%%" align="center"><img src="%s"/></td>' % goals_against_imgurl]
                html += [u'</tr><tr>']

                html += [u'<td align="center">[size=12]Scorede m&aring;l[/size]</td>']
                html += [u'<td align="center">[size=12]Innslupne m&aring;l[/size]</td>']
                html += [u'</tr><tr>']
                html += [u'<td align="center" colspan="2"><img src="%s"/></td>' % goals_advantage_imgurl]
                html += [u'</tr><tr>']
                html += [u'<td align="center" colspan="2">[size=12]M&aring;lforskjell[/size]</td>']
                html += [u'</tr>']

            else:
                html += [u'<tr>']
                
                html += [u'<td width="33%%" align="center"><img src="%s"/></td>' % goals_for_imgurl]
                html += [u'<td width="33%%" align="center"><img src="%s"/></td>' % goals_against_imgurl]
                html += [u'<td width="33%%" align="center"><img src="%s"/></td>' % goals_advantage_imgurl]
                html += [u'</tr><tr>']
                html += [u'<td align="center">[size=12]Scorede m&aring;l[/size]</td>']
                html += [u'<td align="center">[size=12]Innslupne m&aring;l[/size]</td>']
                html += [u'<td align="center">[size=12]M&aring;lforskjell[/size]</td>']
                html += [u'</tr>']

            html += [u'</table>']
            html += [u'</div>\n']


            # player confidence
            players = self.data.get_players_section()
            dummy = players['default']
            dummy_image = dummy['image']

            goalees = matchobj.get_goalees()

            goalcount = stats['goals_for']
            score = float(goalcount) / float(stats['bets'])
            intscore = int("%.0f" % score)

            # fix for multiple goals
            if intscore > 1:
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
            html += [u'<div align="center">',
                     u'<table width="400">']
            html += [u'<tr height="30"></tr>']
            index = 0
            for goalee in goalees:
                if not goalee: continue
                goals = goalee[0]
                confidence = goalee[1]
                shortname = goalee[2]
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

                html += [u'<tr><td><img src="%s"/></td>' % imgurl,
                         u'<td align="center">[size=12]%d[/size]</td>' % goals,
                         u'<td align="center">[size=12]%.0f%%[/size]</td>' % confidence,
                         u'<td>[size=12]%s[/size]</td>' % fullname,
                         u'<td align="right" width="100"><img src="%s"/></td></tr>' % graphurl]

                if index < intscore:
                    betgoalees += [fullname]
                index += 1
                if index == intscore:
                    html += [u'<tr height="3" bgcolor="black"><td colspan="5"></td></tr>']
            html += [u'</table></div>\n']


            # pie chart
            pie_imgurl = Chart.get_results_pie_imgurl(goals_advantage, mid, 400, 200)
            html += [u'<div align="center">',
                     u'<table width="400">',
                     u'<tr height="30"></tr>',
                     u'<tr><td align="center">[b]RBKweb.no\'s kollektive visdom tilsier:[/b]</td></tr>',
                     u'<tr height="200"><td align="center" valign="middle" background="%s">' % pie_imgurl,
                     u'[b][size=18]%s - %s[/size]\n[size=16]%s (%s)[/size][/b]\n\n' % (hometeamname, awayteamname, stats['result'], stats['halftime']),
                     u'[b]' + '\n'.join(betgoalees) + '[/b]',
                     u'</td></tr></table>',
                     u'</div>\n']

            # stats table
            html += [u'<div align="center">']
            html += [u'<table border="1" bordercolor="black" cellspacing="0" cellpadding="5">']
            html += [u'<tr><td></td><td></td><td>[size=12]tips[/size]</td></tr>']

            homegoals = stats['goals_for']
            awaygoals = stats['goals_against']
            if not matchobj.is_home_game():
                homegoals, awaygoals = awaygoals, homegoals
            html += [u'<tr><td>[size=12]Akkumulert resultat:[/size]</td><td align="center">[size=12]%d-%d[/size]</td><td align="center">[size=12]%d[/size]</td></tr>' % (homegoals, awaygoals, stats['bets'])]
            html += [u'<tr><td>[size=12]Snittresultat:[/size]</td><td align="center">[size=12]%s[/size]</td><td align="center">[size=12]%d[/size]</td></tr>' % (stats['result_accurate'], stats['bets'])]

            html += [u'<tr><td>[size=12]Snittresultat, pause:[/size]</td><td align="center">[size=12]%s[/size]</td><td align="center">[size=12]%d[/size]</td></tr>' % (stats['halftime_accurate'], stats['pause_bets'])]
            html += [u'</table>']


            # bet history
            if len(bethistory) > 1:
                if not 'result' in match: # strip off ongoing data
                    bethistory = bethistory[0:-1]
                    hithistory = hithistory[0:-1]

                #width = 38 + 27 * len(bethistory)
                width = 400
                betcountgraph = Chart.get_betcount_imgurl(bethistory, hithistory, width, 120)

                html += [u'\n\n']
                html += [u'Tips og treff de foregående rundene:\n']
                html += [u'<img src="%s">' % betcountgraph]

                html += [u'\n\n</div>']

        contents = u''.join(html)
        contents = contents.replace(u'<', u'&lt;')
        contents = contents.replace(u'>', u'&gt;')

        body += [contents]
        body += [u'</pre>']
        body += self.html_body_close()
        return body


def run(client):
    return MatchBBCode(client)


if __name__ == "__main__":
    class FakeClient:
        def __init__(self):
            self.args = { 'idx': 48 } # RBK-Ulf

        def arg(self, key):
            return self.args[key]

        def get_user(self):
            return 'larsa'

    generator = run(FakeClient())
    print '\n'.join(generator.html()).encode('utf-8', 'ignore')

