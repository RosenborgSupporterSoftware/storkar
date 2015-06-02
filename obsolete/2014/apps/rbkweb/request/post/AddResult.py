# -*- coding: utf-8 -*-
# vim:sw=4

import json

from base.http.Response import Response
from rbkweb.Data import Data


class AddResultResponse(Response):

    def __init__(self, client):
        Response.__init__(self, client)
        self.data = Data()
        self.__idx = int(client.arg('idx'))
        self.__betdata = client.arg('data')
        self.__msg = "%s: match %d: set result" % (self.get_user(), self.__idx)


    def html(self):
        if self.get_user() == 'anonym':
            return []

        self.data.load()

        try:
            betdata = json.loads(self.__betdata)
        except:
            raise ValueError('Value of __betdata ("%s") can not be parsed.' % self.__betdata)

        formvalue = betdata['result']
        if formvalue.count('|') > formvalue.count(','):
            betinfo = formvalue.split('|')
        else:
            betinfo = formvalue.split(',')

        matches = self.data.get_matches_section()
        match = matches[self.__idx]

        fulltime = betinfo[0]
        halftime = betinfo[1]
        goals = betinfo[2:]

        for idx, goalee in enumerate(goals):
            goals[idx] = self.data.get_playerid(goalee)

        match['result'] = fulltime
        match['halftime'] = halftime
        match['goals'] = goals

        self.data.save()
        self.data.commit(self.__msg)

        return [u'<html></html>']


def run(client):
    return AddResultResponse(client)

