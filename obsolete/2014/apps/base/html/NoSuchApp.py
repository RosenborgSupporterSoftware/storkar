# -*- coding: utf-8 -*-

from base.http.Response import Response

class NoSuchApp(Response):

    def __init__(self, client):
        Response.__init__(self, client)

    def status(self):
        return '404 Not found'

    def html(self):
        html = [
            u'<!DOCTYPE html>',
            u'<html>',
            u'<head>',
            u'<title>Application not found</title>',
            u'</head>',
            u'<body>',
            u'<h1>Application not found</h1>']

        if self.client.referer():
            html += [
                u'<a href="%s">Go back</a>' % self.client.referer()
            ]

        html += [
            u'</body>',
            u'</html>']
        return html

