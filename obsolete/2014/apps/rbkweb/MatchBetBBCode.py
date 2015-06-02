# -*- coding: utf-8 -*-
# vim:sw=4

import os
import re
import json

from AppResponse import AppResponse
from Data import Data


class MatchBetBBCode(AppResponse):


    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.dependency(js='jquery')
        self.dependency(css='fontawesome')
        self.__idx = int(client.arg('idx'))
        self.data = Data()


    def get_bets(self, idx):
        bets = []
        match = self.data.get_matches_section()[idx]
        homegame = match['game'].startswith('RBK')
        for bet in match['bets']:
            user = bet['user']
            hg, ag = bet['result'].split('-')
            if not homegame: hg, ag = ag, hg
            hg = int(hg)
            ag = int(ag)
            advantage = hg - ag
            rbkgoals = hg
            if advantage < 0: rbkgoals = -rbkgoals
            result = bet['result']
            halftime = bet['halftime'] if 'halftime' in bet else ''
            goalees = len(bet['goals']) if 'goals' in bet else 0
            goals = ','.join(bet['goals']) if 'goals' in bet else ''
            bets += [(advantage, rbkgoals, goalees, user, result, halftime, goals)]
        return sorted(bets, reverse=True)


    def generate_table(self, bets):
        players = self.data.get_players_section()
        html = []
        html += [
            u'<div align="center">\n\n\n',
            u'<table width="480" cellpadding="1" cellspacing="0" border="0" bordercolor="black">',
            u'']
        for idx, bet in enumerate(bets):
            if idx > 0:
                html += [u'<tr height="1" bgcolor="black"><td colspan="5"></td></tr>']
            html += [
                u'<tr height="34">',
                u'<td align="center">[size=12]%d[/size]&nbsp;</td>' % (idx + 1),
                u'<td>&nbsp;[size=12]%s[/size]</td>' % bet[3],
                u'<td align="center">[size=12]%s[/size]</td>' % bet[4],
                u'<td align="center">[size=12]%s[/size]</td>' % bet[5],
                u'<td>&nbsp;']

            for goal in bet[6].split(','):
                if goal == '': continue
                goal = self.data.get_playerid(goal)
                name = goal
                image = players['default']['image']
                if goal in players:
                    name = players[goal]['name']
                    if 'image' in players[goal]:
                        image = players[goal]['image']
                image = self.data.get_imageurl(image)
                html += [
                    u'<img title="%s" src="%s"/> ' % (name, image)]

            html += [
                u'</td></tr>']
        html += [
            u'</table>\n',
            u'</div>']


        contents = ''.join(html)
        contents = contents.replace("<", "&lt;").replace(">", "&gt;")
        return contents


    def html(self):
        self.data.load()

        matches = self.data.get_matches_section()
        match = matches[self.__idx]

        bets = self.get_bets(self.__idx)
        contents = self.generate_table(bets)

        body = []
        body += self.html_heading()
        body += self.html_body_open()
        body += [u'<pre>']

        body += [contents]

        body += [u'</pre>']
        body += self.html_body_close()
        return body


def run(client):
    return MatchBetBBCode(client)


if __name__ == "__main__":
    class FakeClient:
        def __init__(self):
            self.args = { 'idx': 47 } # RBK-VIF

        def arg(self, key):
            return self.args[key]

        def get_user(self):
            return 'larsa'

    generator = run(FakeClient())
    print '\n'.join(generator.html()).encode('utf-8', 'ignore')

