# -*- coding: utf-8 -*-
# vim:sw=4

from AppResponse import AppResponse
from Data import Data
from Standings import Standings


class StandingsView(AppResponse):


    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.dependency(js='jquery2')
        self.dependency(css='fontawesome')
        self.__idx = int(client.arg("idx"))
        self.data = Data()
        self.standings = Standings(self.data)


    def get_round(self, idx):
        return idx


    def html_tableheader(self):
        html = [
            u'<tr height="5"></tr>',
            u'<tr height="0" bgcolor="black"><td colspan="8"></td></tr>',
            u'<tr>',
            u'    <td bgcolor="white" align="center"><img title="Plassering" src="%s"/></td>' % self.data.get_imageurl(u'img/icon-trophy.png'),
            u'    <td bgcolor="white" align="left"><img title="Deltagernavn" src="%s"/> <img src="%s" title="Jackpot"/></td>' % (self.data.get_imageurl(u'img/icon-player.png'), self.data.get_imageurl(u'img/icon-ball-crop-high.png')),
            u'    <td bgcolor="white" align="center"><img title="Sluttresultat" src="%s"/></td>' % self.data.get_imageurl(u'img/icon-whistle.png'),
            u'    <td bgcolor="white" align="center"><img title="Pauseresultat" src="%s"/></td>' % self.data.get_imageurl(u'img/icon-clock.png'),
            u'    <td bgcolor="white" align="center"><img title="M&aring;lscorere" src="%s"/></td>' % self.data.get_imageurl(u'img/icon-goal.png'),
            u'    <td bgcolor="white" align="center"><img title="Tippetegn HUB" src="%s"/></td>' % self.data.get_imageurl(u'img/icon-tipping.png'),
            u'    <td bgcolor="white" align="center"><img title="Poeng" src="%s"/></td>' % self.data.get_imageurl(u'img/icon-score.png'),
            u'    <td bgcolor="white"></td></tr>',
            u'</tr>',
            u'<tr height="0" bgcolor="black"><td colspan="8"></td></tr>'
        ]
        return html


    def html(self):
        self.data.load()

        html = []
        html += self.html_heading()
        html += self.html_body_open()
        html += self.html_header('Resultater', sections=[{'link':'MatchBetting.py','title':'Kamp-indeks'}])
        html += self.html_content_open()

        html += [
            u'<div align="center">'
        ]

        matches = self.data.get_matches_section()
        match = matches[self.__idx]

        # round score

        html += [
            u'<table width="480" border="0" cellspacing="0" cellpadding="0"><tr>'
        ]

        if self.__idx > 1:
            html += [
                u'<td align="left"><a href="StandingsView.py?idx=%d"><i class="fa fa-arrow-left"></i></a> <a href="StandingsView.py?idx=%d">%s</a></td>' % (self.__idx-1, self.__idx-1, matches[self.__idx-1]['game'])
            ]
        else:
            html += [
                u'<td align="left"></td>'
            ]
        if self.__idx < (len(matches)-1) and 'result' in matches[self.__idx + 1]:
            html += [
                u'<td align="right"><a href="StandingsView.py?idx=%d">%s</a> <a href="StandingsView.py?idx=%d"><i class="fa fa-arrow-right"></i></a></td>' % (self.__idx+1, matches[self.__idx+1]['game'], self.__idx+1)
            ]
        else:
            html += [
                u'<td align="right"></td>'
            ]
        html += [
            u'</tr></table><br/><p>'
        ]
        html += [
            u'<table width=480 border="1" cellspacing="0" cellpadding="5" bordercolor="black" background="%s">' % self.data.get_imageurl(u'img/pattern.jpg'),
            u'<tr><td border="0">',
            u'<table width="100%" cellpadding="2" cellspacing="0" border="0">',
            u'<tr><td align="center" colspan="8"><b><font size="+3" color="white">',
            u'Runde %d:<br>' % self.get_round(self.__idx),
            match['game'],
            u'</font></b></td></tr>'
        ]

        html += self.html_tableheader()

        idx = 1
        plass = 1
        prevscore = 0
        for score in self.standings.get_score(self.__idx, dict()):
            if score[0] != prevscore:
                plass = idx

            html += [
                u'<tr height="5"></tr>',
                u'<tr>',
                u'<td bgcolor="white" align="center">%d</td>' % plass]
            if score[6]:
                html += [
                    u'<td bgcolor=white>%s' % score[5]
                ]
                for jackpot in score[7].split('\n'):
                    if jackpot != '':
                        html += [
                            ' <img src="%s" title="Jackpot!"/>' % self.data.get_imageurl(u'img/icon-ball-crop.png')
                        ]
                html += [u'</td>']
            else:
                html += [
                    u'<td bgcolor="white">%s</td>' % score[5]
                ]
            html += [
                u'<td bgcolor="white" align="center">%d</td>' % score[1],
                u'<td bgcolor="white" align="center">%d</td>' % score[2],
                u'<td bgcolor="white" align="center">%d</td>' % score[3],
                u'<td bgcolor="white" align="center">%d</td>' % score[4],
                u'<td bgcolor="white" align="center">%d</td>' % score[0]
            ]

            if score[0] == 1:
                html += [ u'<td bgcolor="white"></td>' ]
            else:
                html += [ u'<td bgcolor="white" align="center"><img src="%s" title="%s"/></td>' % (self.data.get_imageurl(u'img/icon-stats-crop.png'), score[6]) ]
            html += [
                u'</tr>'
            ]
            idx += 1
            prevscore = score[0]

        html += [
            u'</table>',
            u'</td></tr>',
            u'</table>',
        ]

        html += [
            u'<table width=480 border="1" cellspacing=0 cellpadding=5 bordercolor="white">',
            u'<tr><td align=right><a title="BBCode" target="_blank" href="StandingsBBCode.py?idx=%d&mode=round"><i class="fa fa-code"></i></a></td></tr>' % self.__idx,
            u'</table>',
            u'<p>'
        ]

        # series standings
        misses = {}
        score = self.standings.get_score(1, misses)
        matchname = matches[1]['game']
        for i in range(0, len(score)):
            score[i] = (score[i][0],
                        score[i][1],
                        score[i][2],
                        score[i][3],
                        score[i][4],
                        score[i][5],
                        u'%d: %s (%d)' % (self.get_round(1), matchname, score[i][0]),
                        score[i][7],
                        score[i][8])

        if self.__idx > 1:
            for i in range(2, self.__idx+1):
                matchname = u'%d: %s' % (self.get_round(i), matches[i]['game'])
                newscore = self.standings.get_score(i, misses)
                score = self.standings.merge_scores(score, newscore, matchname)

        html += [
            u'<table width=480 border="1" cellspacing=0 cellpadding=5 bordercolor="black" background="%s">' % self.data.get_imageurl(u'img/pattern.jpg'),
            u'<tr><td border=0>',
            u'<table width="100%" cellpadding="2" cellspacing=0 border="0">',
            u'<tr><td align="center" colspan="8"><b><font size=+3 color=white>',
            u'Tabell, runde %d' % self.get_round(self.__idx),
            u'</font></b></td></tr>'
        ]

        html += self.html_tableheader()

        idx = 1
        plass = 1
        prevscore = 0
        for entry in score:
            if entry[0] != prevscore:
                if plass <= 3 and idx > 3:
                    html += [
                        u'<tr height="5"></tr>',
                        u'<tr height="0" bgcolor="black"><td colspan="8"></td></tr>'
                    ]
                plass = idx

            html += [
                u'<tr height="5"></tr>',
                u'<tr>',
                u'<td bgcolor="white" align="center">%d</td>' % plass
            ]
            if entry[7]:
                html += [
                    u'<td bgcolor="white">%s' % entry[5]
                ]
                for jackpot in entry[7].split('\n'):
                    html += [
                        ' <img src="%s" title="%s"/>' % (self.data.get_imageurl(u'img/icon-ball-crop.png'), jackpot)
                    ]
                html += [u'</td>']
            else:
                html += [
                    u'<td bgcolor="white">%s</td>' % entry[5]
                ]
            html += [
                u'<td bgcolor="white" align="center">%d</td>' % entry[1],
                u'<td bgcolor="white" align="center">%d</td>' % entry[2],
                u'<td bgcolor="white" align="center">%d</td>' % entry[3],
                u'<td bgcolor="white" align="center">%d</td>' % entry[4],
                u'<td bgcolor="white" align="center">%d</td>' % entry[0]
            ]
            if entry[1] == 0:
                html += [
                    u'<td bgcolor="white"></td>'
                ]
            else:
                html += [
                    u'<td bgcolor="white" align="center"><img src="%s" title="%s"/></td>' % (self.data.get_imageurl(u'img/icon-stats-crop.png'), u'Fra %d tips:\n%s' % (entry[8] + misses.get(entry[5], 0), entry[6]))
                ]
            html += [
                u'</tr>'
            ]
            idx += 1
            prevscore = entry[0]


        html += [
            u'</table>',
            u'</td></tr>',
            u'</table>'
        ]
        html += [
            u'<table width=480 border="1" cellspacing=0 cellpadding=5 bordercolor="white">',
            u'<tr><td align=right><a title="BBCode 1/2" target="_blank" href="StandingsBBCode.py?idx=%d&mode=series&part=1"><i class="fa fa-code"></i></a> ' % self.__idx,
            u'<a title="BBCode 2/2" target="_blank" href="StandingsBBCode.py?idx=%d&mode=series&part=2"><i class="fa fa-code"></i></a></td></tr>' % self.__idx,
            u'</table>',
            u'<p>'
        ]

        # formtabell

        formlength = 6
        first = max(self.__idx - formlength + 1, 1)

        misses = {}
        score = self.standings.get_score(first, misses)
        matchname = matches[first]['game']
        for i in range(0, len(score)):
            score[i] = (score[i][0],
                        score[i][1],
                        score[i][2],
                        score[i][3],
                        score[i][4],
                        score[i][5],
                        u'%d: %s (%d)' % (self.get_round(first), matchname, score[i][0]),
                        score[i][7],
                        score[i][8])

        if self.__idx > 1:
            for i in range(first+1, self.__idx+1):
                matchname = u'%d: %s' % (self.get_round(i), matches[i]['game'])
                newscore = self.standings.get_score(i, misses)
                score = self.standings.merge_scores(score, newscore, matchname)

        html += [
            u'<table width=480 border="1" cellspacing=0 cellpadding=5 bordercolor="black" background="%s">' % self.data.get_imageurl(u'img/pattern.jpg'),
            u'<tr><td border=0>',
            u'<table width="100%" cellpadding="2" cellspacing=0 border="0">',
            u'<tr><td align="center" colspan="8"><b><font size=+3 color=white>',
            u'Formtabell, runde %d-%d' % (self.get_round(first), self.get_round(self.__idx)),
            u'</font></b></td></tr>'
        ]

        html += self.html_tableheader()

        idx = 1
        plass = 1
        prevscore = 0
        for entry in score:
            if entry[0] != prevscore:
                if plass <= 3 and idx > 3:
                    html += [
                        u'<tr height="5"></tr>',
                        u'<tr height="0" bgcolor="black"><td colspan="8"></td></tr>'
                    ]
                plass = idx

            html += [
                u'<tr height="5"></tr>',
                u'<tr>',
                u'<td bgcolor=white align=center>%d</td>' % plass
            ]
            if entry[7]:
                html += [
                    u'<td bgcolor=white>%s' % entry[5]
                ]
                for jackpot in entry[7].split('\n'):
                    html += [
                        ' <img src="%s" title="%s"/>' % (self.data.get_imageurl(u'img/icon-ball-crop.png'), jackpot)
                    ]
                html += [u'</td>']
            else:
                html += [
                    u'<td bgcolor=white>%s</td>' % entry[5]
                ]
            html += [
                u'<td bgcolor=white align=center>%d</td>' % entry[1],
                u'<td bgcolor=white align=center>%d</td>' % entry[2],
                u'<td bgcolor=white align=center>%d</td>' % entry[3],
                u'<td bgcolor=white align=center>%d</td>' % entry[4],
                u'<td bgcolor=white align=center>%d</td>' % entry[0]
            ]
            if entry[1] == 0:
                html += [
                    u'<td bgcolor=white></td>'
                ]
            else:
                html += [
                    u'<td bgcolor=white align=center><img src="%s" title="%s"/></td>' % (self.data.get_imageurl(u'img/icon-stats-crop.png'), u'Fra %d tips:\n%s' % (entry[8] + misses.get(entry[5], 0), entry[6]))
                ]
            html += [
                u'</tr>'
            ]
            idx += 1
            prevscore = entry[0]


        html += [
            u'</table>',
            u'</td></tr>',
            u'</table>'
        ]
        html += [
            u'<table width=480 border="1" cellspacing=0 cellpadding=5 bordercolor="white">',
            u'<tr><td align=right><a title="BBCode top10" target="_blank" href="StandingsBBCode.py?idx=%d&mode=form"><i class="fa fa-code"></i></a></td></tr>' % self.__idx,
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
    return StandingsView(client)
