#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from AppResponse import AppResponse


class Environment(AppResponse):
    def __init__(self, client):
        AppResponse.__init__(self, client)


    def head(self):
        html = []
        html += [u'HEAD request']
        html += self.html()
        return html


    def html(self):
        html = []

        html += self.html_heading()
        html += self.html_body_open()
        html += self.html_header(u'Environment')
        html += self.html_content_open()

        html += [u'<table>',
                 u'<tr><td colspan="2" align="center"><b>os.environ</b></td></tr>']

        for key in os.environ:
            html += [u'<tr><td>%s</td><td>%s</td></tr>' % (key, os.environ[key])]

        html += [u'<tr><td colspan="2" align="center"><b>application(environ)</b></td></tr>']

        env = self.get_environment()
        for key in env:
            html += [u'<tr><td>%s</td><td>%s</td></tr>' % (key, env[key])]

        html += [u'</table>']

        html += self.html_content_close()
        html += self.html_footer()
        html += self.html_body_close()
        return html


def run(client):
    return Environment(client)

