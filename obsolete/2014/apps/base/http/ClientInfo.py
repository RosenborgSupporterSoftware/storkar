# -*- coding: utf-8 -*-
# vim:sw=4

import sys
import base64
from urlparse import urlparse
import urllib

class ClientInfo(object):
    """
    Object for parsing the request from the HTTP client.
    """


    def __init__(self, environ, defaults={}, dump=False):
        self.__environ = environ.copy()
        self.__args = {}

        self.__http_scheme = environ.get('wsgi.url_scheme', None)
        self.__http_host = environ.get('HTTP_HOST', None)
        self.__http_referer = environ.get('HTTP_REFERER', None)

        self.__script = environ.get('PATH_INFO', None)
        self.__http_method = environ.get('REQUEST_METHOD', None)

        self.__authorization = environ.get('HTTP_AUTHORIZATION', None)

        dump = False

        if dump:
            for key in sorted(environ.keys()):
                sys.stderr.write(u"env %s = '%s'\n" % (key, environ[key]))

        # parse GET args
        if self.__http_method == 'GET' and 'QUERY_STRING' in environ:
            params = environ['QUERY_STRING']
            if params != '':
                if dump:
                    sys.stderr.write(u"PARAMS: '%s'\n" % params)
                for param in params.split('&'):
                    n = param.find('=')
                    if n == -1:
                        self.__args[param] = 1
                    else:
                        key = param[0:n]
                        value = param[n+1:]
                        self.__args[key] = urllib.unquote_plus(value).decode('utf8')

            if dump:
                for key in sorted(self.__args.keys()):
                    sys.stderr.write(u"arg '%s' = '%s'\n" % (key, self.__args[key]))

        # read POST data if POST
        elif self.__http_method == 'POST':
            pass

        self.set_defaults(defaults)


    def get_environment(self):
        return self.__environ


    def get_user(self):
        if self.__authorization and self.__authorization.startswith("Basic "):
            decoded = base64.b64decode(self.__authorization[6:])
            return decoded.split(':')[0]
        return None


    def set_defaults(self, defaults):
        for key in defaults.keys():
            if not key in self.__args:
                self.__args[key] = defaults[key]


    def script(self):
        return self.__script


    def referer(self):
        return self.__http_referer


    def method(self):
        return self.__http_method;


    def arg(self, key):
        if not key in self.__args: return None
        return self.__args[key]

