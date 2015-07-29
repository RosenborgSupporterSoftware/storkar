#!/bin/sh

source setup.sh --from-script

configfile=storkar-dev.conf
for arg in "$@"; do
  case "$arg" in
  "--profile="*)
    configfile="storkar-"`echo -- $arg | cut -d= -f2-`".conf"
    ;;
  esac
done

if test x"$configfile" != x""; then
  set -- --config "$configfile" "$@"
fi
./src/presto/src/main/boot.scm "$@"

