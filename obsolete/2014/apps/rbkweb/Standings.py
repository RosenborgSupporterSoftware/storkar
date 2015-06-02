# -*- coding: utf-8 -*-

import os
import json

from Data import Data


class Standings:
    def __init__(self, data):
        self.data = data


    def get_round(self, idx):
        return idx


    def get_score(self, matchidx, misses):
        matches = self.data.get_matches_section()
        players = self.data.get_players_section()
        match = matches[matchidx]

        result = match['result']
        halftime = match['halftime']
        goalees = match['goals']

        score = []
        for bet in match['bets']:
            p, r, h, g, j, t = 0, 0, 0, 0, 0, 0

            string = ''
            jackpot = ''

            if bet['result'] == result:
                p, r = 3, 1

                string = bet['result']

                if 'halftime' in bet and bet['halftime'] != '-':
                    string += u' (%s)' % bet['halftime']
                    if bet['halftime'] == halftime:
                        h = 1
                        p += 1

                if 'goals' in bet and len(bet['goals']):
                    for idx, player in enumerate(bet['goals']):
                        player = self.data.get_playerid(player)
                        bet['goals'][idx] = player
                        string += u'\n%s' % players[player]['name']
                    gbets = list(bet['goals']) # modifyable copy
                    for goalee in goalees:
                        playerid = self.data.get_playerid(goalee)
                        if playerid in gbets:
                            g += 1
                            p += 1
                            gbets.remove(playerid)
                if r and h and g == len(match['goals']): # jackpot
                    jackpot = u'%d: %s' % (self.get_round(matchidx), match['game'])

            else:

                if matchidx > 0: # tippetegn-rule introduced for round 1
                    rh, ra = result.split('-')
                    uh, ua = bet['result'].split('-')
                    if int(rh) > int(ra) and int(uh) > int(ua):
                        p, t = 1, 1
                    elif int(rh) == int(ra) and int(uh) == int(ua):
                        p, t = 1, 1
                    elif int(rh) < int(ra) and int(uh) < int(ua):
                        p, t = 1, 1
                    else:
                        user = bet['user']
                        misses[user] = misses.get(user, 0) + 1
                else:
                    user = bet['user']
                    misses[user] = misses.get(user, 0) + 1

            if p > 0:
                score += [(p, r, h, g, t, bet['user'], string, jackpot, 1)]

        score.sort(reverse=True)
        return score


    def merge_scores(self, score, score2, game2):
        merged = list(score)
        addition = list(score2)

        for i in range(0, len(addition)):
            user = addition[i][5]
            found = False
            for j in range(0, len(merged)):
                if user == merged[j][5]:
                    # merge
                    jackpots = ''
                    if merged[j][7] and addition[i][7]:
                        jackpots = u'\n'.join([merged[j][7], addition[i][7]])
                    elif merged[j][7]:
                        jackpots = merged[j][7]
                    elif addition[i][7]:
                        jackpots = addition[i][7]

                    merged[j] = (merged[j][0] + addition[i][0],
                                 merged[j][1] + addition[i][1],
                                 merged[j][2] + addition[i][2],
                                 merged[j][3] + addition[i][3],
                                 merged[j][4] + addition[i][4],
                                 user,
                                 u'%s\n%s (%d)' % (merged[j][6], game2, addition[i][0]),
                                 jackpots,
                                 merged[j][8] + addition[i][8]) # participation
                    found = True
                    break
            if not found:
                merged += [(addition[i][0],
                            addition[i][1],
                            addition[i][2],
                            addition[i][3],
                            addition[i][4],
                            user,
                            u'%s (%d)' % (game2, addition[i][0]),
                            addition[i][7],
                            addition[i][8])]

        #FIXME: sort on points, jackpots, results, halftimes, goalees
        merged.sort(reverse=True)
        return merged

