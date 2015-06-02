# -*- coding: utf-8 -*-
# vim:sw=4

import os
import re
import codecs
import json
import urllib

from base.http.Response import Response
from rbkweb.Data import Data
from rbkweb.Settings import ONLINE

# TODO:
# - add multiple bets at a time... (mobile usage)
# - feedback through json response if adding fails, and which rows to highlight
# - convert to using only a Data() instance, not a __data dict directly

class AddBetResponse(Response):

    def __init__(self, client):
        Response.__init__(self, client)
        self.__idx = int(client.arg('idx'))
        self.__betdata = client.arg('data')
        self.__msg = "match %d: add bet" % self.__idx
        self.data = Data()


    def load_data(self):
        if ONLINE:
            os.system('cd rbkweb/data && git pull')
        f = codecs.open("rbkweb/data/data.json", "r", "utf-8")
        self.__data = Data.upgrade_data(json.load(f))
        f.close()
        self.data.load()


    def save_data(self):
        f = codecs.open("rbkweb/data/data.json", "w", "utf-8")
        f.write(json.dumps(self.__data, indent=4, sort_keys=True, ensure_ascii=False))
        f.close()


    def commit_data(self):
        error = os.system('cd rbkweb/data && git commit -m "%s" data.json' % self.__msg.encode('ascii', errors='replace'))
        if error == 0 and ONLINE:
            error = os.system('cd rbkweb/data && git push')
        return error == 0


    def get_goalees(self, text):
        goalees = []
        if text[-1].isnumeric() and text[-2] == '*':
            goalee = text[:-2]
            count = int(text[-1])
            for i in range(0,count):
                 goalees += [ goalee ]
        else:
            goalees += [ text ]
        return goalees


    def html(self):
        if self.get_user() == 'anonym':
            return []

        self.load_data()

        try:
            betdata = json.loads(self.__betdata)
        except:
            raise ValueError('Value of __betdata ("%s") can not be parsed.' % self.__betdata)

        bets = []
        if 'bet' in betdata:
            formvalue = betdata['bet']
            bets += [formvalue]
        elif 'multibet' in betdata:
            bets += betdata['multibet'].split('\n')

        for formvalue in bets:
            if re.match('^ *$', formvalue):
                continue
            separator = u' '
            separatorcount = formvalue.count(separator)
            for sep in [u'|', u',', u'%', u'#']:
                count = formvalue.count(sep)
                if count > separatorcount:
                    separator = sep
                    separatorcount = count

            formvalue = formvalue.replace(u'%s%s' % (separator, separator), separator)
            betinfo = formvalue.split(separator)

            match = self.__data['matches'][self.__idx]
            bet = {}
            bet['user'] = betinfo[0]
            while len(betinfo) > 1 and not betinfo[1][0].isnumeric():
                betinfo = betinfo[1:]
                bet['user'] = '%s%s%s' % (bet['user'], separator, betinfo[0])

            if bet['user'].endswith('*'):
                bet['user'] = self.data.find_user_from_prefix(bet['user'][:-1])
                if not bet['user']:
                    return False

            bet['result'] = betinfo[1]
            bet['goals'] = []

            if len(betinfo) > 2 and betinfo[2] != u'-':
                if betinfo[2][0].isnumeric():
                    # this will trigger for no halftime but numeric goalee
                    bet['halftime'] = betinfo[2]
                else:
                    bet['goals'] += self.get_goalees(betinfo[2])

            for key in ['result', 'halftime']:
                if key in bet and len(bet[key]) == 2:
                    bet[key] = '%s-%s' % (bet[key][0], bet[key][1])

            if bet['result'] == '0-0':
                bet['halftime'] = '0-0'

            if len(betinfo) > 3:
                for goal in betinfo[3:]:
                    bet['goals'] += self.get_goalees(goal)

            if not 'bets' in match:
                match['bets'] = [ bet ]
            else:
                inserted = False
                for i in range(0, len(match['bets'])):
                    if bet['user'] == match['bets'][i]['user']:
                        match['bets'][i] = bet
                        self.__msg = "match %d: update bet for '%s'" % (self.__idx, bet['user'])
                        inserted = True
                        break
                if not inserted:
                    self.__msg = "match %d: add bet for '%s'" % (self.__idx, bet['user'])
                    match['bets'].append(bet)

        self.save_data()
        self.commit_data()

        return [u'<html></html>']


def run(client):
    return AddBetResponse(client)

