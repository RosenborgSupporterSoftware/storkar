# -*- coding: utf-8 -*-

import os
import json
import urllib

from AppResponse import AppResponse
from Data import Data


class TeamFormationBBCode(AppResponse):


    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.__data = None
        self.__teamdata = client.arg('team')
        self.__team = None
        if self.__teamdata:
            self.__team = self.__teamdata


    def load_data(self):
        os.system('cd rbkweb/data && git pull')
        f = open("rbkweb/data/data.json", "r")
        self.__data = Data.upgrade_data(json.load(f))
        f.close()


    def html(self):
        self.load_data()

        fs = 8 # fontsize, small text

        bbcode = []
        if self.__team:
            playerdata = self.__data['players']

            bbcode += [
                u'<div align="center">\n',
                u'<table width="300" cellspacing="0" cellpadding="0" border="0">',
                u'<tr>',
                u'<td width="13%"></td>',
                u'<td width="12%"></td>',
                u'<td width="12%"></td>',
                u'<td width="13%"></td>',
                u'<td width="13%"></td>',
                u'<td width="12%"></td>',
                u'<td width="12%"></td>',
                u'<td width="13%"></td>',
                u'</tr>'
            ]

            rows = []
            images = []
            playernames = []
            playershortnames = []

            for line in self.__team.split(u'\n'):
                players = filter(lambda x: x != u'', line.split(u' '))
                if len(players) and not players[0]: players = []
                rows += [players]

                imgs = []
                names = []
                shortnames = []
                for player in players:
                    img = playerdata['default']['image']
                    playerid = Data.player_id(self.__data, player)
                    if playerid in playerdata:
                        if 'image' in playerdata[playerid]:
                            img = Data.get_imgurl(self.__data, playerdata[playerid]['image'])
                    imgs += [ img ]
                    names += [ Data.player_name(self.__data, playerid) ]
                    shortnames += [ Data.player_shortname(self.__data, playerid) ]
                assert len(imgs) == len(players), "invalid len() test"
                images += [imgs]
                playernames += [names]
                playershortnames += [shortnames]

            skip = 0
            for i, row in enumerate(rows):
                if skip > 0:
                    skip -= 1
                else:
                    players = row
                    imgs = images[i]
                    names = playernames[i]
                    shortnames = playershortnames[i]
                    if (i+1) < len(rows):
                        nextplayers = rows[i+1]
                        nextimgs = images[i+1]
                        nextnames = playernames[i+1]
                        nextshortnames = playershortnames[i+1]
                        if (i+2) < len(rows):
                            frontplayers = rows[i+2]
                            frontimgs = images[i+2]
                            frontnames = playernames[i+2]
                            frontshortnames = playershortnames[i+2]

                    if len(players) == 0:
                        bbcode += [
                            u'<tr height="10"></tr>'
                        ]
                    elif len(players) == 1:
                        if (i+2) < len(rows) and len(rows[i+1]) == 2 and len(rows[i+2]) == 1:
                            # diamant
                            bbcode += [
                                u'<tr>',
                                u'<td colspan="3" rowspan="2" align="center" valign="middle"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (nextimgs[0], nextnames[0], nextshortnames[0]),
                                u'<td colspan="2" align="center" valign="top"><img src="%s" title="%s"/>[size=8]\n%s\n[/size]</td>' % (imgs[0], names[0], shortnames[0]),
                                u'<td colspan="3" rowspan="2" align="center" valign="middle"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (nextimgs[1], nextnames[1], nextshortnames[1]),
                                u'</tr>',
                                u'<tr>',
                                u'<td colspan="2" align="center" valign="top"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (frontimgs[0], frontnames[0], frontshortnames[0]),
                                u'</tr>'
                            ]

                            skip = 2

                        elif (i+1) < len(rows) and len(rows[i+1]) == 2:
                            # compact
                            bbcode += [
                                u'<tr>',
                                u'<td colspan="3" align="center" valign="bottom">\n<img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (nextimgs[0], nextnames[0], nextshortnames[0]),
                                u'<td colspan="2" align="center" valign="top"><img src="%s" title="%s"/>[size=8]\n%s[/size]\n</td>' % (imgs[0], names[0], shortnames[0]),
                                u'<td colspan="3" align="center" valign="bottom">\n<img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (nextimgs[1], nextnames[1], nextshortnames[1]),
                                u'</tr>'
                            ]
                            skip = 1
                        else:
                            bbcode += [
                                u'<tr><td colspan="8" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td></tr>' % (imgs[0], names[0], shortnames[0])
                            ]
                    elif len(players) == 2:
                        if (i+1) < len(rows) and len(rows[i+1]) == 1:
                            # compact
                            bbcode += [
                                u'<tr>',
                                u'<td colspan="3" align="center" valign="top"><img src="%s" title="%s"/>[size=8]\n%s[/size]\n</td>' % (imgs[0], names[0], shortnames[0]),
                                u'<td colspan="2" align="center" valign="bottom">\n<img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (nextimgs[0], nextnames[0], nextshortnames[0]),
                                u'<td colspan="3" align="center" valign="top"><img src="%s" title="%s"/>[size=8]\n%s[/size]\n</td>' % (imgs[1], names[1], shortnames[1]),
                                u'</tr>'
                            ]
                            skip = 1
                        else:
                            bbcode += [
                                u'<tr>',
                                u'<td colspan="4" align="center"><img src="%s" title="%s"/>\n[size=8]%s[/size]</td>' % (imgs[0], names[0], shortnames[0]),
                                u'<td colspan="4" align="center"><img src="%s" title="%s"/>\n[size=8]%s[/size]</td>' % (imgs[1], names[1], shortnames[1]),
                                u'</tr>'
                            ]
                    elif len(players) == 3:
                        bbcode += [
                            u'<tr>',
                            u'<td colspan="3" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[0], names[0], shortnames[0]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[1], names[1], shortnames[1]),
                            u'<td colspan="3" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[2], names[2], shortnames[2]),
                            u'</tr>'
                        ]
                    elif len(players) == 4:
                        bbcode += [
                            u'<tr>',
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[0], names[0], shortnames[0]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[1], names[1], shortnames[1]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[2], names[2], shortnames[2]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[3], names[3], shortnames[3]),
                            u'</tr>'
                        ]
                    elif len(players) == 5:
                        bbcode += [
                            u'<tr>',
                            u'<td colspan="2" align="center">\n<img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[0], names[0], shortnames[0]),
                            u'<td colspan="1" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[1], names[1], shortnames[1]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[2], names[2], shortnames[2]),
                            u'<td colspan="1" align="center"><img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[3], names[3], shortnames[3]),
                            u'<td colspan="2" align="center">\n<img src="%s" title="%s"/>[size=8]\n%s[/size]</td>' % (imgs[4], names[4], shortnames[4]),
                            u'</tr>'
                        ]
                    else:
                        bbcode += [
                            u'<tr height="10"></tr>'
                        ]

            bbcode += [
                u'</table>\n',
                u'</div>',
            ]

        content = ''.join(bbcode)
        content = content.replace(u'<', u'&lt;').replace(u'>', u'&gt;')

        html = []
        html += self.html_heading(u'Lagoppstilling BBCode')
        html += self.html_body_open()
        html += [
            u'<pre>',
            content,
            u'</pre>'
        ]
        html += self.html_body_close()
        return html


def run(client):
    return TeamFormationBBCode(client)

