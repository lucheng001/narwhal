#!/usr/bin/env bash

BASEDIR=$(cd "$(dirname "$0")";pwd)
APPDIR=$(dirname "$BASEDIR")

PIDFILE="$APPDIR/run/application.pid"
SOCKFILE="$APPDIR/run/application.sock"

if [ -e "$PIDFILE" ]; then
    kill -TERM $(cat "$PIDFILE")
fi

if [ -e "$PIDFILE" ]; then
    rm -f "$PIDFILE"
fi

if [ -e "$SOCKFILE" ]; then
    rm -f "$SOCKFILE"
fi

