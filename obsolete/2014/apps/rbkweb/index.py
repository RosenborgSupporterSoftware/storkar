# -*- coding: utf-8 -*-

import json

from AppResponse import AppResponse


class IndexPage(AppResponse):


    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.dependency(js='jquery2')
        self.dependency(css='fontawesome')
        self.__data = None


    def html(self):
        html = []
        html += self.html_heading("App indeks")
        html += self.html_body_open()
        html += self.html_header("App indeks")
        html += self.html_content_open()

        html += [
            '<div align="center">',
            '<font size="+2">'
        ]
        if self.get_user() != 'anonym':
            html += [
                '<a href="MatchBetting.py">Resultattips</a><br>'
            ]
        html += [
            '<a href="TeamFormation.py">Lagoppstilling</a>',
            '</font>']

        html += ['</div>']

        html += self.html_content_close()
        html += self.html_footer()
        html += self.html_body_close()
        return html


def run(client):
    return IndexPage(client)

