# -*- coding: utf-8 -*-

import os
import codecs
import json

from rbkweb.Settings import ONLINE


class Data(object):

    def __init__(self):
        self.__data = None
        pass


    def load(self):
        if ONLINE:
            os.system('cd rbkweb/data && git pull')
        f = codecs.open('rbkweb/data/data.json', 'r', 'utf-8')
        self.__data = Data.upgrade_data(json.load(f))
        f.close()


    def save(self):
        f = codecs.open('rbkweb/data/data.json', 'w', 'utf-8')
        f.write(json.dumps(self.__data, indent=4, sort_keys=True,
                           ensure_ascii=False))
        f.close()


    def commit(self, message):
        commands = [
            'cd rbkweb/data',
            'git commit -m "%s" data.json' % message
        ]
        if ONLINE:
            commands += [
                'git push'
            ]
        error = os.system(' && '.join(commands))
        return error == 0


    def get_players_section(self):
        return self.__data['players']


    def get_logos_section(self):
        return self.__data['logos']


    def get_images_section(self):
        return self.__data['images']


    def get_matches_section(self):
        return self.__data['matches']


    def get_teams_section(self):
        return self.__data['teams']


    def get_imageurl(self, key):
        images = self.get_images_section()
        return images.get(key, key)


    def get_playerid(self, alias):
        players = self.get_players_section()
        if not alias.lower() in map(lambda x:x.lower(), players.keys()):
            for player in players:
                if 'aliases' in players[player] and \
                    alias.lower() in map(lambda x:x.lower(), players[player]['aliases']):
                    return player
        else:
            if not alias in players:
                for player in players:
                    if alias.lower() == player.lower(): return player

        return alias


    def get_bets_for_user(self, user, gameidx):
        bets = []
        for idx in range(1, gameidx):
            match = self.get_matches_section()[idx]
            for bet in match['bets']:
                if bet['user'] == user:
                    bets += [bet]
        return bets


    def find_user_from_prefix(self, prefix):
        matches = len(self.get_matches_section())
        for idx in range(1, matches):
            match = self.get_matches_section()[idx]
            for bet in match['bets']:
                if bet['user'].startswith(prefix):
                    return bet['user']
        return None














    @staticmethod
    def player_id(data, alias):
        players = data['players']
        if not alias.lower() in map(lambda x:x.lower(), players.keys()):
            for player in players:
                if 'aliases' in players[player] and \
                    alias.lower() in map(lambda x:x.lower(), players[player]['aliases']):
                    return player
        else:
            if not alias in players:
                for player in players:
                    if alias.lower() == player.lower(): return player

        return alias


    @staticmethod
    def player_name(data, playerid):
        players = data['players']
        if not playerid in players:
            playerid = Data.player_id(data, playerid)
        if playerid in players:
            if 'name' in players[playerid]:
                return players[playerid]['name']
        return playerid


    @staticmethod
    def player_shortname(data, playerid):
        players = data['players']
        if not playerid in players:
            playerid = Data.player_id(data, playerid)
        if playerid in players:
            if 'shortname' in players[playerid]:
                return players[playerid]['shortname']
        return playerid


    @staticmethod
    def get_imgurl(data, key):
        images = data['images']
        if key in images: return images[key]
        return key


    @staticmethod
    def upgrade_data(data):

        # convert 'legacy' entries to proper json-data
        for match in data['matches']:
            if 'bets' in match:
                for user in match['bets']:
                    if 'legacy' in user:
                        components = user['legacy'].split(',')
                        user['user'] = components[0]
                        user['result'] = components[1]
                        if components[2] != '-':
                            user['halftime'] = components[2]
                        if len(components) > 3:
                            user['goals'] = components[3:]
                        del user['legacy']

        # might need more 'upgrades' later
        # TODO: convert the &aa; strings and use proper utf-8

        return data


    @staticmethod
    def get_score_histogram(matrix, vertical, horizontal):
        histogram = []
        if vertical:
            for y in range(20, -1, -1):
                count = 0
                for x in range(0, 21):
                    score = '%d-%d' % (y + x * horizontal, x)
                    if score in matrix:
                        count += matrix[score]
                histogram.append(count)

        if horizontal:
            for x in range(vertical, 21):
                count = 0
                for y in range(0, 21):
                    score = '%d-%d' % (y, x + y * vertical)
                    if score in matrix:
                        count += matrix[score]
                histogram.append(count)

        while len(histogram) > 2:
            crop = True
            if vertical: crop &= not histogram[1]
            if horizontal: crop &= not histogram[-2]
            if crop:
                if vertical: histogram.pop(0)
                if horizontal: histogram.pop()
            else:
                break

        if vertical and not horizontal: histogram.reverse()
        return histogram


