# -*- coding: utf-8 -*-
# vim:sw=4

import sys

from base.http.Response import Response
from rbkweb.Data import Data


class DeleteBetResponse(Response):

    def __init__(self, client):
        Response.__init__(self, client)
        self.data = Data()
        self.__idx = int(client.arg('idx'))
        self.__row = int(client.arg('row'))
        self.__user = client.arg('user')
        self.__msg = '%s: match %d: delete bet for \'%s\'' % (self.get_user(), self.__idx, self.__user)


    def html(self):
        if self.get_user() == 'anonym':
            return []

        self.data.load()

        match = self.data.get_matches_section()[self.__idx]

        if 'bets' in match and self.__row <= len(match['bets']):
            bet = match['bets'][self.__row-1]
            if self.__user == bet['user']:
                match['bets'].pop(self.__row-1)
                self.data.save()
                self.data.commit(self.__msg)
            else:
                sys.stderr.write('could not delete "%s" - found "%s" instead.' % (self.__user, bet['user']))

        return []


def run(client):
    return DeleteBetResponse(client)

