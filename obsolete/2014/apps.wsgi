# -*- coding: utf-8 -*-
# vim:ft=python:sw=4

import os
import os.path
import sys
import importlib
import datetime
import time

from base.http.ClientInfo import ClientInfo

from base.html.AppFailure import AppFailure
from base.html.NoSuchApp import NoSuchApp

# WSGI_ROOT = '/var/www/apps'


importtimes = {}


def application(environ, start_response):

    try:
        client = ClientInfo(environ)

        modfile = client.script()
        if modfile.find('/apps/') == 0:
            modfile = modfile[6:]

        module = None
        if os.path.exists(modfile):
            pathname = modfile
            modfile = modfile[:-3].replace('/', '.')
            now = time.mktime(datetime.datetime.now().timetuple())
            if modfile in importtimes:
                modtime = os.stat(pathname).st_mtime
                module = importlib.import_module(modfile)
                if modtime > importtimes[modfile]:
                    sys.stderr.write("RELOADING updated module %s!\n" % modfile)
                    reload(module)
                    importtimes[modfile] = now
            else:
                module = importlib.import_module(modfile)
                importtimes[modfile] = now

        if not module or not hasattr(module, 'run'):
            response = NoSuchApp(client)

            headers = response.headers()
            contents = u'\n'.join(response.html()).encode('utf-8')
            if not 'Content-Length' in headers:
                headers += [('Content-Length', '%d' % len(contents))]

            start_response(response.status(), headers)
            return contents

    except Exception as e:
        # WSGI system failure, not Application failure
        response = AppFailure(environ, exception=e)
        headers = response.headers()
        contents = u'\n'.join(response.html()).encode('utf-8')
        if not 'Content-Length' in headers:
            headers += [('Content-Length', '%d' % len(contents))]

        start_response(response.status(), headers)
        return contents

    try:
        run = getattr(module, 'run')
        app = run(client)

        if client.method() == "GET" or client.method() == "POST":
            contents = u'\n'.join(app.html()).encode('utf-8')

        elif client.method() == "HEAD":
            sys.stderr.write("HEAD request!\n")
            contents = u'\n'.join(app.head()).encode('utf-8')

        else:
            sys.stderr.write("UNKNOWN request %s!\n" % client.method())

        headers = app.headers()
        hastype = False
        haslength = False
        for header in headers:
            if header[0] == 'Content-Type':
                hastype = True
            if header[0] == 'Content-Length':
                haslength = True

        if not hastype:
            headers += [('Content-Type', 'text/html; charset=utf-8')]

        if not haslength in headers:
            headers += [('Content-Length', '%d' % len(contents))]

        start_response(app.status(), headers)
        return contents

    except Exception as e:
        response = AppFailure(environ, exception=e)
        headers = response.headers()
        contents = u'\n'.join(response.html()).encode('utf-8')
        if not 'Content-Length' in headers:
            headers += [('Content-Length', '%d' % len(contents))]
        start_response(response.status(), headers)
        return contents

