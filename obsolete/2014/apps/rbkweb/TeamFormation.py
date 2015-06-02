# -*- coding: utf-8 -*-

import os
import json

from AppResponse import AppResponse
from Data import Data


class IndexPage(AppResponse):

    def __init__(self, client):
        AppResponse.__init__(self, client)
        self.dependency(js='jquery2')
        self.dependency(js='/apps/rbkweb/TeamFormation.js')
        self.dependency(css='fontawesome')
        self.__data = None


    def load_data(self):
        os.system('cd rbkweb/data && git pull')
        f = open('rbkweb/data/data.json', 'r')
        self.__data = Data.upgrade_data(json.load(f))
        f.close()


    def get_imgurl(self, key):
        images = self.__data['images']
        if key in images:
            return images[key]
        return key


    def dummy_team(self):
        return '\n'.join([u'Hansen',
                          u'',
                          u'Svensson Holmar Reginiussen Dorsin',
                          u'',
                          u'OKS',
                          u'Jensen FM',
                          u'',
                          u'PAH EN',
                          u'TM'])


    def html(self):
        self.load_data()

        html = []
        html += self.html_heading(u"Lagoppstilling")
        html += self.html_body_open()
        html += self.html_header(u"Lagoppstilling")
        html += self.html_content_open()

        html += [
            u'<div align="center">',
            u'<textarea id="input" style="resize:none;" cols="40" rows="11">']
        html += [ self.dummy_team() ]
        html += [
            u'</textarea><br>',
            u'<a id="format" title="Oppdater" href="#">',
            u'<i class="fa fa-arrow-circle-down"></i>',
            u'</a><p/>',
            u'</div>',
            u'<div id="formation" align="center">',
            u'</div>',

            u'<script>',
            u'$("#format").click(rbkweb.teamformation.update);',
            u'rbkweb.teamformation.update();',
            u'</script>']

        html += self.html_content_close()
        html += self.html_footer()
        html += self.html_body_close()
        return html


def run(client):
    return IndexPage(client)

