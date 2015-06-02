#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import urllib

from AppResponse import AppResponse
from base.http.ClientInfo import ClientInfo
from Data import Data


class TeamFormationHTML(AppResponse):


    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.__data = None
        self.__teamdata = client.arg('team')
        self.__team = None
        if self.__teamdata:
            self.__team = self.__teamdata


    def load_data(self):
        os.system('cd rbkweb/data && git pull')
        f = open('rbkweb/data/data.json', 'r')
        self.__data = Data.upgrade_data(json.load(f))
        f.close()


    def html(self):
        self.load_data()

        html = []
        html += self.html_heading(u"Lagoppstilling")
        html += self.html_body_open()

        if self.__team:
            playerdata = self.__data['players']

            html += [
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
                        html += [
                            u'<tr><td colspan="8">&nbsp;</td></tr>'
                        ]
                    elif len(players) == 1:
                        if (i+2) < len(rows) and len(rows[i+1]) == 2 and len(rows[i+2]) == 1:
                            # diamant
                            html += [
                                u'<tr>',
                                u'<td colspan="3" rowspan="2" align="center" valign="middle"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (nextimgs[0], nextnames[0], nextshortnames[0]),
                                u'<td colspan="2" align="center" valign="top"><img src="%s" title="%s"/><font size="-4"><br/>%s<br/></font></td>' % (imgs[0], names[0], shortnames[0]),
                                u'<td colspan="3" rowspan="2" align="center" valign="middle"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (nextimgs[1], nextnames[1], nextshortnames[1]),
                                u'</tr>',
                                u'<tr>',
                                u'<td colspan="2" align="center" valign="top"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (frontimgs[0], frontnames[0], frontshortnames[0]),
                                u'</tr>']

                            skip = 2

                        elif (i+1) < len(rows) and len(rows[i+1]) == 2:
                            # compact
                            html += [
                                u'<tr>',
                                u'<td colspan="3" align="center" valign="bottom"><br/><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (nextimgs[0], nextnames[0], nextshortnames[0]),
                                u'<td colspan="2" align="center" valign="top"><img src="%s" title="%s"/><font size="-4"><br/>%s</font><br/></td>' % (imgs[0], names[0], shortnames[0]),
                                u'<td colspan="3" align="center" valign="bottom"><br/><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (nextimgs[1], nextnames[1], nextshortnames[1]),
                                u'</tr>'
                            ]
                            skip = 1
                        else:
                            html += [
                                u'<tr><td colspan="8" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td></tr>' % (imgs[0], names[0], shortnames[0])
                            ]
                    elif len(players) == 2:
                        if (i+1) < len(rows) and len(rows[i+1]) == 1:
                            # compact
                            html += [
                                u'<tr>',
                                u'<td colspan="3" align="center" valign="top"><img src="%s" title="%s"/><font size="-4"><br/>%s</font><br/></td>' % (imgs[0], names[0], shortnames[0]),
                                u'<td colspan="2" align="center" valign="bottom"><br/><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (nextimgs[0], nextnames[0], nextshortnames[0]),
                                u'<td colspan="3" align="center" valign="top"><img src="%s" title="%s"/><font size="-4"><br/>%s</font><br/></td>' % (imgs[1], names[1], shortnames[1]),
                                u'</tr>'
                            ]
                            skip = 1
                        else:
                            html += [
                                u'<tr>',
                                u'<td colspan="4" align="center"><img src="%s" title="%s"/><br/><font size="-4">%s</font></td>' % (imgs[0], names[0], shortnames[0]),
                                u'<td colspan="4" align="center"><img src="%s" title="%s"/><br/><font size="-4">%s</font></td>' % (imgs[1], names[1], shortnames[1]),
                                u'</tr>'
                            ]
                    elif len(players) == 3:
                        html += [
                            u'<tr>',
                            u'<td colspan="3" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[0], names[0], shortnames[0]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[1], names[1], shortnames[1]),
                            u'<td colspan="3" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[2], names[2], shortnames[2]),
                            u'</tr>'
                        ]
                    elif len(players) == 4:
                        html += [
                            u'<tr>',
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[0], names[0], shortnames[0]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[1], names[1], shortnames[1]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[2], names[2], shortnames[2]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[3], names[3], shortnames[3]),
                            u'</tr>'
                        ]
                    elif len(players) == 5:
                        html += [
                            u'<tr>',
                            u'<td colspan="2" align="center"><br/><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[0], names[0], shortnames[0]),
                            u'<td colspan="1" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[1], names[1], shortnames[1]),
                            u'<td colspan="2" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[2], names[2], shortnames[2]),
                            u'<td colspan="1" align="center"><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[3], names[3], shortnames[3]),
                            u'<td colspan="2" align="center"><br/><img src="%s" title="%s"/><font size="-4"><br/>%s</font></td>' % (imgs[4], names[4], shortnames[4]),
                            u'</tr>'
                        ]
                    else:
                        html += [
                            u'<tr><td colspan="8">&nbsp;</td></tr>'
                        ]


            html += [
                u'<tr><td colspan="8" align="right">',
                u'<a title="BBCode" target="_blank" href="TeamFormationBBCode.py?team=%s">' % urllib.quote(self.__teamdata.encode('utf-8')),
                u'<i class="fa fa-code"></i>',
                u'</a>',
                u'</td></tr>',
                u'</table>'
            ]

        html += self.html_body_close()

        return html


def run(client):
    return TeamFormationHTML(client)


if __name__ == "__main__":
    environ = dict(os.environ)
    clientinfo = ClientInfo(environ)
    app = run(clientinfo)
    content = u'\n'.join(app.html())
    string = content.encode('utf-8', errors='ignore')
    print string
    print u'\n'

