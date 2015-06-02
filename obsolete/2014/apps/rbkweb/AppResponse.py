# -*- coding: utf-8 -*-

from base.http.Response import Response


class AppResponse(Response):


    def __init__(self, client):
        Response.__init__(self, client)
        self.dependency(css='fontawesome')


    def html_heading(self, pagetitle="Resultattipsresultater 2015"):
        html = [
            u'<!DOCTYPE html>',
            u'<html>',
            u'<head>'] + \
            self.get_css_headers() + \
            self.get_js_headers() + \
            [u'<meta http-equiv="Content-Type" content="text/html; charset=utf-8">',
            u'<title>RBKWEB: %s</title>' % pagetitle,
            u'</head>']
        return html


    def html_body_open(self):
        if self.get_user() == "larsa":
            return [u'<body style="margin:0; padding:0;">',
                    u'<div style="height:0; visibility:hidden;">',
                    u'<script>',
                    u'window.base = window.base || {};',
                    u'base = base || {};',
                    u'base.restart_wsgi = function() {',
                    u'    $.ajax({url: "/apps/base/util/restart.py"});',
                    u'};',
                    u'</script>',
                    u'<a href="javascript:base.restart_wsgi();" accesskey="r">restart</a>',
                    u'</div>']
        else:
            return [u'<body style="margin:0; padding:0;">']


    def html_body_close(self):
        return [u'</body>',
                u'</html>']


    def html_content_open(self):
        return [u'<div style="margin:0; padding:10px;">']


    def html_content_close(self):
        return [u'</div>', u'<br>']


    def html_header(self, title=u"Resultattipsresultater 2015", sections=None):
        html = [
            u'<div style="background:black;padding:10px;">',
            u'<table width="100%" cellspacing=0 cellpadding=5>',
            u'<tr>',
            u'<td width="10%"></td>',
            u'<td width="80%%" align="center"><font size="+2" style="color:white;">RBKWEB: %s</font></td>' % title,
            u'<td align="right"><a style="color:white;" href="/apps/base/util/restart.py" title="Restart WSGI"><i class="fa fa-refresh"></i></a></td>',
            u'</tr>',
            u'<tr>',
            u'<td colspan="3" align="center"><font style="color:white;">']

        menu = [{'link':'/apps/rbkweb/', 'title':'App-indeks'}]
        if sections: menu += sections

        for link in menu:
            html += [
                u'[<a style="color:white;" href="%s">%s</a>] ' % (link['link'], link['title'])
            ]

        html += [
            u'</font></td>',
            u'</tr>',
            u'</table>',
            u'</div>',
            u'<p>'
        ]
        return html


    def html_footer(self):
        html = [
            u'<div style="background:black;color:white;padding:10px;">'
        ]

        if self.get_user() == "larsa":
            html += [
                u'<div align="right"><a style="color:white;" href="/apps/base/util/restart.py" title="Restart WSGI"><i class="fa fa-refresh"></i></a></div>'
            ]

        html += [
            u'</div>'
        ]
 
        return html

