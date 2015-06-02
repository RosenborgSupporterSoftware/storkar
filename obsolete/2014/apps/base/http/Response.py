# vim:sw=4

import random
import json


class Response(object):


    def __init__(self, client):
        self.client = client
        self.__js_deps = {}
        self.__css_deps = {}
        random.seed()
        self.__random = random.random()
        self.__response_type = "html"


    def get_environment(self):
        return self.client.get_environment()


    def get_user(self):
        return self.client.get_user()


    def set_response_type(self, responsetype):
        self.__response_type = responsetype


    def status(self):
        return '200 OK'


    def headers(self):
        if self.__response_type == "html":
            return [('Content-Type', 'text/html; charset=utf-8')]
        elif self.__response_type == "json":
            return [('Content-Type', 'application/json; charset=utf-8')]
        elif self.__response_type == "text":
            return [('Content-Type', 'text/plain; charset=utf-8')]
        else:
            sys.stderr.write("Unknown response-type '%s'.\n" % self.__response_type)
            return [('Content-Type', 'text/html; charset=utf-8')]


    def dependency(self, js=None, css=None):
        if js:
            self.__js_deps[js] = True
        if css:
            self.__css_deps[css] = True


    def make_js_header(self, local, external=None, namespace=None):
        if external and namespace:
            return u'<script language="javascript" type="text/javascript" src="%s"></script>\n<script language="javascript">if (!window.%s) { document.write(\'<script src="%s"><\\/script>\'); }</script>' % (external, namespace, local)
        else:
            return u'<script language="javascript" type="text/javascript" src="%s?%f"></script>' % (local, self.__random)


    def get_js_headers(self):
        headers = []
        if 'jquery2' in self.__js_deps:
            headers += [ self.make_js_header(u'/apps/other/js/jquery-2.1.0.min.js', u'//ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js', 'jQuery') ]
        if 'jquery2ui' in self.__js_deps:
            headers += [ self.make_js_header(u'/apps/other/js/jquery-ui-1.10.4/ui/jquery-ui.js') ]
        if 'jquery' in self.__js_deps:
            headers += [ self.make_js_header(u'/apps/other/js/jquery-1.11.0.min.js', u'//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js', 'jQuery') ]
        if 'jqueryui' in self.__js_deps:
            headers += [ self.make_js_header(u'/apps/other/js/jquery-ui-1.10.4/ui/jquery-ui.js') ]

        for key in self.__js_deps:
            if key == 'jquery': pass
            if key == 'jqueryui': pass
            elif key == 'jquery2': pass
            elif key == 'jquery2ui': pass
            elif key.find('/') == 0:
                headers += [ self.make_js_header(key) ]
        return headers


    def make_css_header(self, path, external=None):
        if external:
            return u'<link rel="stylesheet" type="text/css" href="%s">' % external
        else:
            return u'<link rel="stylesheet" type="text/css" href="%s?%s">' % (path, self.__random)


    def get_css_headers(self):
        headers = []
        for key in self.__css_deps:
            if key == 'fontawesome':
                headers += [ self.make_css_header(u'/apps/other/css/font-awesome-4.0.3/css/font-awesome.min.css', u'https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css') ]
            if key == 'jqueryui':
                headers += [ self.make_css_header(u'/apps/other/js/jquery-ui-1.10.4/themes/base/jquery-ui.css', u'http://code.jquery.com/ui/1.10.4/jquery-ui.min.js') ]


        for key in self.__css_deps:
            if key == 'fontawesome': pass
            if key == 'jqueryui': pass
            elif key.find('/') == 0:
                headers += [ self.make_css_header(key) ]

        return headers


    def head(self):
        """ attempt to handle HEAD requests for optimization purposes. """
        return [u'']


    def html(self):
        return [u'']


    def return_json_success(self):
        return [ json.dumps({ 'status': 'OK' }) ]


    def return_json_error(self, msg):
        return [ json.dumps({ 'status': 'error', 'message': msg }) ]


