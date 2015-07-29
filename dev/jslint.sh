#!/bin/sh

for scriptfile in `find webapps/storkar-dev -name "*.js"`; do
    echo $scriptfile;
    jslint -nologo -nofilelisting -nosummary -process $scriptfile;
done
