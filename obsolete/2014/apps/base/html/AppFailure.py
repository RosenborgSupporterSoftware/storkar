# -*- coding: utf-8 -*-
# vim:sw=4

import sys
import traceback

from base.http.Response import Response


class AppFailure(Response):

    def __init__(self, environ, exception=None):
        Response.__init__(self, environ)

        self.__exception = exception

    def status(self):
        return '500 Internal Error'

    def html(self):
        html = [
            u'<html>',
            u'<head>',
            u'<title>Application failure</title>',
            u'</head>',
            u'<body>',
            u'<h1>Application Failure</h1>']

        if self.__exception:
            html += [
                u'<h2>Exception information</h2>',
                u'<b>Type</b>: %s<br>' % self.__exception.__class__.__name__,
                u'<b>Message</b>: %s<br>' % str(self.__exception),
                u'<pre>',
                u'%s' % traceback.format_exc().decode("utf-8"),
                u'</pre>',
                u'']

        html += [
            u'<div align="right">',
            u'<a href="/apps/base/util/restart.py">Retry</a>',
            u'</div>']

        html += [
            u'</body>',
            u'</html>']

        sys.stderr.write('\n'.join(html))

        return html

