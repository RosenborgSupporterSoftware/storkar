#!/bin/sh

# FIXME: also minify html-templates and css?
for scriptfile in `find webapps/storkar-dev -name "*.js" -o -name "*.html" -o -name "*.css"`; do
  echo minifying $scriptfile;
  minscriptfile=`echo $scriptfile | sed -e 's/storkar-dev/storkar-min/'`;
  dir=`dirname $minscriptfile`;
  echo $dir $minscriptfile;
  test -d $dir || mkdir -p $dir/;
  jsmin <$scriptfile >$minscriptfile;
done
