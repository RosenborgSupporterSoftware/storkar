# -*- coding: utf-8 -*-
# vim:sw=4

import os
import codecs
import sys
import json
import urllib

from base.http.Response import Response
from rbkweb.Data import Data


class AddMatchResponse(Response):

    def __init__(self, client):
        Response.__init__(self, client)
        self.data = Data()
        self.__matchdata = urllib.unquote(client.arg('data'))
        self.__msg = "%s: main: add match" % self.get_user()


    def html(self):
        if self.get_user() == 'anonym':
            return []

        self.data.load()

        try:
            matchdata = json.loads(self.__matchdata)
        except:
            raise ValueError('Value of __matchdata ("%s") can not be parsed.' % self.__matchdata)

        formvalue = matchdata['match']

        matchname, matchdate = formvalue.split(u' 20', 2)
        matchdate = u'20%s' % matchdate
        hometeam, awayteam = matchname.split(u' - ', 2)

        teams = self.data.get_teams_section()
        if not hometeam in teams:
            sys.stderr.write("error: hometeam (%s) not in teams" % hometeam)
            return []

        if not awayteam in teams:
            sys.stderr.write("error: awayteam (%s) not in teams" % awayteam)
            return []

        matchname = u'%s - %s' % (hometeam, awayteam)

        newmatch = {}
        newmatch['game'] = matchname
        newmatch['date'] = matchdate

        matches = self.data.get_matches_section()

        idx = 1
        inserted = False
        while idx < len(matches):
            match = matches[idx]
            date = match['date']
            if date[:10] > matchdate[:10]:
                matches.insert(idx, newmatch)
                inserted = True
                self.__msg = "%s: main: insert match at index %d" % (self.get_user(), idx)
                break
            idx += 1

        if not inserted:
            self.__msg = "%s: main: expanded list of matches" % self.get_user()
            matches.append(newmatch)

        self.data.save()
        self.data.commit(self.__msg)

        return []


def run(client):
    return AddMatchResponse(client)

