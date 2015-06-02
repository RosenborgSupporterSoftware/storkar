# -*- coding: utf-8 -*-
# vim:sw=4

import os
import re
import json

from AppResponse import AppResponse
from Data import Data
from Standings import Standings


class StandingsView(AppResponse):


    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.dependency(js='jquery2')
        self.dependency(css='fontawesome')
        self.__idx = int(client.arg('idx'))
        self.__mode = client.arg('mode')
        assert self.__mode in ['round', 'series', 'form'], 'invalid mode arg'

        self.__part = 0
        if self.__mode == 'series':
            self.__part = int(client.arg('part'))

        self.data = Data()
        self.standings = Standings(self.data)


    def get_round(self, idx):
        return idx


    def gen_table(self, results, title, separator=False, missing=None, cutoff=1000):
        header = [
            u'<table width="480" border="1" cellspacing="0" cellpadding="5" bordercolor="black" background="%s">' % self.data.get_imageurl('img/pattern.jpg'),
            u'<tr><td border="0">',
            u'<table width="100%" cellpadding="2" cellspacing="0" border="0">',
            u'<tr><td align="center" colspan="8">[b][size=22][color=white]',
            u'%sFILLER' % title,
            u'[/color][/size][/b]</td></tr>',

            u'<tr height="5"></tr>',
            u'<tr height="0" bgcolor="black"><td colspan="8"></td></tr>',
            u'<tr>',
            u'<td bgcolor="white" align="center"><img title="Plassering" src="%s"/></td>' % self.data.get_imageurl("img/icon-trophy.png"),
            u'<td bgcolor="white"><img title="Deltagernavn" src="%s"/> <img title="Jackpot" src="%s"/></td>' % (self.data.get_imageurl("img/icon-player.png"), self.data.get_imageurl("img/icon-ball-crop-high.png")),
            u'<td bgcolor="white" align="center"><img title="Sluttresultat" src="%s"/></td>' % self.data.get_imageurl("img/icon-whistle.png"),
            u'<td bgcolor="white" align="center"><img title="Pauseresultat" src="%s"/></td>' % self.data.get_imageurl("img/icon-clock.png"),
            u'<td bgcolor="white" align="center"><img title="M&aring;lscorere" src="%s"/></td>' % self.data.get_imageurl("img/icon-goal.png"),
            u'<td bgcolor="white" align="center"><img title="Tippetegn HUB" src="%s"/></td>' % self.data.get_imageurl("img/icon-tipping.png"),
            u'<td bgcolor="white" align="center"><img title="Poeng" src="%s"/></td>' % self.data.get_imageurl("img/icon-score.png"),
            u'<td bgcolor="white"></td></tr>',
            u'</tr>',
            u'<tr height="0" bgcolor="black"><td colspan="8"></td></tr>'
        ]

        html = []
        html += [ u'<div align="center">\n' ]
        html += header

        idx = 1
        plass = 1
        prevscore = 0
        block = 0
        for line, score in enumerate(results):

            if score[0] != prevscore:
                if line > 50 and block == 0:
                    block += 1
                    html += [
                        u'</td></tr>',
                        u'</table>',
                        u'</td></tr>',
                        u'</table>\n</div>\n',
                    ]
                    html += [ u'<div align="center">\n' ]
                    html += header
                if separator and plass <= 3 and idx > 3:
                    html += [
                        u'<tr height="5"></tr>',
                        u'<tr height="0" bgcolor="black"><td colspan="8"></td></tr>'
                    ]
                plass = idx

            if plass > cutoff:
                continue

            html += [
                u'<tr height="5"></tr>',
                u'<tr>',
                u'<td bgcolor="white" align="center">[size=12][b]%d[/b][/size]</td>' % plass
            ]

            html += [
                u'<td bgcolor="white">[size=12][b]%s[/b][/size]' % score[5]
            ]
            for jackpot in score[7].split('\n'):
                if not jackpot: continue
                if jackpot == u'': continue
                if not separator: jackpot = u'Jackpot!'
                html += [
                    u' <img title="%s" src="%s"/>' % (jackpot, self.data.get_imageurl("img/icon-ball-crop.png"))
                ]
            html += [
                u'</td>'
            ]

            html += [
                u'<td bgcolor="white" align="center">[size=12][b]%d[/b][/size]</td>' % score[1],
                u'<td bgcolor="white" align="center">[size=12][b]%d[/b][/size]</td>' % score[2],
                u'<td bgcolor="white" align="center">[size=12][b]%d[/b][/size]</td>' % score[3],
                u'<td bgcolor="white" align="center">[size=12][b]%d[/b][/size]</td>' % score[4],
                u'<td bgcolor="white" align="center">[size=12][b]%d[/b][/size]</td>' % score[0]
            ]
            if score[1] > 0:
                html += [
                    u'<td bgcolor="white" align="center"><img src="%s" title="%s"/></td>' % (self.data.get_imageurl("img/icon-stats-crop.png"), score[6].replace('\n', ' || ')),
                ]
            else:
                html += [
                    u'<td bgcolor="white"></td>'
                ]
            html += [
                u'</tr>'
            ]
            idx += 1
            prevscore = score[0]

        html += [
            u'</table>',
            u'</td></tr>',
            u'</table>',
            u'\n</div>'
        ]

        contents = ''.join(html)
        contents = contents.replace(r'<', u'&lt;')
        contents = contents.replace(r'>', u'&gt;')

        return contents


    def html(self):
        self.data.load()

        matches = self.data.get_matches_section()
        match = matches[self.__idx]
        missing = {}

        if self.__mode == 'round':
            separator = False
            results = self.standings.get_score(self.__idx, missing)
            title = u'Runde %d:\n%s' % (self.get_round(self.__idx), match['game'])

        elif self.__mode == 'series':
            separator = True
            title = u'Tabell, runde %d' % (self.get_round(self.__idx))
            results = self.standings.get_score(1, missing)
            matchname = matches[1]['game']
            for i in range(0, len(results)):
                results[i] = (results[i][0],
                              results[i][1],
                              results[i][2],
                              results[i][3],
                              results[i][4],
                              results[i][5],
                              u'%d: %s (%d)' % (self.get_round(1), matchname, results[i][0]),
                              results[i][7],
                              results[i][8])

            if self.__idx > 1:
                for i in range(2, self.__idx+1):
                    matchname = u'%d: %s' % (self.get_round(i), matches[i]['game'])
                    newscore = self.standings.get_score(i, missing)
                    results = self.standings.merge_scores(results, newscore, matchname)

            for i in range(0, len(results)):
                results[i] = (results[i][0],
                              results[i][1],
                              results[i][2],
                              results[i][3],
                              results[i][4],
                              results[i][5],
                              u'Fra %d tips:\n%s' % (results[i][8] + missing.get(results[i][5], 0), results[i][6]),
                              results[i][7],
                              results[i][8])

        elif self.__mode == 'form':
            kamper = 6
            separator = True
            first = max(self.__idx - kamper + 1, 1)
            title = u'Formtabell, runde %d-%d' % (self.get_round(first), self.get_round(self.__idx))
            results = self.standings.get_score(first, missing)
            matchname = matches[first]['game']
            for i in range(0, len(results)):
                results[i] = (results[i][0],
                              results[i][1],
                              results[i][2],
                              results[i][3],
                              results[i][4],
                              results[i][5],
                              u'%d: %s (%d)' % (self.get_round(1), matchname, results[i][0]),
                              results[i][7],
                              results[i][8])

            if self.__idx > 1:
                for i in range(first+1, self.__idx+1):
                    matchname = u'%d: %s' % (self.get_round(i), matches[i]['game'])
                    newscore = self.standings.get_score(i, missing)
                    results = self.standings.merge_scores(results, newscore, matchname)
            for i in range(0, len(results)):
                results[i] = (results[i][0],
                              results[i][1],
                              results[i][2],
                              results[i][3],
                              results[i][4],
                              results[i][5],
                              u'Fra %d tips:\n%s' % (results[i][8] + missing.get(results[i][5], 0), results[i][6]),
                              results[i][7],
                              results[i][8])

        cutoff = 1000
        if self.__mode == 'form': cutoff = 10

        contents = self.gen_table(results, title, separator, missing, cutoff)

        if self.__mode == 'round':
            contents = contents.replace('FILLER', '')
        elif self.__mode == 'series':
            parts = contents.split(u'&lt;/div&gt;')
            for idx, part in enumerate(parts):
                parts[idx] = part.replace('FILLER', ', %d/2' % (idx+1))
            if self.__part > 0:
                contents = parts[self.__part-1] + u'&lt;/div&gt;'
            else:
                contents = u'&lt;/div&gt;'.join(parts)

        elif self.__mode == 'form':
            contents = contents.replace('FILLER', ', topp 10')

        body = []
        body += self.html_heading()
        body += self.html_body_open()
        body += [u'<pre>']

        body += [contents]

        body += [u'</pre>']
        body += self.html_body_close()
        return body


def run(client):
    return StandingsView(client)



if __name__ == "__main__":
    class FakeClient:
        def __init__(self):
            self.args = { 'idx': 47, # RBK-VIF
              'mode': 'form',
              'part': 0 }

        def arg(self, key):
            return self.args[key]

        def get_user(self):
            return 'larsa'

    generator = run(FakeClient())
    print '\n'.join(generator.html()).encode('utf-8', 'ignore')

