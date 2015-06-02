# vim:sw=4

import os

from base.http.Response import Response


WSGI_FILE = '/var/www/apps.wsgi'

class ReloadPage(Response):

    def __init__(self, client):
        Response.__init__(self, client)
        self.ok = self.force_reload()


    def touch_file(self, filename):
        errorcode = os.system('touch %s' % filename)
        return errorcode == 0


    def force_reload(self):
        return self.touch_file(WSGI_FILE)


    def html(self):
        html = ['<html>',
                '<head>',
                '<title>WSGI restarting...</title>']
        if self.client.referer():
            html += ['<meta http-equiv="refresh" content="3;url=%s"/>' % self.client.referer()]
        html += ['</head>',
                 '<body>',
                 '<h4>WSGI restarting...</h4>']
        if self.client.referer():
            html += ['<a href="%s">Back</a>' % self.client.referer()]
        html += ['</body>',
                 '</html>']

        return html


def run(client):
    return ReloadPage(client)


if __name__ == "__main__":
    run()

