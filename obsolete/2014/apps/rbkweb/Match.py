# -*- coding: utf-8 -*-
# vim:sw=4

from rbkweb.Data import Data


class Match(object):


    def __init__(self, data, dataobj):
        self.__data = data
        self.data = dataobj


    def is_home_game(self):
        return self.__data['game'].find("RBK") == 0


    def get_score_matrix(self, key="result"):
        matrix = {}
        for user in self.__data.get('bets', []):
            assert not 'legacy' in user, "not supported"
            if key in user:
                score = user[key]
                matrix[score] = matrix.get(score, 0) + 1
        return matrix


    def get_bet_count(self):
        return len(self.__data.get('bets', []))


    def get_hit_count(self):
        if not 'result' in self.__data:
            return 0
        if not 'bets' in self.__data:
            return 0
        count = 0
        result = self.__data['result']
        for bet in self.__data['bets']:
            if bet['result'] == result:
                count += 1
        return count


    def get_stats(self):
        homegame = self.is_home_game()

        goals_for = 0
        goals_against = 0
        goals_for_2 = 0
        goals_against_2 = 0
        pause_bets = 0

        for user in self.__data.get('bets', []):
            assert not 'legacy' in user, "not supported"
            result = user['result']
            homegoals, awaygoals = result.split('-',2)
            if not homegame:
                homegoals, awaygoals = awaygoals, homegoals
            goals_for += int(homegoals)
            goals_against += int(awaygoals)

            if 'halftime' in user and len(user['halftime']) >= 3:
                pause = user['halftime']
                assert pause.find('-') != -1, "invalid pause score '%s'" % pause
                homegoals, awaygoals = pause.split('-',2)
                if not homegame:
                    homegoals, awaygoals = awaygoals, homegoals
                goals_for_2 += int(homegoals)
                goals_against_2 += int(awaygoals)
                pause_bets += 1

        stats = {}
        stats['bets'] = len(self.__data.get('bets', []))
        stats['goals_for'] = goals_for
        stats['goals_against'] = goals_against

        stats['pause_bets'] = pause_bets
        stats['pause_goals_for'] = goals_for_2
        stats['pause_goals_against'] = goals_against_2

        if stats['bets'] > 0:
            score_for = float(goals_for) / float(stats['bets'])
            score_against = float(goals_against) / float(stats['bets'])
            pause_score_for = float(goals_for_2) / float(pause_bets)
            pause_score_against = float(goals_against_2) / float(pause_bets)

            if not homegame:
                score_for, score_against = score_against, score_for
                pause_score_for, pause_score_against = pause_score_against, pause_score_for

            stats['result'] = u"%.0f-%.0f" % (score_for, score_against)
            stats['result_accurate'] = u"%.2f-%.2f" % (score_for, score_against)
            stats['halftime'] = u"%.0f-%.0f" % (pause_score_for, pause_score_against)
            stats['halftime_accurate'] = u"%.2f-%.2f" % (pause_score_for, pause_score_against)

        return stats


    def get_goalees(self):
        stats = self.get_stats()
        if stats['bets'] == 0: return []

        goaleesdict = {}

        for user in self.__data['bets']:
            assert not 'legacy' in user, "not supported - not upgraded"
            if 'goals' in user:
                for goalee in user['goals']:
                    key = self.data.get_playerid(goalee)
                    goaleesdict[key] = goaleesdict.get(key, 0) + 1

        stats = self.get_stats()
        goalcount = stats['goals_for']
        score = float(goalcount) / float(stats['bets'])

        goalees = []
        for goalee in goaleesdict:
            confidence = (float(goaleesdict[goalee]) / float(goalcount)) * 100.0 * score
            goalees += [(goaleesdict[goalee], confidence, goalee)]

        return sorted(goalees, reverse=True)

