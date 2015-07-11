#!/usr/bin/env chibi-scheme -r

(import (chibi) (chibi show) (chibi io))

(define (application request)
  (define status 200)
  (define headers '(("Content-Type" . ("text/html" "charset=utf-8"))))
  (define page
    (string->utf8 (show #f
      "<html>" nl
      "<head>" nl
      "<title>Main Page</title>" nl
      "</head>" nl
      "<body>" nl
      "<img alt=\"[Storkar]\" src=\"/gfx/stork.png\" style=\"position: absolute; left: 0px; top: 0px; z-index: -1;\"/>" nl
      "<img alt=\"[Storkar]\" src=\"/gfx/tophatguy.png\" style=\"position: absolute; right: 0px; top: 0px; z-index: -1;\"/>" nl
      "<h1 style=\"margin-top: 40px;\" align=\"center\">Storkar Dummy Page</h1>" nl
      "<p style=\"margin-top: 100px;\">" nl
      "Beklageligvis er det enn så lenge det gamle systemet under obsolete/" nl
      "som er i bruk. Et nytt mer snasent rammeverk er under utvikling." nl
      "<p>" nl
      "For å si det på en annen måte... :)<br><i>\"This site is under construction.\"</i>" nl
      "</body>" nl
      "</html>" nl)))
  (list status headers page))

(define (main args)
  (display (application #t))
  (newline))
