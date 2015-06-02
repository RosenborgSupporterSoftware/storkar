# -*- coding: utf-8 -*-

# see https://developers.google.com/chart/image/docs/making_charts
# and https://developers.google.com/chart/image/docs/chart_params



class Chart(object):

    urlbase = "https://chart.googleapis.com/chart"


    @staticmethod
    def get_round(idx):
        return idx


    @classmethod
    def get_chart_urlbase(cls):
        return cls.urlbase


    @classmethod
    def _join_data(cls, string, array):
        data = ""
        for num in array:
            data += "%d%s" % (num, string)
        data = data[:-len(string)]
        return data


    @classmethod
    def get_results_pie_imgurl(cls, goals, zeroidx, width, height):
        wins = 0
        losses = 0
        evens = goals[zeroidx]
        for i in range(0, zeroidx): losses += goals[i]
        for i in range(zeroidx+1, len(goals)): wins += goals[i]


        if not wins and not losses and not evens:
            wins = 1
            losses = 1
            evens = 1

        # FIXME: labels with just the numbers, before the numbers are adjusted
        # chma=l,r,t,b - chart margin
        url = Chart.get_chart_urlbase() + \
            "?chs=%dx%d" % (width, height) + \
            "&chco=00ff00,ffff00,ff0000" + \
            "&chf=bg,s,ffffff00" + \
            "&cht=p3" + \
            "&chma=0,0,0,0" + \
            "&chl=%d|%d|%d" % (wins, evens, losses) + \
            "&chd=t:%d,%d,%d" % (wins, evens, losses)

        return url


    @classmethod
    def get_goals_imgurl(cls, goals, zeroidx, width, height, maxval, signlabels=False):
        # chbh - barwidth,spacing,seriesspacing
        data = ""
        for count in goals:
            if len(data): data += ","
            data += "%d" % count

        labels = ""
        if zeroidx or signlabels:
            labels = None
            for i in range(-zeroidx, len(goals) - zeroidx):
                if not labels:
                    labels = "%d" % i
                else:
                    if i > 0:
                        labels += "|%%2b%d" % i
                    else:
                        labels += "|%d" % i
            labels = "&chl=" + labels

        url = Chart.get_chart_urlbase() + \
            "?chs=%dx%d" % (width, height) + \
            "&cht=bvs" + \
            "&chbh=10,2,0" + \
            "&chco=000000" + \
            "&chxt=x,y" + \
            "&chds=0,%d" % maxval + \
            "&chxr=1,0,%d" % maxval + \
            "&chf=bg,s,ffffff00" + \
            "&chd=t:" + data + \
            labels

        return url


    @classmethod
    def get_confidence_imgurl(cls, trend, width, height):

        data = ""
        for d in trend: data += "%d," % d
        data = data[:-1]

        colors = ""
        prev = 0
        idx = 0
        for d in trend:
            if idx > 0:
                if d >= (prev * 0.9) or d >= 75.0 or (prev - d) <= 5: # green
                    color="00ff00"
                else: #red
                    color="ff0000"
                colors += "B,%s,0,%d:%d,0|" % (color, idx-1, idx)
            idx += 1
            prev = d
        colors = colors[:-1]

        url = Chart.get_chart_urlbase() + \
            "?chs=%dx%d" % (width, height) + \
            "&cht=ls" + \
            "&chco=000000" + \
            "&chf=bg,s,ffffff00" + \
            "&chd=t:%s" % data + \
            "&chm=%s" % colors

        return url


    @classmethod
    def get_team_position_imgurl(cls, trend, width, height):

        data = ""
        for d in trend: data += "-%d," % d
        data = data[:-1]

        url = Chart.get_chart_urlbase() + \
            "?chs=%dx%d" % (width, height+5) + \
            "&chf=bg,s,ff00ff00" + \
            "&chco=cccccc" + \
            "&cht=lxy" + \
            "&chxt=" + \
            "&chds=0.5,40,-25,0" + \
            "&chd=t:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30|%s" % data

        return url


    @classmethod
    def get_betcount_imgurl(cls, betcounts, hits, width, height):

        if not betcounts:
            return None
        maxbets = max(betcounts)
        while maxbets % 10 != 0: maxbets += 1
        maxhits = max(hits)
        while maxhits % 4 != 0: maxhits += 1
        maxhits = 20

        roundlabels = map(Chart.get_round, range(1, len(betcounts)+1))
        colwidth = ((width - 35) / len(betcounts)) - 4

        url = Chart.get_chart_urlbase() + \
            "?chs=%dx%d" % (width, height) + \
            "&chf=bg,s,ff00ff00" + \
            "&chco=000000" + \
            "&cht=bvs" + \
            "&chxt=r,y,x" + \
            "&chbh=%d,4,0" % int(colwidth) + \
            "&chxr=0,0,%d,0|1,0,%d,0" % (maxhits,maxbets) + \
            "&chds=0,%d.0,0,%d.0" % (maxhits, maxbets) + \
            "&chxl=2%%3A|%s|" % Chart._join_data('|', roundlabels) + \
            "&chd=t1%%3A%s" % Chart._join_data(',', hits) + \
            "|" + Chart._join_data(',', betcounts) + \
            "&chm=D,000000,1,0,1"

        return url


